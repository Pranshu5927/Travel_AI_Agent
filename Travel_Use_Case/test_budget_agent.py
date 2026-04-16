#!/usr/bin/env python3
"""
Test script for Budget Agent
Run this to test the budget agent functionality
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_budget_agent():
    """Test the budget agent with sample data"""

    try:
        # Import the budget agent
        from agents.budget_agent import BudgetAgent

        # Create agent instance
        agent = BudgetAgent()

        # Sample input data
        test_input = {
            "destination": "Paris",
            "duration": 5,
            "budget_tier": "moderate",
            "user_budget": 1500,
            "currency": "USD"
        }

        print("🧪 Testing Budget Agent...")
        print(f"Input: {test_input}")

        # Process the request
        result = await agent.process(test_input)

        print("\n✅ Budget Agent Response:")
        print(result)

    except Exception as e:
        print(f"❌ Error testing budget agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_budget_agent())