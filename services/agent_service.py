"""
Agent service for managing human agent data and operations
"""

import json
import os
import random
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from models import AgentInfo, Status

logger = logging.getLogger(__name__)


class AgentService:
    """Service for managing human agent data and operations"""
    
    def __init__(self, agents_file: str = "mock_data/agents.json"):
        self.agents_file = agents_file
        self.agents = []
        self.load_agents()
    
    def load_agents(self) -> None:
        """Load agents from JSON file or generate if doesn't exist"""
        try:
            if os.path.exists(self.agents_file):
                with open(self.agents_file, 'r', encoding='utf-8') as f:
                    self.agents = json.load(f)
                logger.info(f"Loaded {len(self.agents)} agents from {self.agents_file}")
            else:
                logger.warning(f"Agents file {self.agents_file} not found. Generating new agents...")
                self.generate_agents()
        except Exception as e:
            logger.error(f"Error loading agents: {e}")
            self.generate_agents()
    
    def generate_agents(self) -> None:
        """Generate new agents using the agent generator"""
        try:
            from generate_agents import AgentDataGenerator
            
            generator = AgentDataGenerator()
            self.agents = generator.generate_agents(count=25)
            generator.save_agents_to_json(self.agents_file)
            logger.info(f"Generated {len(self.agents)} new agents")
        except ImportError:
            logger.error("Could not import AgentDataGenerator. Creating minimal agent data.")
            self._create_minimal_agents()
        except Exception as e:
            logger.error(f"Error generating agents: {e}")
            self._create_minimal_agents()
    
    def _create_minimal_agents(self) -> None:
        """Create minimal agent data as fallback"""
        self.agents = []
        for i in range(10):
            agent = {
                "agent_id": f"AGENT{1000 + i}",
                "employee_id": f"EMP{10000 + i}",
                "full_name": f"Agent {i+1}",
                "department": "Customer Service",
                "specialization": "General Banking",
                "languages_spoken": ["English", "Hindi"],
                "years_experience": random.randint(1, 10),
                "performance_rating": round(random.uniform(3.5, 5.0), 1),
                "customer_satisfaction_rate": round(random.uniform(85, 98), 1),
                "current_status": "Available" if i < 5 else "Busy",
                "is_available": i < 5,
                "next_available_time": None,
                "average_response_time": random.randint(30, 120),
                "resolution_rate": round(random.uniform(85, 99), 1),
                "escalation_level": "L1"
            }
            self.agents.append(agent)
        
        # Save minimal agents
        os.makedirs(os.path.dirname(self.agents_file), exist_ok=True)
        with open(self.agents_file, 'w', encoding='utf-8') as f:
            json.dump(self.agents, f, indent=2)
    
    def get_available_agents(self, specialization: Optional[str] = None, limit: int = 5) -> List[AgentInfo]:
        """Get available agents, optionally filtered by specialization"""
        available_agents = []
        
        for agent_data in self.agents:
            if agent_data.get("is_available", False):
                if specialization is None or agent_data.get("specialization") == specialization:
                    available_agents.append(AgentInfo(**agent_data))
        
        # Sort by performance rating and satisfaction rate
        available_agents.sort(
            key=lambda x: (x.performance_rating, x.customer_satisfaction_rate), 
            reverse=True
        )
        
        return available_agents[:limit]
    
    def get_agent_by_id(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent by ID"""
        for agent_data in self.agents:
            if agent_data.get("agent_id") == agent_id:
                return AgentInfo(**agent_data)
        return None
    
    def get_all_agents(self) -> List[AgentInfo]:
        """Get all agents"""
        return [AgentInfo(**agent_data) for agent_data in self.agents]
    
    def update_agent_status(self, agent_id: str, new_status: str) -> bool:
        """Update agent status"""
        for agent in self.agents:
            if agent.get("agent_id") == agent_id:
                agent["current_status"] = new_status
                agent["is_available"] = new_status == "Available"
                
                # Calculate next available time if not available
                if new_status != "Available":
                    if new_status == "Busy":
                        minutes = random.randint(15, 60)
                    elif new_status == "On Break":
                        minutes = random.randint(10, 30)
                    elif new_status == "In Training":
                        hours = random.randint(1, 4)
                        minutes = hours * 60
                    else:  # Off Duty
                        minutes = random.randint(480, 1440)  # 8-24 hours
                    
                    next_available = datetime.now().timestamp() + (minutes * 60)
                    agent["next_available_time"] = datetime.fromtimestamp(next_available).isoformat()
                else:
                    agent["next_available_time"] = None
                
                # Save updated data
                self._save_agents()
                return True
        return False
    
    def _save_agents(self) -> None:
        """Save agents to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.agents_file), exist_ok=True)
            with open(self.agents_file, 'w', encoding='utf-8') as f:
                json.dump(self.agents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving agents: {e}")
    
    def get_best_agent(self, specialization: Optional[str] = None) -> Optional[AgentInfo]:
        """Get the best available agent based on performance metrics"""
        available_agents = self.get_available_agents(specialization, limit=1)
        return available_agents[0] if available_agents else None
    
    def get_alternative_agents(self, primary_agent_id: str, specialization: Optional[str] = None, limit: int = 3) -> List[AgentInfo]:
        """Get alternative agents excluding the primary agent"""
        available_agents = self.get_available_agents(specialization, limit=limit + 1)
        return [agent for agent in available_agents if agent.agent_id != primary_agent_id][:limit]
    
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get statistics about agents"""
        total_agents = len(self.agents)
        available_agents = len([a for a in self.agents if a.get("is_available", False)])
        
        dept_stats = {}
        specialization_stats = {}
        
        for agent in self.agents:
            dept = agent.get("department", "Unknown")
            specialization = agent.get("specialization", "Unknown")
            
            dept_stats[dept] = dept_stats.get(dept, 0) + 1
            specialization_stats[specialization] = specialization_stats.get(specialization, 0) + 1
        
        return {
            "total_agents": total_agents,
            "available_agents": available_agents,
            "availability_rate": round((available_agents / total_agents) * 100, 1) if total_agents > 0 else 0,
            "department_distribution": dept_stats,
            "specialization_distribution": specialization_stats
        }


# Global agent service instance
agent_service = AgentService()