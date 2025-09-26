from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from models import DisputeRequest, DisputeResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dispute", tags=["dispute"])


@router.post("/raise", response_model=DisputeResponse)
async def raise_dispute(request: DisputeRequest):
    """Raise a transaction dispute"""
    try:
        logger.info(
            f"Dispute request for amount: {request.amount}, date: {request.transaction_date}"
        )

        # Generate dispute ticket
        ticket_id = f"DISPUTE{random.randint(10000, 99999)}"
        estimated_days = random.randint(5, 30)

        response = DisputeResponse(
            ticket_id=ticket_id,
            content="UNDER_REVIEW",
            amount=request.amount,
            estimated_resolution_days=estimated_days,
            status=Status.SUCCESS,
        )

        logger.info(f"Dispute raised successfully with ticket ID: {ticket_id}")
        return response

    except Exception as e:
        logger.error(f"Error raising dispute: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
