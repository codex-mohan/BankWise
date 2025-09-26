from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from mock_data_storage import mock_storage
from database import db_manager
from models import (
    ComplaintRequest,
    ComplaintStatusRequest,
    ComplaintResponse,
    Status,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/complaint", tags=["complaint"])


@router.post("/new", response_model=ComplaintResponse)
async def create_complaint(request: ComplaintRequest):
    """Create a new complaint"""
    try:
        logger.info(f"Complaint creation request for category: {request.category}")

        # Generate complaint ticket
        ticket_id = f"COMPLAINT{random.randint(10000, 99999)}"
        created_at = datetime.now()
        estimated_days = random.randint(3, 15)

        response = ComplaintResponse(
            ticket_id=ticket_id,
            content="OPEN",
            created_at=created_at.isoformat(),
            estimated_resolution_days=estimated_days,
            status=Status.SUCCESS,
        )

        logger.info(f"Complaint created successfully with ticket ID: {ticket_id}")
        return response

    except Exception as e:
        logger.error(f"Error creating complaint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/status", response_model=ComplaintResponse)
async def get_complaint_status(request: ComplaintStatusRequest):
    """Get complaint status"""
    try:
        logger.info(f"Complaint status request for ticket ID: {request.ticket_id}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                complaint = await conn.fetchrow(
                    "SELECT * FROM complaints WHERE ticket_id = $1", request.ticket_id
                )
                if complaint:
                    response = ComplaintResponse(
                        ticket_id=complaint["ticket_id"],
                        content=complaint["status"],
                        created_at=complaint["created_at"].isoformat(),
                        estimated_resolution_days=complaint[
                            "estimated_resolution_days"
                        ],
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Complaint status retrieved from database for ticket ID: {request.ticket_id}"
                    )
                    return response

        # Fallback to mock data
        complaint = mock_storage.get_complaint_by_id(request.ticket_id)
        if not complaint:
            logger.warning(f"Complaint not found with ticket ID: {request.ticket_id}")
            raise HTTPException(status_code=404, detail="Complaint not found")

        response = ComplaintResponse(
            ticket_id=complaint["ticket_id"],
            content=complaint["status"],
            created_at=complaint["created_at"],
            estimated_resolution_days=complaint["estimated_resolution_days"],
            status=Status.SUCCESS,
        )

        logger.info(
            f"Complaint status retrieved from mock data for ticket ID: {request.ticket_id}"
        )
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting complaint status for ticket ID {request.ticket_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")
