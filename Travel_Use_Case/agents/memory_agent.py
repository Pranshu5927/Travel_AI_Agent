"""
Memory & Personalization Agent - Priority 4
Responsible for remembering user preferences and personalizing recommendations.
"""

import logging
from typing import Any, Dict, Optional, List
from .base_agent import BaseAgent, AgentRole
from services.session_memory import get_memory_service, get_session_manager
from services.callbacks import get_event_logger

logger = logging.getLogger(__name__)


class MemoryPersonalizationAgent(BaseAgent):
    """
    Memory and personalization agent.
    Learns user preferences and provides personalized recommendations.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="memory_personalization_v1",
            role=AgentRole.MEMORY,
            name="Memory & Personalization Agent"
        )
        self.memory_service = get_memory_service()
        self.session_manager = get_session_manager()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process memory and personalization request.
        
        Input:
        {
            "action": str (save_preferences|load_preferences|get_personalized_recommendations),
            "user_id": str,
            "preferences": Dict (optional),
            "destination": str (optional),
            "context": Dict (optional)
        }
        
        Output:
        {
            "success": bool,
            "preferences": Dict,
            "recommendations": List,
            "memory_score": float,
            "error": Optional[str]
        }
        """
        
        action = input_data.get("action", "load_preferences")
        user_id = input_data.get("user_id")
        
        if not user_id:
            return {
                "success": False,
                "error": "user_id is required"
            }
        
        self.log_action(f"Processing memory action: {action}", {"user_id": user_id})
        
        try:
            if action == "save_preferences":
                return await self._save_preferences(user_id, input_data)
            elif action == "load_preferences":
                return await self._load_preferences(user_id)
            elif action == "get_personalized_recommendations":
                return await self._get_personalized_recommendations(user_id, input_data)
            elif action == "update_session":
                return await self._update_session(user_id, input_data)
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
        
        except Exception as e:
            logger.error(f"Memory error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _save_preferences(
        self,
        user_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save user preferences."""
        
        preferences = input_data.get("preferences", {})
        
        # Save to memory service
        self.memory_service.save_user_preferences(user_id, preferences)
        
        # Log event
        event_logger = get_event_logger(user_id)
        event_logger.log_event("preferences_saved", {
            "preferences": preferences,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        })
        
        self.log_action("User preferences saved", {"user_id": user_id})
        
        return {
            "success": True,
            "preferences": preferences,
            "message": "Preferences saved successfully",
            "metadata": {
                "user_id": user_id,
                "action": "save_preferences"
            }
        }
    
    async def _load_preferences(self, user_id: str) -> Dict[str, Any]:
        """Load user preferences."""
        
        preferences = self.memory_service.load_user_preferences(user_id)
        
        if not preferences:
            preferences = self._get_default_preferences()
        
        # Calculate memory score (how much we know about this user)
        memory_score = self._calculate_memory_score(preferences)
        
        self.log_action("User preferences loaded", {"user_id": user_id})
        
        return {
            "success": True,
            "preferences": preferences,
            "memory_score": memory_score,
            "is_new_user": preferences == self._get_default_preferences(),
            "metadata": {
                "user_id": user_id,
                "action": "load_preferences"
            }
        }
    
    async def _get_personalized_recommendations(
        self,
        user_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get personalized recommendations based on user history."""
        
        # Load user preferences
        preferences = self.memory_service.load_user_preferences(user_id)
        if not preferences:
            preferences = self._get_default_preferences()
        
        destination = input_data.get("destination")
        context = input_data.get("context", {})
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            user_id,
            preferences,
            destination,
            context
        )
        
        self.log_action(
            "Generated personalized recommendations",
            {
                "user_id": user_id,
                "destination": destination,
                "rec_count": len(recommendations)
            }
        )
        
        return {
            "success": True,
            "recommendations": recommendations,
            "preferences": preferences,
            "personalization_level": "high" if preferences != self._get_default_preferences() else "low",
            "metadata": {
                "user_id": user_id,
                "destination": destination,
                "action": "get_personalized_recommendations"
            }
        }
    
    async def _update_session(
        self,
        user_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update user session."""
        
        updates = input_data.get("updates", {})
        
        # Get or create session
        session = self.session_manager.get_session(user_id)
        
        # Update session
        self.session_manager.update_session(user_id, updates)
        
        # Log event
        event_logger = get_event_logger(user_id)
        event_logger.log_event("session_updated", {
            "updates": updates,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        })
        
        self.log_action("Session updated", {"user_id": user_id})
        
        return {
            "success": True,
            "session": self.session_manager.get_session(user_id),
            "message": "Session updated successfully",
            "metadata": {
                "user_id": user_id,
                "action": "update_session"
            }
        }
    
    def _generate_recommendations(
        self,
        user_id: str,
        preferences: Dict[str, Any],
        destination: Optional[str],
        context: Dict[str, Any]
    ) -> List[str]:
        """Generate personalized recommendations."""
        
        recommendations = []
        
        # Get user's favorite destinations
        fav_destinations = preferences.get("favorite_destinations", [])
        
        # Activity preferences
        activity_prefs = preferences.get("travel_preferences", {}).get("activities", [])
        
        # Budget preference
        budget_pref = preferences.get("budget_preference", "moderate")
        
        # Generate recommendations
        if activity_prefs:
            recommendations.append(
                f"🎯 Based on your interest in {', '.join(activity_prefs[:2])}, "
                f"we recommend activities matching your style"
            )
        
        if fav_destinations:
            recommendations.append(
                f"❤️ Since you enjoyed {fav_destinations[0]}, "
                f"you might like similar destinations"
            )
        
        if destination and fav_destinations:
            if destination.lower() in [d.lower() for d in fav_destinations]:
                recommendations.append(
                    f"🌟 Welcome back to {destination}! "
                    f"We've remembered your preferences from last time"
                )
        
        # Budget-based recommendations
        if budget_pref == "budget":
            recommendations.append(
                "💡 Showing you budget-friendly options and local experiences"
            )
        elif budget_pref == "luxury":
            recommendations.append(
                "👑 Curating premium experiences and exclusive activities"
            )
        
        # Default recommendations if no preferences
        if not recommendations:
            recommendations = [
                "🌍 Explore destinations based on your interests",
                "💡 Tell us your preferences to get better recommendations",
                "📍 Share your favorite destinations to get similar suggestions"
            ]
        
        return recommendations
    
    def _calculate_memory_score(self, preferences: Dict[str, Any]) -> float:
        """Calculate how much we know about the user (0.0 - 1.0)."""
        
        score = 0.0
        max_score = 0.0
        
        # Score components
        components = {
            "name": 0.1,
            "travel_preferences": 0.3,
            "favorite_destinations": 0.3,
            "budget_preference": 0.2
        }
        
        for key, weight in components.items():
            max_score += weight
            if key in preferences and preferences[key]:
                score += weight
        
        # Normalize to 0-1
        return score / max_score if max_score > 0 else 0.0
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences for new users."""
        return {
            "name": "",
            "travel_preferences": {
                "activities": [],
                "vibe": "mixed",
                "pace": "moderate"
            },
            "favorite_destinations": [],
            "budget_preference": "moderate"
        }
    
    async def learn_from_interactions(
        self,
        user_id: str,
        interactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Learn and update preferences based on user interactions."""
        
        preferences = self.memory_service.load_user_preferences(user_id)
        if not preferences:
            preferences = self._get_default_preferences()
        
        # Analyze interactions to update preferences
        for interaction in interactions:
            event_type = interaction.get("type")
            
            if event_type == "destination_visited":
                dest = interaction.get("destination")
                if dest and dest not in preferences["favorite_destinations"]:
                    preferences["favorite_destinations"].append(dest)
            
            elif event_type == "activity_preference":
                activity = interaction.get("activity")
                if activity and activity not in preferences["travel_preferences"]["activities"]:
                    preferences["travel_preferences"]["activities"].append(activity)
            
            elif event_type == "budget_preference_changed":
                preferences["budget_preference"] = interaction.get("budget_tier", "moderate")
        
        # Save updated preferences
        self.memory_service.save_user_preferences(user_id, preferences)
        
        self.log_action("Preferences updated from interactions", {"user_id": user_id})
        
        return {
            "success": True,
            "preferences": preferences,
            "message": "Preferences updated based on your history"
        }
