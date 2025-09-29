from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

from mock_data_storage import mock_storage
from services.sms_service import sms_service, SMSTemplates
from models import Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/sms", tags=["sms"])


class TransactionAlertRequest(BaseModel):
    account_number: str
    amount: float
    transaction_type: str  # DEBIT, CREDIT, TRANSFER, etc.
    description: Optional[str] = None


class GeneralSMSRequest(BaseModel):
    account_number: str
    message: str


class SMSResponse(BaseModel):
    success: bool
    message: str
    sent_to: List[str]
    failed_numbers: List[str]
    status: Status


@router.post("/transaction-alert", response_model=SMSResponse)
async def send_transaction_alert(request: TransactionAlertRequest):
    """Send SMS alert for a transaction"""
    try:
        logger.info(f"Transaction alert request for account: {request.account_number}")
        
        # Get account details to retrieve customer info and mobile numbers
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")
        
        if not account.get("mobile_numbers"):
            logger.warning(f"No mobile numbers found for account {request.account_number}")
            raise HTTPException(status_code=400, detail="No mobile numbers registered for this account")
        
        if not sms_service.is_enabled():
            logger.warning("SMS service not enabled")
            raise HTTPException(status_code=503, detail="SMS service not available")
        
        # Create transaction alert message
        customer_name = account.get("customer_name", "Customer")
        sms_message = SMSTemplates.transaction_alert(
            customer_name,
            request.amount,
            request.transaction_type
        )
        
        if request.description:
            sms_message += f" Description: {request.description}"
        
        # Send SMS to all mobile numbers
        sms_result = await sms_service.send_bulk_sms(
            account["mobile_numbers"], 
            sms_message
        )
        
        sent_to = [item["phone_number"] for item in sms_result["successful_sends"]]
        failed_numbers = [item["phone_number"] for item in sms_result["failed_sends"]]
        
        response = SMSResponse(
            success=sms_result["success"],
            message=f"Transaction alert sent to {len(sent_to)} numbers" if sms_result["success"] else "Failed to send transaction alert",
            sent_to=sent_to,
            failed_numbers=failed_numbers,
            status=Status.SUCCESS if sms_result["success"] else Status.FAILED
        )
        
        logger.info(f"Transaction alert processed for account {request.account_number}: sent to {len(sent_to)}, failed {len(failed_numbers)}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending transaction alert for account {request.account_number}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/send", response_model=SMSResponse)
async def send_general_sms(request: GeneralSMSRequest):
    """Send a general SMS to account holder"""
    try:
        logger.info(f"General SMS request for account: {request.account_number}")
        
        # Get account details to retrieve customer info and mobile numbers
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")
        
        if not account.get("mobile_numbers"):
            logger.warning(f"No mobile numbers found for account {request.account_number}")
            raise HTTPException(status_code=400, detail="No mobile numbers registered for this account")
        
        if not sms_service.is_enabled():
            logger.warning("SMS service not enabled")
            raise HTTPException(status_code=503, detail="SMS service not available")
        
        # Send SMS to all mobile numbers
        sms_result = await sms_service.send_bulk_sms(
            account["mobile_numbers"], 
            request.message
        )
        
        sent_to = [item["phone_number"] for item in sms_result["successful_sends"]]
        failed_numbers = [item["phone_number"] for item in sms_result["failed_sends"]]
        
        response = SMSResponse(
            success=sms_result["success"],
            message=f"SMS sent to {len(sent_to)} numbers" if sms_result["success"] else "Failed to send SMS",
            sent_to=sent_to,
            failed_numbers=failed_numbers,
            status=Status.SUCCESS if sms_result["success"] else Status.FAILED
        )
        
        logger.info(f"General SMS processed for account {request.account_number}: sent to {len(sent_to)}, failed {len(failed_numbers)}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending general SMS for account {request.account_number}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/status")
async def get_sms_service_status():
    """Get SMS service status"""
    return {
        "enabled": sms_service.is_enabled(),
        "service": "Twilio SMS",
        "status": "active" if sms_service.is_enabled() else "inactive"
    }