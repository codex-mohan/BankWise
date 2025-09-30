from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from mock_data_storage import mock_storage
from database import db_manager
from services.sms_service import sms_service, SMSTemplates
from models import (
    ComplaintRequest,
    ComplaintStatusRequest,
    ComplaintResponse,
    Complaint,
    Status,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/complaint", tags=["complaint"])


# Configuration for complaint priority and resolution time
COMPLAINT_CONFIG = {
    "ACCOUNT": {"priority": "MEDIUM", "days": 5},
    "CARD": {"priority": "HIGH", "days": 3},
    "TRANSACTION": {"priority": "HIGH", "days": 2},
    "ATM": {"priority": "MEDIUM", "days": 7},
    "BRANCH": {"priority": "LOW", "days": 10},
    "LOAN": {"priority": "HIGH", "days": 7},
    "FD": {"priority": "LOW", "days": 10},
    "NET_BANKING": {"priority": "MEDIUM", "days": 3},
    "MOBILE_BANKING": {"priority": "MEDIUM", "days": 3},
    "OTHER": {"priority": "LOW", "days": 15},
    "DEFAULT": {"priority": "LOW", "days": 15}
}


@router.post("/new", response_model=ComplaintResponse)
async def create_complaint(request: ComplaintRequest):
    """Create a new complaint"""
    try:
        logger.info(f"Complaint creation request for account: {request.account_number}")

        # Get account details to retrieve customer info and mobile numbers
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")

        # Determine priority and resolution days from config
        config = COMPLAINT_CONFIG.get(request.category.upper(), COMPLAINT_CONFIG["DEFAULT"])
        priority = config["priority"]
        estimated_days = config["days"]

        # Create a new complaint data dict
        complaint_data = {
            "account_number": request.account_number,
            "subject": request.subject,
            "description": request.description,
            "category": request.category,
            "priority": priority,
            "estimated_resolution_days": estimated_days
        }

        # Add to mock storage using the proper method
        new_complaint_dict = mock_storage.add_complaint(complaint_data)
        new_complaint = Complaint(**new_complaint_dict)

        # Send SMS notification to customer
        if account.get("mobile_numbers") and sms_service.is_enabled():
            customer_name = account.get("customer_name", "Customer")
            sms_message = SMSTemplates.complaint_confirmation(
                new_complaint.ticket_id,
                customer_name
            )
            
            # Send SMS to all mobile numbers
            sms_result = await sms_service.send_bulk_sms(
                account["mobile_numbers"],
                sms_message
            )
            
            if sms_result["success"]:
                logger.info(f"SMS notification sent for complaint {new_complaint.ticket_id} to {len(sms_result['successful_sends'])} numbers")
            else:
                logger.warning(f"Failed to send SMS notification for complaint {new_complaint.ticket_id}")
        else:
            if not account.get("mobile_numbers"):
                logger.warning(f"No mobile numbers found for account {request.account_number}")
            if not sms_service.is_enabled():
                logger.info("SMS service not enabled, skipping notification")

        response = ComplaintResponse(
            complaint=new_complaint,
            status=Status.SUCCESS,
        )

        logger.info(f"Complaint created successfully with ticket ID: {new_complaint.ticket_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating complaint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/update-status", response_model=ComplaintResponse)
async def update_complaint_status(request: ComplaintStatusRequest):
    """Update complaint status and send SMS notification if resolved"""
    try:
        logger.info(f"Updating complaint status for ticket ID: {request.ticket_id}")
        
        # Find the complaint in mock storage
        complaint_data = mock_storage.get_complaint_by_id(request.ticket_id)
        if not complaint_data:
            logger.warning(f"Complaint not found with ticket ID: {request.ticket_id}")
            raise HTTPException(status_code=404, detail="Complaint not found")
        
        # Get account details for SMS notification
        account = mock_storage.get_account_by_number(complaint_data["account_number"])
        if not account:
            logger.warning(f"Account not found: {complaint_data['account_number']}")
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Update complaint status using the proper update method
        original_status = complaint_data["status"]
        update_data = {
            "status": "RESOLVED",
            "resolved_at": datetime.now(),
            "resolution_notes": "Complaint has been resolved successfully"
        }
        
        # Update the complaint in storage
        updated_complaint = mock_storage.update_complaint(request.ticket_id, update_data)
        if not updated_complaint:
            logger.error(f"Failed to update complaint with ticket ID: {request.ticket_id}")
            raise HTTPException(status_code=500, detail="Failed to update complaint")
        
        # Send SMS notification if status changed to resolved
        if original_status != "RESOLVED" and account.get("mobile_numbers") and sms_service.is_enabled():
            customer_name = account.get("customer_name", "Customer")
            sms_message = SMSTemplates.complaint_resolution(
                request.ticket_id,
                customer_name
            )
            
            # Send SMS to all mobile numbers
            sms_result = await sms_service.send_bulk_sms(
                account["mobile_numbers"],
                sms_message
            )
            
            if sms_result["success"]:
                logger.info(f"SMS notification sent for complaint resolution {request.ticket_id} to {len(sms_result['successful_sends'])} numbers")
            else:
                logger.warning(f"Failed to send SMS notification for complaint resolution {request.ticket_id}")
        
        complaint = Complaint(**updated_complaint)
        response = ComplaintResponse(
            complaint=complaint,
            status=Status.SUCCESS,
        )
        
        logger.info(f"Complaint status updated successfully for ticket ID: {request.ticket_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating complaint status for ticket ID {request.ticket_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/status", response_model=ComplaintResponse)
async def get_complaint_status(request: ComplaintStatusRequest):
    """Get complaint status"""
    try:
        logger.info(f"Complaint status request for ticket ID: {request.ticket_id}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                complaint_data = await conn.fetchrow(
                    "SELECT * FROM complaints WHERE ticket_id = $1", request.ticket_id
                )
                if complaint_data:
                    # Convert datetime fields to ISO format strings
                    complaint_dict = dict(complaint_data)
                    for field in ['created_at', 'resolved_at']:
                        if field in complaint_dict and complaint_dict[field] is not None:
                            if hasattr(complaint_dict[field], 'isoformat'):
                                complaint_dict[field] = complaint_dict[field].isoformat()
                    complaint = Complaint(**complaint_dict)
                    response = ComplaintResponse(
                        complaint=complaint,
                        status=Status.SUCCESS,
                    )
                    logger.info(
                        f"Complaint status retrieved from database for ticket ID: {request.ticket_id}"
                    )
                    return response

        # Fallback to mock data
        complaint_data = mock_storage.get_complaint_by_id(request.ticket_id)
        if not complaint_data:
            logger.warning(f"Complaint not found with ticket ID: {request.ticket_id}")
            raise HTTPException(status_code=404, detail="Complaint not found")

        complaint = Complaint(**complaint_data)

        response = ComplaintResponse(
            complaint=complaint,
            status=Status.SUCCESS,
        )

        logger.info(
            f"Complaint status retrieved from mock data for ticket ID: {request.ticket_id}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting complaint status for ticket ID {request.ticket_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")
