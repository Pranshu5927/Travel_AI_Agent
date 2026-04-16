"""
Booking Helper Agent - Priority 3
Responsible for assisting with hotel, flight, and activity bookings.
Uses LangGraph for deterministic booking flows.
"""

import logging
import json
from typing import Any, Dict, Optional, List
from datetime import datetime
from .base_agent import BaseAgent, AgentRole
from services.mcp_clients import (
    get_hotel_flight_client,
    get_weather_client
)

logger = logging.getLogger(__name__)


class BookingHelperAgent(BaseAgent):
    """
    Booking assistant agent.
    Searches for and helps with hotel, flight, and activity bookings.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="booking_helper_v1",
            role=AgentRole.BOOKING_HELPER,
            name="Booking Helper Agent"
        )
        self.hotel_client = get_hotel_flight_client()
        self.weather_client = get_weather_client()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process booking request.
        
        Input:
        {
            "action": str (search_hotels|search_flights|get_recommendations),
            "destination": str,
            "check_in": str,
            "check_out": str,
            "origin": str (for flights),
            "guests": int,
            "budget_tier": str,
            "preferences": Dict
        }
        
        Output:
        {
            "success": bool,
            "results": Dict,
            "recommendations": List,
            "error": Optional[str]
        }
        """
        
        action = input_data.get("action", "search_hotels")
        destination = input_data.get("destination")
        
        self.log_action(f"Processing booking action: {action}")
        
        try:
            if action == "search_hotels":
                return await self._search_hotels(input_data)
            elif action == "search_flights":
                return await self._search_flights(input_data)
            elif action == "get_recommendations":
                return await self._get_recommendations(input_data)
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}"
                }
        
        except Exception as e:
            logger.error(f"Booking error: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": None
            }
    
    async def _search_hotels(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Search for hotels."""
        
        required_fields = ["destination", "check_in", "check_out"]
        if not self.validate_input(required_fields, input_data):
            return {
                "success": False,
                "error": "Missing required fields for hotel search",
                "results": None
            }
        
        destination = input_data.get("destination")
        check_in = input_data.get("check_in")
        check_out = input_data.get("check_out")
        guests = input_data.get("guests", 2)
        budget_tier = input_data.get("budget_tier", "moderate")
        
        self.log_action(
            "Searching hotels",
            {
                "destination": destination,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "tier": budget_tier
            }
        )
        
        # Search hotels using MCP
        hotel_results = await self.hotel_client.search_hotels(
            destination=destination,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            budget_tier=budget_tier
        )
        
        # Get weather info for the stay
        weather = await self.weather_client.get_weather_forecast(destination)
        
        # Generate recommendations
        recommendations = self._generate_hotel_recommendations(
            hotel_results.get("hotels", []),
            input_data
        )
        
        return {
            "success": True,
            "results": {
                "hotels": hotel_results.get("hotels", []),
                "weather": weather.get("forecast", [])
            },
            "recommendations": recommendations,
            "metadata": {
                "destination": destination,
                "check_in": check_in,
                "check_out": check_out,
                "search_time": datetime.now().isoformat()
            }
        }
    
    async def _search_flights(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Search for flights."""
        
        required_fields = ["origin", "destination", "departure_date"]
        if not self.validate_input(required_fields, input_data):
            return {
                "success": False,
                "error": "Missing required fields for flight search",
                "results": None
            }
        
        origin = input_data.get("origin")
        destination = input_data.get("destination")
        departure_date = input_data.get("departure_date")
        return_date = input_data.get("return_date")
        passengers = input_data.get("passengers", 1)
        
        self.log_action(
            "Searching flights",
            {
                "origin": origin,
                "destination": destination,
                "departure": departure_date,
                "return": return_date,
                "passengers": passengers
            }
        )
        
        # Search flights using MCP
        flight_results = await self.hotel_client.search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            passengers=passengers
        )
        
        # Generate recommendations
        recommendations = self._generate_flight_recommendations(
            flight_results.get("flights", []),
            input_data
        )
        
        return {
            "success": True,
            "results": flight_results,
            "recommendations": recommendations,
            "metadata": {
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "search_time": datetime.now().isoformat()
            }
        }
    
    async def _get_recommendations(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized booking recommendations."""
        
        destination = input_data.get("destination")
        preferences = input_data.get("preferences", {})
        budget = input_data.get("budget")
        
        self.log_action("Generating booking recommendations")
        
        recommendations = {
            "hotels": self._recommend_hotels(destination, preferences, budget),
            "flights": self._recommend_flights(destination, preferences),
            "activities": self._recommend_activities(destination, preferences)
        }
        
        return {
            "success": True,
            "recommendations": recommendations,
            "metadata": {
                "destination": destination,
                "based_on": list(preferences.keys())
            }
        }
    
    def _generate_hotel_recommendations(
        self,
        hotels: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> List[str]:
        """Generate hotel booking recommendations."""
        recommendations = []
        
        if not hotels:
            recommendations.append("⚠️ No hotels found. Try different dates or adjust criteria.")
            return recommendations
        
        # Find best value option
        best_value = None
        best_score = 0
        
        for hotel in hotels:
            score = (hotel.get("rating", 0) / 5) / (hotel.get("price_per_night", 1) / 100)
            if score > best_score:
                best_score = score
                best_value = hotel
        
        if best_value:
            recommendations.append(
                f"✨ Best Value: {best_value.get('name')} - "
                f"${best_value.get('price_per_night')}/night, "
                f"{best_value.get('rating')} stars"
            )
        
        # Budget-friendly option
        cheapest = min(hotels, key=lambda x: x.get("price_per_night", 0))
        recommendations.append(
            f"💰 Budget Option: {cheapest.get('name')} - "
            f"${cheapest.get('price_per_night')}/night"
        )
        
        # Luxury option
        priciest = max(hotels, key=lambda x: x.get("price_per_night", 0))
        recommendations.append(
            f"👑 Premium Option: {priciest.get('name')} - "
            f"${priciest.get('price_per_night')}/night"
        )
        
        # General tips
        recommendations.append("💡 Book early for better rates")
        recommendations.append("💡 Check cancellation policies before booking")
        
        return recommendations
    
    def _generate_flight_recommendations(
        self,
        flights: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> List[str]:
        """Generate flight booking recommendations."""
        recommendations = []
        
        if not flights:
            recommendations.append("⚠️ No flights found. Try different dates.")
            return recommendations
        
        # Fastest option
        fastest = min(flights, key=lambda x: self._parse_duration(x.get("duration", "")))
        recommendations.append(
            f"⚡ Fastest: {fastest.get('airline')} - "
            f"{fastest.get('duration')} (${fastest.get('price')})"
        )
        
        # Cheapest option
        cheapest = min(flights, key=lambda x: x.get("price", float('inf')))
        recommendations.append(
            f"💰 Cheapest: {cheapest.get('airline')} - "
            f"${cheapest.get('price')} ({cheapest.get('stops')} stops)"
        )
        
        # Best rated
        best_rated = max(flights, key=lambda x: x.get("rating", 0))
        recommendations.append(
            f"⭐ Best Rated: {best_rated.get('airline')} - "
            f"{best_rated.get('rating')} stars (${best_rated.get('price')})"
        )
        
        # General tips
        recommendations.append("💡 Set price alerts for better deals")
        recommendations.append("💡 Book midweek for cheaper flights")
        
        return recommendations
    
    def _recommend_hotels(
        self,
        destination: str,
        preferences: Dict[str, Any],
        budget: Optional[float]
    ) -> List[str]:
        """Recommend hotels based on preferences."""
        return [
            f"🏨 Looking for luxury hotels near downtown {destination}",
            f"💼 Checking business-class hotels with amenities",
            f"🏖️ Searching for beach resorts if applicable",
            f"💡 Filtering by your preferred amenities"
        ]
    
    def _recommend_flights(
        self,
        destination: str,
        preferences: Dict[str, Any]
    ) -> List[str]:
        """Recommend flights based on preferences."""
        return [
            f"✈️ Searching direct flights to {destination}",
            f"💨 Checking for fastest routes",
            f"💰 Comparing prices across airlines",
            f"📅 Looking at flexible date options"
        ]
    
    def _recommend_activities(
        self,
        destination: str,
        preferences: Dict[str, Any]
    ) -> List[str]:
        """Recommend activities based on preferences."""
        activities = preferences.get("activities", [])
        
        recommendations = [
            f"🎭 Popular activities in {destination}:",
        ]
        
        if not activities:
            recommendations.extend([
                "  • Museums and historical sites",
                "  • Local food experiences",
                "  • Outdoor adventures",
                "  • Cultural experiences"
            ])
        
        return recommendations
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse duration string to minutes."""
        # Simple parser: "8h 30m" -> 510 minutes
        try:
            hours = int(duration_str.split('h')[0].strip()) if 'h' in duration_str else 0
            minutes = int(duration_str.split('m')[0].split('h')[1].strip()) if 'm' in duration_str else 0
            return hours * 60 + minutes
        except:
            return float('inf')
