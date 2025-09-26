from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging
import random

from models import ChequeStatusRequest, ChequeStatusResponse, Status
from mock_data_storage import mock_storage
from database import db_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cheque", tags=["cheque"])


@router.post("/status", response_model=ChequeStatusResponse)
async def get_cheque_status(request: ChequeStatusRequest):
    """Get cheque status"""
    try:
        logger.info(f"Cheque status request for cheque number: {request.cheque_number}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                cheque = await conn.fetchrow(
                    "SELECT * FROM cheques WHERE cheque_number = $1",
                    request.cheque_number,
                )
                if cheque:
                    response = ChequeStatusResponse(
                        cheque_number=cheque["cheque_number"],
                        content=cheque["status"],
                        amount=cheque["amount"],
                        date=cheque["issue_date"].isoformat(),
                        clearing_date=cheque["clearing_date"].isoformat()
                        if cheque["clearing_date"]
                        else None,
                        status=Status.SUCCESS,
                    )
                    logger.info(
                        f"Cheque status retrieved from database for cheque number: {request.cheque_number}"
                    )
                    return response

        # Fallback to mock data
        cheque = mock_storage.get_cheque_by_number(request.cheque_number)
        if not cheque:
            logger.warning(f"Cheque not found: {request.cheque_number}")
            raise HTTPException(status_code=404, detail="Cheque not found")

        response = ChequeStatusResponse(
            cheque_number=cheque["cheque_number"],
            content=cheque["status"],
            amount=cheque["amount"],
            date=cheque["issue_date"],
            clearing_date=cheque["clearing_date"],
            status=Status.SUCCESS,
        )

        logger.info(
            f"Cheque status retrieved from mock data for cheque number: {request.cheque_number}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting cheque status for cheque number {request.cheque_number}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")