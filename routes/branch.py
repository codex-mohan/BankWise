from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
import random

from mock_data_storage import mock_storage
from database import db_manager
from models import BranchLocatorRequest, Branch, BranchLocatorResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/branch", tags=["branch"])


@router.post("/locate", response_model=BranchLocatorResponse)
async def locate_branch(request: BranchLocatorRequest):
    """Locate branches in a city"""
    try:
        logger.info(
            f"Branch locator request for city: {request.branch_city}, limit: {request.limit}"
        )

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                branch_records = await conn.fetch(
                    "SELECT * FROM branches WHERE city ILIKE $1 ORDER BY name LIMIT $2",
                    f"%{request.branch_city}%",
                    request.limit,
                )

                if branch_records:
                    branch_list = []
                    for branch in branch_records:
                        # Calculate distance from city center (mock calculation)
                        distance = round(random.uniform(0.5, 15.0), 1)
                        branch_list.append(
                            Branch(
                                name=branch["name"],
                                address=branch["address"],
                                city=branch["city"],
                                pincode=branch["pincode"],
                                ifsc=branch["ifsc"],
                                latitude=branch["latitude"],
                                longitude=branch["longitude"],
                                distance=distance,
                            )
                        )

                    response = BranchLocatorResponse(
                        branches=branch_list,
                        total_count=len(branch_list),
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Branches located from database in city: {request.branch_city}"
                    )
                    return response

        # Fallback to mock data
        branches = mock_storage.get_branches_by_city(request.branch_city, request.limit)

        if not branches:
            logger.warning(f"No branches found in city: {request.branch_city}")
            raise HTTPException(
                status_code=404, detail="No branches found in the specified city"
            )

        branch_list = []
        for branch in branches:
            # Calculate distance from city center (mock calculation)
            distance = round(random.uniform(0.5, 15.0), 1)
            branch_list.append(
                Branch(
                    name=branch["name"],
                    address=branch["address"],
                    city=branch["city"],
                    pincode=branch["pincode"],
                    ifsc=branch["ifsc"],
                    latitude=branch["latitude"],
                    longitude=branch["longitude"],
                    distance=distance,
                )
            )

        response = BranchLocatorResponse(
            branches=branch_list, total_count=len(branch_list), status=Status.SUCCESS
        )

        logger.info(f"Branches located from mock data in city: {request.branch_city}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error locating branches in city {request.branch_city}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
