"""
Reusable Skills for Travel Planning.
Skills are domain-specific functions that agents can use.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class BudgetTier(Enum):
    """Budget classification."""
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class BudgetEstimationSkill:
    """Estimate trip costs and create budget breakdown."""
    
    # Cost estimates per day (USD)
    COST_ESTIMATES = {
        "accommodation": {
            "budget": 30,
            "moderate": 80,
            "luxury": 200
        },
        "food": {
            "budget": 15,
            "moderate": 40,
            "luxury": 100
        },
        "activities": {
            "budget": 20,
            "moderate": 60,
            "luxury": 150
        },
        "transport": {
            "budget": 10,
            "moderate": 25,
            "luxury": 50
        }
    }
    
    DESTINATION_MULTIPLIERS = {
        "tokyo": 1.8,
        "paris": 1.9,
        "london": 1.8,
        "new york": 2.0,
        "dubai": 1.5,
        "bali": 0.4,
        "bangkok": 0.5,
        "mexico city": 0.6
    }
    
    @staticmethod
    def estimate_budget(
        destination: str,
        duration: int,
        tier: str = "moderate"
    ) -> Dict[str, Any]:
        """
        Estimate total budget needed for a trip.
        
        Args:
            destination: Trip destination
            duration: Number of days
            tier: Budget tier (budget, moderate, luxury)
        
        Returns:
            Budget breakdown and total
        """
        multiplier = BudgetEstimationSkill.DESTINATION_MULTIPLIERS.get(
            destination.lower(), 1.0
        )
        
        breakdown = {}
        total = 0
        
        for category, costs in BudgetEstimationSkill.COST_ESTIMATES.items():
            daily_cost = costs.get(tier, 50) * multiplier
            category_total = daily_cost * duration
            breakdown[category] = {
                "daily": round(daily_cost, 2),
                "total": round(category_total, 2)
            }
            total += category_total
        
        breakdown["total"] = round(total, 2)
        breakdown["tier"] = tier
        breakdown["duration"] = duration
        breakdown["destination"] = destination
        
        logger.info(f"Budget estimated for {destination}: ${total:.2f}")
        return breakdown
    
    @staticmethod
    def validate_budget(
        budget: float,
        destination: str,
        duration: int
    ) -> Dict[str, Any]:
        """Check if budget is sufficient."""
        estimated = BudgetEstimationSkill.estimate_budget(destination, duration, "budget")
        minimum = estimated["total"]
        
        is_feasible = budget >= minimum
        
        return {
            "is_feasible": is_feasible,
            "budget_provided": budget,
            "minimum_recommended": minimum,
            "difference": budget - minimum,
            "percentage_sufficient": (budget / minimum * 100) if minimum > 0 else 0,
            "recommendation": "Budget is sufficient" if is_feasible else f"Consider increasing budget by ${minimum - budget:.2f}"
        }


class DestinationMatchingSkill:
    """Match destinations to user preferences."""
    
    DESTINATIONS_DB = {
        "paris": {
            "country": "France",
            "region": "Europe",
            "best_months": ["April", "May", "September", "October"],
            "attractions": ["Eiffel Tower", "Louvre", "Notre-Dame", "Arc de Triomphe"],
            "activities": ["Museums", "Dining", "Shopping", "Walking Tours"],
            "vibe": ["Romantic", "Cultural", "Historic"],
            "weather_avg_temp": 15
        },
        "tokyo": {
            "country": "Japan",
            "region": "Asia",
            "best_months": ["March", "April", "October", "November"],
            "attractions": ["Senso-ji", "Tokyo Tower", "Shibuya", "Imperial Palace"],
            "activities": ["Temples", "Shopping", "Food Tours", "Cherry Blossom Viewing"],
            "vibe": ["Modern", "Traditional", "Energetic"],
            "weather_avg_temp": 15
        },
        "bali": {
            "country": "Indonesia",
            "region": "Southeast Asia",
            "best_months": ["April", "May", "June", "September"],
            "attractions": ["Temples", "Rice Terraces", "Beaches", "Volcanoes"],
            "activities": ["Beach", "Hiking", "Yoga", "Surfing"],
            "vibe": ["Relaxing", "Spiritual", "Beach"],
            "weather_avg_temp": 28
        },
        "new york": {
            "country": "USA",
            "region": "North America",
            "best_months": ["September", "October", "April", "May"],
            "attractions": ["Statue of Liberty", "Central Park", "Times Square", "Empire State Building"],
            "activities": ["Museums", "Theater", "Shopping", "Food"],
            "vibe": ["Urban", "Energetic", "Diverse"],
            "weather_avg_temp": 15
        }
    }
    
    @staticmethod
    def match_destinations(
        preferences: Dict[str, Any],
        num_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Match destinations based on user preferences.
        
        Args:
            preferences: User preferences (activities, vibe, budget, etc.)
            num_results: Number of results to return
        
        Returns:
            List of matched destinations
        """
        matches = []
        
        for dest, info in DestinationMatchingSkill.DESTINATIONS_DB.items():
            score = 0
            
            # Score based on activities
            user_activities = preferences.get("activities", [])
            for activity in user_activities:
                if activity.lower() in [a.lower() for a in info.get("activities", [])]:
                    score += 20
            
            # Score based on vibe
            user_vibe = preferences.get("vibe", "")
            if user_vibe.lower() in [v.lower() for v in info.get("vibe", [])]:
                score += 15
            
            # Score based on region preference
            if preferences.get("region") and preferences["region"].lower() == info.get("region", "").lower():
                score += 10
            
            matches.append({
                "destination": dest,
                "score": score,
                "info": info
            })
        
        # Sort by score and return top results
        matches = sorted(matches, key=lambda x: x["score"], reverse=True)
        return matches[:num_results]


