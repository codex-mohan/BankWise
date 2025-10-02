from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
import random

from models import SpeakToAgentRequest, EscalationResponse, Status, AgentInfo
from services.agent_service import agent_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["escalation"])


@router.post("/escalate", response_model=EscalationResponse)
async def escalate_to_agent(request: SpeakToAgentRequest):
    """Escalate to human agent with intelligent agent selection"""
    try:
        logger.info(f"Escalation request received - Reason: {request.reason}, Urgency: {request.urgency}")

        # Generate escalation ID
        escalation_id = f"ESCALATION{random.randint(10000, 99999)}"
        
        # Determine specialization based on reason (if provided)
        specialization = None
        if request.reason:
            reason_lower = request.reason.lower()
            if any(keyword in reason_lower for keyword in ["card", "debit", "credit"]):
                specialization = "Card Issues"
            elif any(keyword in reason_lower for keyword in ["loan", "emi", "personal"]):
                specialization = "Loan Processing"
            elif any(keyword in reason_lower for keyword in ["account", "balance", "statement"]):
                specialization = "Account Queries"
            elif any(keyword in reason_lower for keyword in ["transaction", "dispute", "fraud"]):
                specialization = "Transaction Disputes"
            elif any(keyword in reason_lower for keyword in ["technical", "app", "online", "mobile"]):
                specialization = "Technical Support"
        
        # Get best available agent
        best_agent = agent_service.get_best_agent(specialization)
        
        if not best_agent:
            # No agents available immediately, get alternatives
            all_agents = agent_service.get_all_agents()
            if all_agents:
                # Find agent with shortest next available time
                soonest_available = None
                soonest_time = None
                
                for agent in all_agents:
                    if agent.next_available_time:
                        next_time = datetime.fromisoformat(agent.next_available_time.replace('Z', '+00:00'))
                        if soonest_time is None or next_time < soonest_time:
                            soonest_time = next_time
                            soonest_available = agent
                
                if soonest_available:
                    wait_minutes = max(1, int((soonest_time - datetime.now()).total_seconds() / 60))
                    alternative_agents = agent_service.get_alternative_agents(
                        soonest_available.agent_id, specialization, limit=3
                    )
                    
                    response = EscalationResponse(
                        escalation_id=escalation_id,
                        agent_info=soonest_available,
                        estimated_wait_time=wait_minutes,
                        queue_position=random.randint(1, 5),
                        alternative_agents=alternative_agents,
                        status=Status.SUCCESS,
                    )
                    
                    logger.info(f"Escalation queued with agent {soonest_available.full_name}, wait time: {wait_minutes} minutes")
                    return response
            
            # No agents at all
            raise HTTPException(status_code=503, detail="No agents are currently available. Please try again later.")
        
        # Agent is available immediately
        wait_time = random.randint(1, 5)  # Minimal wait for available agent
        alternative_agents = agent_service.get_alternative_agents(best_agent.agent_id, specialization, limit=3)
        
        # Update agent status to busy
        agent_service.update_agent_status(best_agent.agent_id, "Busy")
        
        response = EscalationResponse(
            escalation_id=escalation_id,
            agent_info=best_agent,
            estimated_wait_time=wait_time,
            queue_position=1,
            alternative_agents=alternative_agents,
            status=Status.SUCCESS,
        )

        logger.info(f"Escalation created successfully - Agent: {best_agent.full_name}, ID: {escalation_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing escalation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/agents/statistics")
async def get_agent_statistics():
    """Get statistics about agents and their availability"""
    try:
        stats = agent_service.get_agent_statistics()
        logger.info("Retrieved agent statistics")
        return stats
    except Exception as e:
        logger.error(f"Error retrieving agent statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/agents/available", response_model=list[AgentInfo])
async def get_available_agents(specialization: str = None, limit: int = 10):
    """Get list of available agents, optionally filtered by specialization"""
    try:
        agents = agent_service.get_available_agents(specialization, limit)
        logger.info(f"Retrieved {len(agents)} available agents for specialization: {specialization}")
        return agents
    except Exception as e:
        logger.error(f"Error retrieving available agents: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/agents/{agent_id}", response_model=AgentInfo)
async def get_agent_details(agent_id: str):
    """Get detailed information about a specific agent"""
    try:
        agent = agent_service.get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        logger.info(f"Retrieved details for agent: {agent_id}")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving agent details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/agents/{agent_id}/status")
async def update_agent_status(agent_id: str, status: str):
    """Update agent availability status"""
    try:
        valid_statuses = ["Available", "Busy", "On Break", "In Training", "Off Duty"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        success = agent_service.update_agent_status(agent_id, status)
        if not success:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        logger.info(f"Updated agent {agent_id} status to: {status}")
        return {"message": f"Agent status updated to {status}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
