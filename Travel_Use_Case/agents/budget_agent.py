"""
Budget Agent - Priority 2
Responsible for budget estimation, cost tracking, and financial planning.
"""

import logging
from typing import Any, Dict, Optional, List
from .base_agent import BaseAgent, AgentRole
from skills.travel_skills import BudgetEstimationSkill, CurrencyConversionSkill
from services.callbacks import get_cost_tracker

logger = logging.getLogger(__name__)


class BudgetAgent(BaseAgent):
    """
    Budget planning and cost management agent.
    Estimates trip costs, creates budget breakdowns, and tracks spending.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="budget_agent_v1",
            role=AgentRole.BUDGET,
            name="Budget Agent"
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process budget estimation request.
        
        Input:
        {
            "destination": str,
            "duration": int,
            "budget": float,
            "budget_tier": str (budget/moderate/luxury),
            "user_id": str,
            "currency": str (optional)
        }
        
        Output:
        {
            "success": bool,
            "budget_breakdown": Dict,
            "feasibility": Dict,
            "recommendations": List[str],
            "error": Optional[str]
        }
        """
        
        # Validate required fields
        required_fields = ["destination", "duration"]
        if not self.validate_input(required_fields, input_data):
            return {
                "success": False,
                "error": "Missing required fields: destination, duration",
                "budget_breakdown": None
            }
        
        destination = input_data.get("destination")
        duration = input_data.get("duration")
        budget = input_data.get("budget")
        tier = input_data.get("budget_tier", "moderate")
        user_id = input_data.get("user_id")
        currency = input_data.get("currency", "USD")
        
        self.log_action(
            "Estimating budget",
            {
                "destination": destination,
                "duration": duration,
                "tier": tier,
                "budget": budget
            }
        )
        
        try:
            # Estimate budget
            breakdown = BudgetEstimationSkill.estimate_budget(
                destination, duration, tier
            )
            
            # Check feasibility
            feasibility = BudgetEstimationSkill.validate_budget(
                budget if budget else breakdown["total"],
                destination,
                duration
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                breakdown,
                feasibility,
                budget,
                tier
            )
            
            # Track cost for user if user_id provided
            if user_id and budget:
                cost_tracker = get_cost_tracker(user_id, budget)
                is_valid, msg = cost_tracker.validate_budget()
            
            result = {
                "success": True,
                "budget_breakdown": breakdown,
                "feasibility": feasibility,
                "recommendations": recommendations,
                "currency": currency,
                "metadata": {
                    "destination": destination,
                    "duration": duration,
                    "tier": tier
                }
            }
            
            self.log_action("Budget estimation complete", {"feasible": feasibility["is_feasible"]})
            return result
        
        except Exception as e:
            logger.error(f"Error in budget estimation: {e}")
            return {
                "success": False,
                "error": str(e),
                "budget_breakdown": None,
                "feasibility": None
            }
    
    def _generate_recommendations(
        self,
        breakdown: Dict[str, Any],
        feasibility: Dict[str, Any],
        user_budget: Optional[float],
        tier: str
    ) -> List[str]:
        """Generate budget-related recommendations."""
        recommendations = []
        
        # Feasibility recommendations
        if not feasibility.get("is_feasible"):
            recommendations.append(
                f"⚠️ Current budget is insufficient. "
                f"Recommend increasing by ${feasibility.get('difference', 0):.2f}"
            )
        
        # Tier recommendations
        if user_budget:
            total = breakdown.get("total", 0)
            ratio = user_budget / total if total > 0 else 0
            
            if ratio < 0.8:
                recommendations.append(
                    "💡 Consider upgrading to luxury experiences for better value"
                )
            elif ratio > 1.5:
                recommendations.append(
                    "💰 You have extra budget! Consider adding premium activities or longer stay"
                )
        
        # Per-category recommendations
        if breakdown.get("accommodation"):
            acc_cost = breakdown["accommodation"]["total"]
            recommendations.append(
                f"🏨 Accommodation budget: ${acc_cost:.2f} ({breakdown['accommodation']['daily']:.2f}/night)"
            )
        
        if breakdown.get("food"):
            food_cost = breakdown["food"]["total"]
            recommendations.append(
                f"🍽️ Food budget: ${food_cost:.2f} ({breakdown['food']['daily']:.2f}/day)"
            )
        
        # Cost saving tips
        recommendations.append(
            "💡 Tip: Book accommodation and flights in advance for better rates"
        )
        recommendations.append(
            "💡 Tip: Use public transportation instead of taxis/Uber"
        )
        
        return recommendations
    
    async def refine_budget(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Refine budget based on changes to trip."""
        
        # Handle budget changes from user feedback
        if "new_preferences" in input_data:
            return await self.process(input_data)
        
        return {
            "success": False,
            "error": "No budget changes provided"
        }
    
    async def compare_budget_tiers(
        self,
        destination: str,
        duration: int
    ) -> Dict[str, Any]:
        """Compare costs across different budget tiers."""
        
        tiers = ["budget", "moderate", "luxury"]
        comparison = {
            "destination": destination,
            "duration": duration,
            "tiers": {}
        }
        
        for tier in tiers:
            breakdown = BudgetEstimationSkill.estimate_budget(
                destination, duration, tier
            )
            comparison["tiers"][tier] = {
                "total": breakdown["total"],
                "accommodation": breakdown.get("accommodation", {}).get("total"),
                "food": breakdown.get("food", {}).get("total"),
                "activities": breakdown.get("activities", {}).get("total"),
                "transport": breakdown.get("transport", {}).get("total")
            }
        
        return {
            "success": True,
            "comparison": comparison,
            "metadata": {
                "destination": destination,
                "duration": duration
            }
        }
