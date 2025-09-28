from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging
import random

from models import (
    ChequeStatusRequest,
    ChequeStatusResponse,
    Status,
    ChequeTrackingEvent,
    ChequeTrackingRequest,
    ChequeTrackingResponse,
)
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
                try:
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
                            clearing_date=(
                                cheque["clearing_date"].isoformat()
                                if cheque["clearing_date"]
                                else None
                            ),
                            status=Status.SUCCESS,
                        )
                        logger.info(
                            f"Cheque status retrieved from database for cheque number: {request.cheque_number}"
                        )
                        return response
                except Exception as e:
                    logger.warning(f"Database query failed: {str(e)}")
                    # Proceed to mock data
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
            else:
                # Database connection failed, use mock data
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


@router.post("/track", response_model=ChequeTrackingResponse)
async def track_cheque(request: ChequeTrackingRequest):
    """Track a cheque's journey and current status"""
    try:
        logger.info(f"Cheque tracking request for cheque: {request.cheque_number}")

        # Try to get from database first
        async with db_manager.get_connection() as conn:
            if conn:
                try:
                    # Get cheque details from DB
                    cheque = await conn.fetchrow(
                        "SELECT * FROM cheques WHERE cheque_number = $1 AND account_number = $2",
                        request.cheque_number,
                        request.account_number,
                    )

                    if not cheque:
                        # Fallback to mock data
                        cheque = mock_storage.get_cheque_by_number(
                            request.cheque_number
                        )

                    if not cheque:
                        logger.warning(f"Cheque not found: {request.cheque_number}")
                        raise HTTPException(status_code=404, detail="Cheque not found")

                    # Convert DB row to dict if needed
                    cheque_data = (
                        dict(cheque)
                        if cheque and not isinstance(cheque, dict)
                        else cheque
                    )

                    # Get tracking events (from DB or mock data)
                    tracking_events = []
                    if hasattr(conn, "fetch"):
                        tracking_events = await conn.fetch(
                            "SELECT * FROM cheque_events WHERE cheque_number = $1 ORDER BY timestamp DESC",
                            request.cheque_number,
                        )

                    # Fallback to mock data if no DB events
                    if not tracking_events:
                        tracking_events = mock_storage.generate_cheque_tracking_events(
                            request.cheque_number
                        )

                    # Format response
                    response = ChequeTrackingResponse(
                        cheque_number=cheque_data["cheque_number"],
                        content=cheque_data["status"],
                        amount=cheque_data["amount"],
                        date=cheque_data["issue_date"],
                        clearing_date=cheque_data["clearing_date"],
                        current_location=(
                            tracking_events[0]["location"]
                            if tracking_events
                            else "Unknown"
                        ),
                        expected_clearing_date=cheque_data["clearing_date"]
                        or "Not available",
                        issuer=cheque_data["account_number"],
                        payee=cheque_data["payee_name"],
                        tracking_events=[
                            ChequeTrackingEvent(
                                event_type=event["event_type"],
                                description=event["description"],
                                timestamp=event["timestamp"],
                                location=event["location"],
                            )
                            for event in tracking_events
                        ],
                        status=Status.SUCCESS,
                    )

                    logger.info(
                        f"Cheque tracking details retrieved for {request.cheque_number}"
                    )
                    return response

                except HTTPException:
                    raise
    except Exception as e:
        logger.error(f"Error tracking cheque {request.cheque_number}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