class ItineraryFormattingSkill:
    """Format and structure itineraries."""
    
    @staticmethod
    def format_day_plan(
        day: int,
        activities: List[str],
        restaurants: List[str],
        accommodation: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Format a single day's plan."""
        return {
            "day": day,
            "morning": activities[0] if len(activities) > 0 else "Free time",
            "afternoon": activities[1] if len(activities) > 1 else "Free time",
            "evening": activities[2] if len(activities) > 2 else "Dinner",
            "restaurants": restaurants,
            "accommodation": accommodation,
            "notes": notes,
            "highlights": activities
        }
    
    @staticmethod
    def create_itinerary_structure(
        destination: str,
        duration: int,
        theme: str = "mixed"
    ) -> Dict[str, Any]:
        """Create base itinerary structure."""
        days = []
        
        # Generic day plans based on theme
        themes_activities = {
            "cultural": ["Museums/Temples", "Historical Sites", "Local Markets"],
            "adventure": ["Hiking", "Water Sports", "Extreme Activities"],
            "relaxation": ["Beach/Spa", "Yoga", "Nature Walks"],
            "food": ["Food Tours", "Cooking Classes", "Fine Dining"],
            "mixed": ["Local Attractions", "Local Experiences", "Unique Activities"]
        }
        
        activity_list = themes_activities.get(theme, themes_activities["mixed"])
        
        for day in range(1, duration + 1):
            day_plan = ItineraryFormattingSkill.format_day_plan(
                day=day,
                activities=activity_list,
                restaurants=["Restaurant TBD"] * 3,
                accommodation="Hotel TBD",
                notes=f"Day {day} in {destination}"
            )
            days.append(day_plan)
        
        return {
            "destination": destination,
            "duration": duration,
            "theme": theme,
            "days": days,
            "created_at": datetime.now().isoformat()
        }


class CurrencyConversionSkill:
    """Handle currency conversions."""
    
    # Simplified exchange rates (would be fetched from API in production)
    EXCHANGE_RATES = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 149.50,
        "INR": 83.12,
        "IDR": 16250,
        "THB": 35.50
    }
    
    @staticmethod
    def convert_currency(
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> Dict[str, Any]:
        """Convert between currencies."""
        from_rate = CurrencyConversionSkill.EXCHANGE_RATES.get(from_currency.upper(), 1.0)
        to_rate = CurrencyConversionSkill.EXCHANGE_RATES.get(to_currency.upper(), 1.0)
        
        amount_in_usd = amount / from_rate
        converted_amount = amount_in_usd * to_rate
        
        return {
            "original_amount": amount,
            "original_currency": from_currency,
            "converted_amount": round(converted_amount, 2),
            "converted_currency": to_currency,
            "exchange_rate": round(to_rate / from_rate, 4)
        }


# Skill factory for easy access
def get_skill(skill_name: str):
    """Get a skill by name."""
    skills = {
        "budget_estimation": BudgetEstimationSkill,
        "destination_matching": DestinationMatchingSkill,
        "itinerary_formatting": ItineraryFormattingSkill,
        "currency_conversion": CurrencyConversionSkill
    }
    return skills.get(skill_name)
