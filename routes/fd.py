from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging

from mock_data_storage import mock_storage
from database import db_manager
from models import FDRateInfoRequest, FDRate, FDRateInfoResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/fd", tags=["fd"])


@router.post("/rates", response_model=FDRateInfoResponse)
async def get_fd_rates(request: FDRateInfoRequest):
    """Get fixed deposit rates"""
    try:
        logger.info(f"FD rates request for tenure: {request.tenure}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                if request.tenure:
                    rate_records = await conn.fetch(
                        "SELECT * FROM fd_rates WHERE tenure = $1 ORDER BY customer_type",
                        request.tenure,
                    )
                else:
                    rate_records = await conn.fetch(
                        "SELECT * FROM fd_rates ORDER BY tenure, customer_type"
                    )

                if rate_records:
                    rate_list = []
                    for rate in rate_records:
                        rate_list.append(
                            FDRate(
                                tenure=rate["tenure"],
                                rate=float(rate["rate"]),
                                min_amount=float(rate["min_amount"]),
                                max_amount=float(rate["max_amount"]),
                                currency=rate["currency"],
                            )
                        )

                    response = FDRateInfoResponse(
                        rates=rate_list,
                        currency="INR",
                        last_updated=datetime.now().isoformat(),
                        status=Status.SUCCESS,
                    )

                    logger.info(f"FD rates retrieved from database")
                    return response

        # Fallback to mock data
        rates = mock_storage.get_fd_rates(request.tenure)

        rate_list = []
        for rate in rates:
            rate_list.append(
                FDRate(
                    tenure=rate["tenure"],
                    rate=rate["rate"],
                    min_amount=rate["min_amount"],
                    max_amount=rate["max_amount"],
                    currency=rate["currency"],
                )
            )

        response = FDRateInfoResponse(
            rates=rate_list,
            currency="INR",
            last_updated=datetime.now().isoformat(),
            status=Status.SUCCESS,
        )

        logger.info(f"FD rates retrieved from mock data")
        return response

    except Exception as e:
        logger.error(f"Error getting FD rates: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
