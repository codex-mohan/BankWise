from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
import random

from mock_data_storage import mock_storage
from database import db_manager
from models import ATMLocatorRequest, ATM, ATMLocatorResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/atm", tags=["atm"])


@router.post("/locate", response_model=ATMLocatorResponse)
async def locate_atm(request: ATMLocatorRequest):
    """Locate ATMs by pincode"""
    try:
        logger.info(
            f"ATM locator request for pincode: {request.pincode}, limit: {request.limit}"
        )

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                atm_records = await conn.fetch(
                    "SELECT * FROM atms WHERE pincode = $1 ORDER BY bank_name LIMIT $2",
                    request.pincode,
                    request.limit,
                )

                if atm_records:
                    atm_list = []
                    for atm in atm_records:
                        # Calculate distance from pincode center (mock calculation)
                        distance = round(random.uniform(0.2, 8.0), 1)
                        atm_list.append(
                            ATM(
                                id=atm["atm_id"],
                                address=atm["address"],
                                city=atm["city"],
                                pincode=atm["pincode"],
                                bank_name=atm["bank_name"],
                                latitude=atm["latitude"],
                                longitude=atm["longitude"],
                                distance=distance,
                            )
                        )

                    response = ATMLocatorResponse(
                        atms=atm_list, total_count=len(atm_list), status=Status.SUCCESS
                    )

                    logger.info(
                        f"ATMs located from database for pincode: {request.pincode}"
                    )
                    return response

        # Fallback to mock data
        atms = mock_storage.get_atms_by_pincode(request.pincode, request.limit)

        if not atms:
            logger.warning(f"No ATMs found for pincode: {request.pincode}")
            raise HTTPException(
                status_code=404, detail="No ATMs found for the specified pincode"
            )

        atm_list = []
        for atm in atms:
            # Calculate distance from pincode center (mock calculation)
            distance = round(random.uniform(0.2, 8.0), 1)
            atm_list.append(
                ATM(
                    id=atm["id"],
                    address=atm["address"],
                    city=atm["city"],
                    pincode=atm["pincode"],
                    bank_name=atm["bank_name"],
                    latitude=atm["latitude"],
                    longitude=atm["longitude"],
                    distance=distance,
                )
            )

        response = ATMLocatorResponse(
            atms=atm_list, total_count=len(atm_list), status=Status.SUCCESS
        )

        logger.info(f"ATMs located from mock data for pincode: {request.pincode}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error locating ATMs for pincode {request.pincode}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
