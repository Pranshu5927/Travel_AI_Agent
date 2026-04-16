#!/usr/bin/env python3
"""
Simple CLI test for Budget Agent - No external dependencies required
"""

import json
from datetime import datetime

# Mock the skills since we don't have full dependencies
class MockBudgetEstimationSkill:
    @staticmethod
    def estimate_budget(destination, duration, tier):
        # Mock data
        base_costs = {
            "budget": {"accommodation": 30, "food": 15, "activities": 10, "transport": 5},
            "moderate": {"accommodation": 80, "food": 40, "activities": 30, "transport": 15},
            "luxury": {"accommodation": 200, "food": 100, "activities": 75, "transport": 50}
        }

        multipliers = {
            "Paris": 1.9, "Tokyo": 1.8, "Bali": 0.4, "Bangkok": 0.5, "New York": 2.0
        }

        multiplier = multipliers.get(destination, 1.0)
        costs = base_costs.get(tier, base_costs["moderate"])

        total = sum(costs.values()) * duration * multiplier

        return {
            "destination": destination,
            "duration": duration,
            "tier": tier,
            "multiplier": multiplier,
            "breakdown": {k: v * duration * multiplier for k, v in costs.items()},
            "total_estimated": round(total, 2)
        }

# Simple budget agent implementation
class SimpleBudgetAgent:
    def __init__(self):
        self.skill = MockBudgetEstimationSkill()

    async def process(self, input_data):
        """Process budget request"""
        destination = input_data.get("destination", "Unknown")
        duration = input_data.get("duration", 1)
        budget_tier = input_data.get("budget_tier", "moderate")
        user_budget = input_data.get("user_budget", 0)

        # Get estimate
        estimate = self.skill.estimate_budget(destination, duration, budget_tier)

        # Check feasibility
        feasible = estimate["total_estimated"] <= user_budget if user_budget > 0 else True

        return {
            "agent": "Budget Agent",
            "feasible": feasible,
            "estimate": estimate,
            "user_budget": user_budget,
            "difference": user_budget - estimate["total_estimated"] if user_budget > 0 else 0,
            "recommendations": self._get_recommendations(estimate, feasible)
        }

    def _get_recommendations(self, estimate, feasible):
        """Get budget recommendations"""
        recs = []

        if not feasible:
            cheaper_total = estimate["total_estimated"] * 0.7
            recs.append(f"Consider budget tier for ~${cheaper_total:.0f} total")

        recs.append(f"Daily budget: ~${estimate['total_estimated']/estimate['duration']:.0f}")
        recs.append("Prices vary by season - check current rates")

        return recs

async def test_budget_agent():
    """Test the budget agent"""
    print("🧪 Testing Simple Budget Agent (No external dependencies)")
    print("=" * 60)

    agent = SimpleBudgetAgent()

    # Test cases
    test_cases = [
        {
            "destination": "Paris",
            "duration": 5,
            "budget_tier": "moderate",
            "user_budget": 1500
        },
        {
            "destination": "Bali",
            "duration": 7,
            "budget_tier": "budget",
            "user_budget": 500
        },
        {
            "destination": "Tokyo",
            "duration": 3,
            "budget_tier": "luxury",
            "user_budget": 2000
        }
    ]

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}:")
        print(f"   Destination: {test_input['destination']}")
        print(f"   Duration: {test_input['duration']} days")
        print(f"   Budget Tier: {test_input['budget_tier']}")
        print(f"   User Budget: ${test_input['user_budget']}")

        result = await agent.process(test_input)

        print("\n✅ Result:")
        print(f"   Feasible: {'Yes' if result['feasible'] else 'No'}")
        print(f"   Estimated Total: ${result['estimate']['total_estimated']:.2f}")

        if not result['feasible']:
            print(f"   Shortfall: ${abs(result['difference']):.2f}")

        print("   Breakdown:")
        for category, amount in result['estimate']['breakdown'].items():
            print(f"     {category.title()}: ${amount:.2f}")

        print("   💡 Recommendations:")
        for rec in result['recommendations']:
            print(f"     • {rec}")

    print("\n" + "=" * 60)
    print("🎉 Budget Agent Test Complete!")
    print("\n💡 This demonstrates the core budget estimation logic.")
    print("   The full system includes Google ADK for intelligent reasoning,")
    print("   session persistence, and multi-agent coordination.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_budget_agent())