from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging
import random

from models import ChequeStatusRequest, ChequeStatusResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cheque", tags=["cheque"])


@router.post("/status", response_model=ChequeStatusResponse)
async def get_cheque_status(request: ChequeStatusRequest):
    """Get cheque status"""
    try:
        logger.info(f"Cheque status request for cheque number: {request.cheque_number}")

        # Mock cheque status - randomly assign status
        statuses = ["Cleared", "Pending", "Bounced", "Under Process"]
        status = random.choice(statuses)

        # Generate mock data based on status
        if status == "Cleared":
            amount = round(random.uniform(1000, 50000), 2)
            date = (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            clearing_date = (
                datetime.now() - timedelta(days=random.randint(1, 5))
            ).isoformat()
        elif status == "Pending":
            amount = round(random.uniform(1000, 50000), 2)
            date = (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat()
            clearing_date = None
        else:
            amount = round(random.uniform(1000, 50000), 2)
            date = (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            clearing_date = None

        response = ChequeStatusResponse(
            cheque_number=request.cheque_number,
            content=status,
            amount=amount,
            date=date,
            clearing_date=clearing_date,
            status=Status.SUCCESS,
        )

        logger.info(
            f"Cheque status retrieved successfully for cheque number: {request.cheque_number}"
        )
        return response

    except Exception as e:
        logger.error(
            f"Error getting cheque status for cheque number {request.cheque_number}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")