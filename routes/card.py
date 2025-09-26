from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from mock_data_storage import mock_storage
from database import db_manager
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

        # Simulate card blocking process
        blocked_at = datetime.now()
        ticket_id = f"BLOCK{random.randint(10000, 99999)}"

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
