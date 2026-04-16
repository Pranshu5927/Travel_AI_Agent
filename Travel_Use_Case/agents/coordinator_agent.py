"""
Destination Research Agent & Coordinator Agent
Handles destination research and orchestrates other agents.
"""

import logging
from typing import Any, Dict, Optional, List
from .base_agent import BaseAgent, AgentRole
from skills.travel_skills import DestinationMatchingSkill

logger = logging.getLogger(__name__)


class DestinationResearchAgent(BaseAgent):
    """
    Destination research agent.
    Provides information about destinations and helps with destination selection.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="destination_research_v1",
            role=AgentRole.DESTINATION_RESEARCH,
            name="Destination Research Agent"
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process destination research request.
        
        Input:
        {
            "action": str (search|recommend|get_info),
            "destination": str (optional),
            "preferences": Dict (optional),
            "keywords": List[str] (optional)
        }
        
        Output:
        {
            "success": bool,
            "results": Dict,
            "recommendations": List,
            "error": Optional[str]
        }
        """
        
        action = input_data.get("action", "recommend")
        
        self.log_action(f"Processing destination research: {action}")
        
        try:
            if action == "search":
                return await self._search_destinations(input_data)
            elif action == "recommend":
                return await self._recommend_destinations(input_data)
            elif action == "get_info":
                return await self._get_destination_info(input_data)
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
        
        except Exception as e:
            logger.error(f"Destination research error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _search_destinations(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Search destinations."""
        keywords = input_data.get("keywords", [])
        
        # Search in destination database
        results = []
        
        destinations_db = DestinationMatchingSkill.DESTINATIONS_DB
        
        for dest, info in destinations_db.items():
            match_score = 0
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # Check in activities
                if keyword_lower in str(info.get("activities", [])).lower():
                    match_score += 2
                
                # Check in vibe
                if keyword_lower in str(info.get("vibe", [])).lower():
                    match_score += 2
                
                # Check in attractions
                if keyword_lower in str(info.get("attractions", [])).lower():
                    match_score += 1
            
            if match_score > 0:
                results.append({
                    "destination": dest,
                    "score": match_score,
                    "info": info
                })
        
        # Sort by score
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        
        self.log_action("Destination search complete", {"results_found": len(results)})
        
        return {
            "success": True,
            "results": results,
            "search_terms": keywords,
            "total_found": len(results)
        }
    
    async def _recommend_destinations(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend destinations based on preferences."""
        preferences = input_data.get("preferences", {})
        num_results = input_data.get("num_results", 5)
        
        matches = DestinationMatchingSkill.match_destinations(
            preferences,
            num_results=num_results
        )
        
        self.log_action(
            "Destination recommendations generated",
            {"count": len(matches)}
        )
        
        return {
            "success": True,
            "recommendations": matches,
            "preferences_used": preferences,
            "metadata": {
                "algorithm": "preference_matching",
                "total_scored": len(DestinationMatchingSkill.DESTINATIONS_DB)
            }
        }
    
    async def _get_destination_info(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed information about a destination."""
        destination = input_data.get("destination")
        
        if not destination:
            return {
                "success": False,
                "error": "destination is required"
            }
        
        destinations_db = DestinationMatchingSkill.DESTINATIONS_DB
        dest_info = destinations_db.get(destination.lower())
        
        if not dest_info:
            return {
                "success": False,
                "error": f"Destination not found: {destination}",
                "suggestions": list(destinations_db.keys())
            }
        
        # Enrich with additional info
        enriched_info = {
            **dest_info,
            "tips": self._get_travel_tips(destination),
            "best_time": dest_info.get("best_months", []),
            "avg_temperature": dest_info.get("weather_avg_temp", "N/A")
        }
        
        self.log_action(
            "Destination information retrieved",
            {"destination": destination}
        )
        
        return {
            "success": True,
            "destination": destination,
            "information": enriched_info,
            "metadata": {
                "retrieved_at": __import__("datetime").datetime.now().isoformat()
            }
        }
    
    def _get_travel_tips(self, destination: str) -> List[str]:
        """Get travel tips for destination."""
        tips_db = {
            "paris": [
                "Visit the Louvre on Thursday for extended hours",
                "Buy a carnet of 10 metro tickets for savings",
                "Street food and markets offer good value",
                "Learn basic French phrases",
                "Book reservations at popular restaurants in advance"
            ],
            "tokyo": [
                "Get a Suica card for easy transportation",
                "Convenience stores have excellent food options",
                "Many temples and shrines are free",
                "Public transit is very reliable",
                "Respect local customs and etiquette"
            ],
            "bali": [
                "Rent a scooter for flexibility",
                "Visit temples early to avoid crowds",
                "Try local warungs for authentic food",
                "Bargain respectfully at markets",
                "Respect temple etiquette (sarongs required)"
            ],
            "new york": [
                "Use the subway to navigate efficiently",
                "Pizza slices are great budget meals",
                "Many museums have pay-what-you-wish hours",
                "Walk the streets to discover neighborhoods",
                "Book theater tickets in advance"
            ]
        }
        
        return tips_db.get(destination.lower(), [
            "Check local customs before visiting",
            "Book accommodations in advance",
            "Get travel insurance",
            "Learn key phrases in local language"
        ])


class CoordinatorAgent(BaseAgent):
    """
    Coordinator agent.
    Orchestrates all other agents and manages the planning workflow.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="coordinator_v1",
            role=AgentRole.COORDINATOR,
            name="Coordinator Agent"
        )
        self.agents = {}  # Will be populated after other agents are created
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate agent workflow.
        
        Input:
        {
            "user_input": str,
            "user_id": str,
            "session_state": Dict
        }
        
        Output:
        {
            "success": bool,
            "response": str,
            "actions_taken": List,
            "state_updates": Dict,
            "error": Optional[str]
        }
        """
        
        user_id = input_data.get("user_id")
        user_input = input_data.get("user_input")
        session_state = input_data.get("session_state", {})
        
        self.log_action(
            "Orchestrating trip planning workflow",
            {"user_id": user_id, "input": user_input[:50]}
        )
        
        try:
            # Determine what actions to take based on user input
            plan = await self._determine_plan(user_input, session_state)
            
            # Execute plan
            result = await self._execute_plan(plan, input_data)
            
            return result
        
        except Exception as e:
            logger.error(f"Coordination error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "An error occurred while planning. Please try again."
            }
    
    async def _determine_plan(
        self,
        user_input: str,
        session_state: Dict[str, Any]
    ) -> List[str]:
        """Determine which agents to invoke."""
        
        plan = []
        user_input_lower = user_input.lower()
        
        # Analyze user input to determine plan
        
        # Check for destination-related requests
        if any(word in user_input_lower for word in ["where", "destination", "city", "country"]):
            plan.append("destination_research")
        
        # Check for itinerary-related requests
        if any(word in user_input_lower for word in ["plan", "itinerary", "activities", "things to do"]):
            plan.append("itinerary")
        
        # Check for budget-related requests
        if any(word in user_input_lower for word in ["budget", "cost", "price", "afford", "expensive"]):
            plan.append("budget")
        
        # Check for booking-related requests
        if any(word in user_input_lower for word in ["book", "hotel", "flight", "accommodation", "book"]):
            plan.append("booking")
        
        # Always use memory for personalization
        plan.append("memory")
        
        # Default to comprehensive planning
        if not plan:
            plan = ["memory", "destination_research", "itinerary", "budget"]
        
        self.log_action("Plan determined", {"agents": plan})
        return plan
    
    async def _execute_plan(
        self,
        plan: List[str],
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the determined plan."""
        
        actions_taken = []
        state_updates = {}
        all_results = {}
        
        for agent_name in plan:
            # Map agent names to actual agent calls
            # In a real implementation, would call actual agent instances
            
            actions_taken.append(f"Invoke {agent_name} agent")
        
        response = self._generate_response(plan, all_results, input_data)
        
        return {
            "success": True,
            "response": response,
            "actions_taken": actions_taken,
            "state_updates": state_updates,
            "metadata": {
                "plan_executed": plan,
                "agents_used": len(plan)
            }
        }
    
    def _generate_response(
        self,
        plan: List[str],
        results: Dict[str, Any],
        input_data: Dict[str, Any]
    ) -> str:
        """Generate conversational response."""
        
        destination = input_data.get("destination", "your destination")
        
        response = f"""🌍 **Trip Planning Assistant**

I'll help you plan an amazing trip to {destination}!

Based on your request, I'm analyzing:
"""
        
        if "destination_research" in plan:
            response += "\n  ✓ Destination options and information"
        if "itinerary" in plan:
            response += "\n  ✓ Day-by-day itinerary planning"
        if "budget" in plan:
            response += "\n  ✓ Budget estimation and breakdown"
        if "booking" in plan:
            response += "\n  ✓ Hotel, flight, and activity recommendations"
        if "memory" in plan:
            response += "\n  ✓ Your preferences and past travels"
        
        response += """

Please provide more details about:
  • Travel dates (when are you planning to go?)
  • Budget (what's your budget range?)
  • Interests (what activities do you enjoy?)
  • Trip duration (how many days?)

I'll create a personalized itinerary once I have this information!
"""
        
        return response
