from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
import logging

from main import get_session_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/accessibility", tags=["accessibility"])

class AccessibilityRequest(BaseModel):
    session_id: str
    action: str # "slower_speech" or "repeat_last_answer"

class AccessibilityResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any] = {}

@router.post("/")
async def handle_accessibility_request(request: AccessibilityRequest, session: Dict[str, Any] = Depends(get_session_data)):
    """Handle accessibility requests like slower speech or repeating the last answer"""
    try:
        logger.info(f"Accessibility request received: {request.action} for session {request.session_id}")

        if request.action == "slower_speech":
            # In a real voice application, this would trigger a change in the TTS settings.
            # For a chat-based demo, we can acknowledge the request.
            response_message = "I will speak slower."
            return AccessibilityResponse(status="success", message=response_message)

        elif request.action == "repeat_last_answer":
            last_response = session.get("last_response")
            if last_response:
                return AccessibilityResponse(status="success", message="Here is the last message again.", data=last_response)
            else:
                return AccessibilityResponse(status="success", message="There is no previous message to repeat.")

        else:
            raise HTTPException(status_code=400, detail="Invalid accessibility action")

    except Exception as e:
        logger.error(f"Error processing accessibility request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")