from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from mock_data_storage import mock_storage
from services.sms_service import sms_service, SMSTemplates
from models import DisputeRequest, DisputeResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dispute", tags=["dispute"])


@router.post("/raise", response_model=DisputeResponse)
async def raise_dispute(request: DisputeRequest):
    """Raise a transaction dispute"""
    try:
        logger.info(
            f"Dispute request for account: {request.account_number}, amount: {request.amount}, date: {request.transaction_date}"
        )

        # Get account details to retrieve customer info and mobile numbers
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")

        # Generate dispute ticket
        ticket_id = f"DISPUTE{random.randint(10000, 99999)}"
        estimated_days = random.randint(5, 30)

        # Create dispute record for mock storage
        dispute_data = {
            "ticket_id": ticket_id,
            "account_number": request.account_number,
            "transaction_id": f"TXN{random.randint(1000000, 9999999)}",
            "amount": request.amount,
            "transaction_date": request.transaction_date,
            "dispute_type": "UNAUTHORIZED",
            "reason": request.reason,
            "description": request.description or "",
            "status": "UNDER_REVIEW",
            "created_at": datetime.now().isoformat(),
            "resolved_at": None,
            "estimated_resolution_days": estimated_days,
            "assigned_officer": None,
            "resolution_notes": None,
            "evidence_submitted": "NO",
            "customer_contacted": "YES"
        }
        
        # Add to mock storage for future retrieval
        mock_storage.disputes.append(dispute_data)

        # Send SMS notification to customer
        if account.get("mobile_numbers") and sms_service.is_enabled():
            customer_name = account.get("customer_name", "Customer")
            sms_message = SMSTemplates.dispute_confirmation(
                ticket_id,
                customer_name,
                request.amount
            )
            
            # Send SMS to all mobile numbers
            sms_result = await sms_service.send_bulk_sms(
                account["mobile_numbers"],
                sms_message
            )
            
            if sms_result["success"]:
                logger.info(f"SMS notification sent for dispute {ticket_id} to {len(sms_result['successful_sends'])} numbers")
            else:
                logger.warning(f"Failed to send SMS notification for dispute {ticket_id}")
        else:
            if not account.get("mobile_numbers"):
                logger.warning(f"No mobile numbers found for account {request.account_number}")
            if not sms_service.is_enabled():
                logger.info("SMS service not enabled, skipping notification")

        response = DisputeResponse(
            ticket_id=ticket_id,
            content="UNDER_REVIEW",
            amount=request.amount,
            estimated_resolution_days=estimated_days,
            status=Status.SUCCESS,
        )

        logger.info(f"Dispute raised successfully with ticket ID: {ticket_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error raising dispute: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/update-status")
async def update_dispute_status(ticket_id: str, new_status: str):
    """Update dispute status and send SMS notification if resolved"""
    try:
        logger.info(f"Updating dispute status for ticket ID: {ticket_id}")
        
        # Find the dispute in mock storage
        dispute_data = mock_storage.get_dispute_by_id(ticket_id)
        if not dispute_data:
            logger.warning(f"Dispute not found with ticket ID: {ticket_id}")
            raise HTTPException(status_code=404, detail="Dispute not found")
        
        # Get account details for SMS notification
        account = mock_storage.get_account_by_number(dispute_data["account_number"])
        if not account:
            logger.warning(f"Account not found: {dispute_data['account_number']}")
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Update dispute status
        original_status = dispute_data["status"]
        dispute_data["status"] = new_status.upper()
        
        if new_status.upper() in ["APPROVED", "REJECTED", "RESOLVED"]:
            dispute_data["resolved_at"] = datetime.now().isoformat()
            dispute_data["resolution_notes"] = f"Dispute has been {new_status.lower()}"
            
            # Send SMS notification if status changed to resolved
            if original_status != new_status.upper() and account.get("mobile_numbers") and sms_service.is_enabled():
                customer_name = account.get("customer_name", "Customer")
                sms_message = SMSTemplates.dispute_resolution(
                    ticket_id,
                    customer_name,
                    new_status
                )
                
                # Send SMS to all mobile numbers
                sms_result = await sms_service.send_bulk_sms(
                    account["mobile_numbers"],
                    sms_message
                )
                
                if sms_result["success"]:
                    logger.info(f"SMS notification sent for dispute resolution {ticket_id} to {len(sms_result['successful_sends'])} numbers")
                else:
                    logger.warning(f"Failed to send SMS notification for dispute resolution {ticket_id}")
        
        logger.info(f"Dispute status updated successfully for ticket ID: {ticket_id}")
        return {
            "ticket_id": ticket_id,
            "status": new_status.upper(),
            "message": f"Dispute status updated to {new_status.upper()}",
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating dispute status for ticket ID {ticket_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
