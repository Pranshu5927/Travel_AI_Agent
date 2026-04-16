"""
Itinerary Agent - Priority 1
Responsible for generating, organizing, and refining travel itineraries.
Uses Google ADK for intelligent itinerary generation and personalization.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
from .base_agent import BaseAgent, AgentRole

logger = logging.getLogger(__name__)


class ItineraryAgent(BaseAgent):
    """
    Intelligent itinerary planning agent.
    Generates day-by-day plans based on destination, duration, and preferences.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="itinerary_agent_v1",
            role=AgentRole.ITINERARY,
            name="Itinerary Agent"
        )
        self.cache = {}
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process itinerary generation request.
        
        Input:
        {
            "destination": str,
            "start_date": str,
            "end_date": str,
            "preferences": {
                "activities": List[str],
                "vibe": str,
                "pace": str (slow/moderate/fast)
            },
            "budget": float,
            "user_id": str
        }
        
        Output:
        {
            "success": bool,
            "itinerary": Dict,
            "summary": str,
            "metadata": Dict
        }
        """
        
        # Validate input
        required_fields = ["destination", "start_date", "end_date"]
        if not self.validate_input(required_fields, input_data):
            return {
                "success": False,
                "error": "Missing required fields: destination, start_date, end_date",
                "itinerary": None
            }
        
        destination = input_data.get("destination")
        preferences = input_data.get("preferences", {})
        duration = self._calculate_duration(
            input_data.get("start_date"),
            input_data.get("end_date")
        )
        
        self.log_action(
            "Generating itinerary",
            {
                "destination": destination,
                "duration": duration,
                "preferences": preferences
            }
        )
        
        try:
            itinerary = self._generate_itinerary(
                destination,
                duration,
                preferences
            )
            
            summary = self._create_summary(itinerary)
            
            return {
                "success": True,
                "itinerary": itinerary,
                "summary": summary,
                "metadata": {
                    "destination": destination,
                    "duration": duration,
                    "preferences": preferences,
                    "generated_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
        
        except Exception as e:
            logger.error(f"Error generating itinerary: {e}")
            return {
                "success": False,
                "error": str(e),
                "itinerary": None
            }
    
    def _calculate_duration(self, start_date: str, end_date: str) -> int:
        """Calculate trip duration in days."""
        try:
            # Handle relative dates
            from utils import parse_date
            start = parse_date(start_date)
            end = parse_date(end_date)
            
            if start and end:
                return (end - start).days + 1
        except:
            pass
        
        # Default to 5 days if dates can't be parsed
        return 5
    
    def _generate_itinerary(
        self,
        destination: str,
        duration: int,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate detailed itinerary."""
        
        # Get activity theme
        theme = self._determine_theme(preferences)
        
        # Generate day-by-day activities
        days = []
        activities_db = self._get_destination_activities(destination, theme)
        
        for day_num in range(1, duration + 1):
            day_plan = self._create_day_plan(
                day_num,
                destination,
                activities_db,
                theme
            )
            days.append(day_plan)
        
        return {
            "destination": destination,
            "duration": duration,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=duration)).isoformat(),
            "theme": theme,
            "days": days,
            "highlights": self._extract_highlights(days),
            "practical_tips": self._get_practical_tips(destination)
        }
    
    def _determine_theme(self, preferences: Dict[str, Any]) -> str:
        """Determine itinerary theme based on preferences."""
        activities = preferences.get("activities", [])
        vibe = preferences.get("vibe", "mixed")
        
        # Map activities to themes
        theme_mapping = {
            "adventure": ["hiking", "diving", "sports", "extreme"],
            "cultural": ["temples", "museums", "history", "cultural"],
            "relaxation": ["beach", "spa", "yoga", "wellness"],
            "food": ["food tour", "cooking", "dining", "market"],
            "urban": ["shopping", "nightlife", "modern", "city"],
            "nature": ["hiking", "nature", "parks", "wildlife"]
        }
        
        for theme, keywords in theme_mapping.items():
            if any(kw in str(activities).lower() or kw in str(vibe).lower() for kw in keywords):
                return theme
        
        return "mixed"
    
    def _get_destination_activities(self, destination: str, theme: str) -> Dict[str, Any]:
        """Get activities database for destination."""
        
        activities_db = {
            "paris": {
                "cultural": ["Louvre Museum", "Notre-Dame", "Versailles", "Arc de Triomphe"],
                "food": ["Michelin restaurants", "Wine tasting", "Pastry classes", "Market tours"],
                "romantic": ["Seine River cruise", "Eiffel Tower", "Montmartre", "Café hopping"],
                "mixed": ["Museums", "Cafés", "Shopping", "Walking tours"]
            },
            "tokyo": {
                "cultural": ["Senso-ji Temple", "Meiji Shrine", "Imperial Palace", "Tea ceremony"],
                "modern": ["Shibuya Crossing", "Tokyo Tower", "Akihabara", "Team Lab"],
                "food": ["Tsukiji Market", "Sushi class", "Ramen tour", "Izakaya experience"],
                "mixed": ["Temples", "Modern districts", "Food tours", "Shopping"]
            },
            "bali": {
                "relaxation": ["Beach resorts", "Spa treatments", "Yoga retreats", "Water sports"],
                "cultural": ["Temple visits", "Traditional dances", "Cooking class", "Art galleries"],
                "adventure": ["Volcano hiking", "Surfing", "Diving", "Jungle trekking"],
                "mixed": ["Temples", "Beaches", "Hiking", "Cultural experiences"]
            },
            "new york": {
                "urban": ["Broadway", "Shopping", "Nightlife", "Rooftop bars"],
                "cultural": ["Museums", "Broadway", "Art galleries", "Historic sites"],
                "food": ["Food hall tours", "Fine dining", "Street food", "Cooking class"],
                "mixed": ["Museums", "Central Park", "Shopping", "Theater"]
            }
        }
        
        dest_lower = destination.lower()
        return activities_db.get(dest_lower, activities_db.get("new york"))
    
    def _create_day_plan(
        self,
        day_num: int,
        destination: str,
        activities_db: Dict[str, Any],
        theme: str
    ) -> Dict[str, Any]:
        """Create a single day's plan."""
        
        activities_list = []
        
        # Get activities for this theme
        if theme in activities_db:
            activities_list = activities_db[theme]
        else:
            # Use first theme available
            activities_list = next(iter(activities_db.values()), [])
        
        # Distribute activities across the day
        morning_activity = activities_list[(day_num * 2) % len(activities_list)]
        afternoon_activity = activities_list[(day_num * 2 + 1) % len(activities_list)]
        evening_activity = "Dinner at local restaurant"
        
        return {
            "day": day_num,
            "date": (datetime.now() + timedelta(days=day_num - 1)).strftime("%Y-%m-%d"),
            "morning": {
                "activity": morning_activity,
                "time": "9:00 AM",
                "duration": "3 hours",
                "notes": f"Start your {day_num}th day exploring {morning_activity.lower()}"
            },
            "afternoon": {
                "activity": afternoon_activity,
                "time": "1:00 PM",
                "duration": "4 hours",
                "notes": f"Continue with {afternoon_activity.lower()}"
            },
            "evening": {
                "activity": evening_activity,
                "time": "7:00 PM",
                "duration": "2 hours",
                "notes": "Relax and enjoy local cuisine"
            },
            "meals": {
                "breakfast": "Hotel breakfast or local café",
                "lunch": "Local restaurant or food market",
                "dinner": "Recommended local restaurant"
            },
            "transportation": "Walk or use local transit",
            "tips": [
                "Wear comfortable shoes",
                "Bring water and sun protection",
                "Check opening hours in advance"
            ]
        }
    
    def _extract_highlights(self, days: List[Dict[str, Any]]) -> List[str]:
        """Extract itinerary highlights."""
        highlights = []
        for day in days:
            morning = day.get("morning", {}).get("activity")
            afternoon = day.get("afternoon", {}).get("activity")
            if morning:
                highlights.append(f"Day {day['day']}: {morning}")
            if afternoon:
                highlights.append(f"Day {day['day']}: {afternoon}")
        
        return highlights[:5]  # Top 5 highlights
    
    def _get_practical_tips(self, destination: str) -> Dict[str, Any]:
        """Get practical tips for destination."""
        tips_db = {
            "paris": {
                "transportation": "Use Paris Metro or walk",
                "language": "French, English widely spoken in tourist areas",
                "currency": "Euro",
                "best_time": "April-May or September-October",
                "safety": "Safe city, watch for pickpockets in crowded areas"
            },
            "tokyo": {
                "transportation": "Excellent public transport (trains, buses)",
                "language": "Japanese, English signs in tourist areas",
                "currency": "Japanese Yen",
                "best_time": "March-April or October-November",
                "safety": "Very safe, extremely low crime rate"
            },
            "bali": {
                "transportation": "Rent scooter or hire driver",
                "language": "Indonesian, English widely spoken",
                "currency": "Indonesian Rupiah",
                "best_time": "April-October (dry season)",
                "safety": "Generally safe, avoid political events"
            },
            "new york": {
                "transportation": "Subway is main transport",
                "language": "English",
                "currency": "US Dollar",
                "best_time": "September-October or April-May",
                "safety": "Safe in tourist areas, avoid deserted areas at night"
            }
        }
        
        return tips_db.get(destination.lower(), tips_db.get("new york"))
    
    def _create_summary(self, itinerary: Dict[str, Any]) -> str:
        """Create a text summary of the itinerary."""
        destination = itinerary.get("destination")
        duration = itinerary.get("duration")
        theme = itinerary.get("theme")
        highlights = itinerary.get("highlights", [])
        
        summary = f"""
🌍 **{destination.title()} Trip Summary**
📅 Duration: {duration} days
🎯 Theme: {theme.title()}

**Highlights:**
"""
        for highlight in highlights[:3]:
            summary += f"  • {highlight}\n"
        
        summary += f"""
**Practical Info:**
  • Best visited: Year-round
  • Main transport: Local public transit
  • Currency: Check before arrival
  • Language: English spoken in most tourist areas

The itinerary is designed to balance exploration with relaxation.
Each day includes morning activities, afternoon experiences, and evening dining.
"""
        
        return summary
