from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging

from mock_data_storage import mock_storage
from database import db_manager
from models import KYCStatusRequest, KYCStatusResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/kyc", tags=["kyc"])


@router.post("/status", response_model=KYCStatusResponse)
async def get_kyc_status(request: KYCStatusRequest):
    """Get KYC status"""
    try:
        logger.info(f"KYC status request for account: {request.account_number}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                account = await conn.fetchrow(
                    "SELECT * FROM accounts WHERE account_number = $1",
                    request.account_number,
                )
                if account:
                    response = KYCStatusResponse(
                        account_number=f"******{request.account_number[-4:]}",
                        kyc_status=account["kyc_status"],
                        verification_level=account["kyc_level"],
                        last_updated=account["last_updated"].isoformat() if isinstance(account["last_updated"], datetime) else str(account["last_updated"]),
                        documents_required=[],
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"KYC status retrieved from database for account: {request.account_number}"
                    )
                    return response

        # Fallback to mock data
        account = mock_storage.get_account_by_number(request.account_number)
        if not account:
            logger.warning(f"Account not found: {request.account_number}")
            raise HTTPException(status_code=404, detail="Account not found")

        response = KYCStatusResponse(
            account_number=f"******{request.account_number[-4:]}",
            kyc_status=account["kyc_status"],
            verification_level=account["kyc_level"],
            last_updated=account["last_updated"].isoformat() if isinstance(account["last_updated"], datetime) else str(account["last_updated"]),
            documents_required=[],
            status=Status.SUCCESS,
        )

        logger.info(
            f"KYC status retrieved from mock data for account: {request.account_number}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting KYC status for account {request.account_number}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")
