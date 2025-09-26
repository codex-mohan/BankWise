from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging

from mock_data_storage import mock_storage
from database import db_manager
from models import LoanStatusRequest, LoanInfo, LoanStatusResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/loan", tags=["loan"])


@router.post("/status", response_model=LoanStatusResponse)
async def get_loan_status(request: LoanStatusRequest):
    """Get loan status"""
    try:
        logger.info(f"Loan status request for loan ID: {request.loan_id}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                loan = await conn.fetchrow(
                    "SELECT * FROM loans WHERE loan_id = $1", request.loan_id
                )
                if loan:
                    loan_info = LoanInfo(
                        loan_id=loan["loan_id"],
                        loan_type=loan["loan_type"],
                        principal=float(loan["principal"]),
                        emi_amount=float(loan["emi_amount"]),
                        due_date=loan["next_emi_date"].isoformat(),
                        remaining_tenure=loan["remaining_tenure"],
                        interest_rate=float(loan["interest_rate"]),
                        status=loan["status"],
                    )

                    response = LoanStatusResponse(
                        loan_info=loan_info,
                        next_payment_date=loan["next_emi_date"].isoformat(),
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Loan status retrieved from database for loan ID: {request.loan_id}"
                    )
                    return response

        # Fallback to mock data
        loan = mock_storage.get_loan_by_id(request.loan_id)
        if not loan:
            logger.warning(f"Loan not found with ID: {request.loan_id}")
            raise HTTPException(status_code=404, detail="Loan not found")

        loan_info = LoanInfo(
            loan_id=loan["loan_id"],
            loan_type=loan["loan_type"],
            principal=loan["principal"],
            emi_amount=loan["emi_amount"],
            due_date=loan["next_emi_date"],
            remaining_tenure=loan["remaining_tenure"],
            interest_rate=loan["interest_rate"],
            status=loan["status"],
        )

        response = LoanStatusResponse(
            loan_info=loan_info,
            next_payment_date=loan["next_emi_date"],
            status=Status.SUCCESS,
        )

        logger.info(
            f"Loan status retrieved from mock data for loan ID: {request.loan_id}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting loan status for loan ID {request.loan_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")
