from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from mock_data_storage import mock_storage
from database import db_manager
from services.sms_service import sms_service, SMSTemplates
from models import CardBlockRequest, CardBlockResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/card", tags=["card"])


@router.post("/block", response_model=CardBlockResponse)
async def block_card(request: CardBlockRequest):
    """Block a card"""
    try:
        logger.info(f"Card block request for card ending with: {request.last4}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                card = await conn.fetchrow(
                    "SELECT * FROM cards WHERE card_number LIKE $1", f"%{request.last4}"
                )
                if card:
                    # Simulate card blocking process
                    blocked_at = datetime.now()
                    ticket_id = f"BLOCK{random.randint(10000, 99999)}"

                    # Update card status in database
                    await conn.execute(
                        "UPDATE cards SET card_status = $1 WHERE card_number LIKE $2",
                        "BLOCKED",
                        f"%{request.last4}",
                    )

                    response = CardBlockResponse(
                        card_number=f"****{request.last4}",
                        content="BLOCKED",
                        blocked_at=blocked_at.isoformat(),
                        ticket_id=ticket_id,
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Card blocked in database for card ending with: {request.last4}"
                    )
                    return response

        # Fallback to mock data
        card = mock_storage.get_card_by_last4(request.last4)
        if not card:
            logger.warning(f"Card not found ending with: {request.last4}")
            raise HTTPException(status_code=404, detail="Card not found")

        # Get account details to retrieve customer info and mobile numbers
        account = mock_storage.get_account_by_number(card["account_number"])
        if not account:
            logger.warning(f"Account not found: {card['account_number']}")
            # Continue with card blocking even if account not found

        # Simulate card blocking process
        blocked_at = datetime.now()
        ticket_id = f"BLOCK{random.randint(10000, 99999)}"

        # Update card status in mock data
        card["card_status"] = "BLOCKED"

        # Send SMS notification to customer if account and mobile numbers are available
        if account and account.get("mobile_numbers") and sms_service.is_enabled():
            customer_name = account.get("customer_name", "Customer")
            reason = request.reason or "security reasons"
            sms_message = SMSTemplates.account_alert(
                customer_name,
                "Card Blocked",
                f"Your card ending with {request.last4} has been blocked for {reason}. Ticket ID: {ticket_id}"
            )
            
            # Send SMS to all mobile numbers
            sms_result = await sms_service.send_bulk_sms(
                account["mobile_numbers"],
                sms_message
            )
            
            if sms_result["success"]:
                logger.info(f"SMS notification sent for card block {ticket_id} to {len(sms_result['successful_sends'])} numbers")
            else:
                logger.warning(f"Failed to send SMS notification for card block {ticket_id}")
        else:
            if not account:
                logger.warning(f"Account not found for card ending with {request.last4}")
            elif not account.get("mobile_numbers"):
                logger.warning(f"No mobile numbers found for account {card['account_number']}")
            if not sms_service.is_enabled():
                logger.info("SMS service not enabled, skipping notification")

        response = CardBlockResponse(
            card_number=f"****{request.last4}",
            content="BLOCKED",
            blocked_at=blocked_at.isoformat(),
            ticket_id=ticket_id,
            status=Status.SUCCESS,
        )

        logger.info(f"Card blocked in mock data for card ending with: {request.last4}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error blocking card ending with {request.last4}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
