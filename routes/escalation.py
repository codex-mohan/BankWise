from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from models import SpeakToAgentRequest, EscalationResponse, Status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["escalation"])


@router.post("/escalate", response_model=EscalationResponse)
async def escalate_to_agent(request: SpeakToAgentRequest):
    """Escalate to human agent"""
    try:
        logger.info(f"Escalation request with urgency: {request.urgency}")

        escalation_id = f"ESCALATION{random.randint(10000, 99999)}"
        agent_id = f"AGENT{random.randint(100, 999)}"
        wait_time = random.randint(5, 30)

        response = EscalationResponse(
            escalation_id=escalation_id,
            agent_id=agent_id,
            estimated_wait_time=wait_time,
            status=Status.SUCCESS,
        )

        logger.info(f"Escalation created successfully with ID: {escalation_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing escalation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
