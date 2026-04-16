"""
Base Agent class and utilities for Google ADK agents.
"""

import logging
from typing import Any, Dict, Optional, List
from abc import ABC, abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent roles in the system."""
    COORDINATOR = "coordinator"
    DESTINATION_RESEARCH = "destination_research"
    ITINERARY = "itinerary"
    BUDGET = "budget"
    BOOKING_HELPER = "booking_helper"
    MEMORY = "memory"


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, agent_id: str, role: AgentRole, name: str):
        self.agent_id = agent_id
        self.role = role
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return output."""
        pass
    
    def validate_input(self, required_fields: List[str], data: Dict[str, Any]) -> bool:
        """Validate input has required fields."""
        missing = [f for f in required_fields if f not in data or data[f] is None]
        if missing:
            self.logger.error(f"Missing required fields: {missing}")
            return False
        return True
    
    def log_action(self, action: str, details: Dict[str, Any] = None):
        """Log agent action."""
        msg = f"[{self.name}] {action}"
        if details:
            msg += f" - {details}"
        self.logger.info(msg)


class AgentChain:
    """Chain multiple agents together."""
    
    def __init__(self, agents: List[BaseAgent], name: str = "AgentChain"):
        self.agents = agents
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
    
    async def execute(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute chain of agents."""
        result = initial_input
        
        for agent in self.agents:
            self.logger.info(f"Executing {agent.name}")
            try:
                result = await agent.process(result)
                if not result.get("success", True):
                    self.logger.error(f"Agent {agent.name} failed: {result.get('error')}")
                    break
            except Exception as e:
                self.logger.error(f"Error in {agent.name}: {e}")
                result["success"] = False
                result["error"] = str(e)
                break
        
        return result


# Agent registry
_agent_registry: Dict[str, BaseAgent] = {}


def register_agent(agent: BaseAgent):
    """Register an agent."""
    _agent_registry[agent.agent_id] = agent
    logger.info(f"Agent registered: {agent.name} ({agent.agent_id})")


def get_agent(agent_id: str) -> Optional[BaseAgent]:
    """Get a registered agent."""
    return _agent_registry.get(agent_id)


def list_agents() -> Dict[str, BaseAgent]:
    """List all registered agents."""
    return _agent_registry.copy()
