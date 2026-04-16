#!/usr/bin/env python3
"""
Travel AI Agent v2.0 - Multi-Agent Travel Planning System
Main Streamlit application integrating the coordinator agent
"""

import streamlit as st
import asyncio
import os
from datetime import datetime
from typing import Dict, List, Any

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our agents and services
try:
    from google import adk as google_adk
    from agents import CoordinatorAgent
    from services import get_session_manager, get_memory_service
    AGENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Agents not available: {e}")
    st.error("Running in demo mode with mock agents...")
    AGENTS_AVAILABLE = False

# Mock agents for demo mode
class MockCoordinatorAgent:
    async def process(self, input_data):
        user_message = input_data.get('message', '')
        
        # Simple mock responses based on keywords
        if 'budget' in user_message.lower() or 'cost' in user_message.lower():
            return {
                "agent": "Budget Agent",
                "response": "💰 **Budget Analysis**\n\nI've analyzed your travel costs. For a typical trip, expect:\n- Accommodation: $100-300/night\n- Food: $30-80/day\n- Activities: $50-150/day\n\nTotal estimate: $500-2000 for 5-7 days.\n\nWould you like me to break this down further?",
                "estimated_cost": 1200,
                "feasible": True
            }
        elif 'itinerary' in user_message.lower() or 'plan' in user_message.lower():
            return {
                "agent": "Itinerary Agent", 
                "response": "🗓️ **Sample Itinerary for Paris**\n\n**Day 1: Arrival & Exploration**\n- Morning: Eiffel Tower visit\n- Afternoon: Seine River cruise\n- Evening: Montmartre district\n\n**Day 2: Culture & Museums**\n- Morning: Louvre Museum\n- Afternoon: Notre-Dame Cathedral\n- Evening: French cuisine experience\n\n**Day 3: Shopping & Departure**\n- Morning: Champs-Élysées shopping\n- Afternoon: Free time\n- Evening: Departure\n\nThis is a themed itinerary focusing on culture and landmarks!",
                "days": 3,
                "theme": "cultural"
            }
        elif 'hotel' in user_message.lower() or 'book' in user_message.lower():
            return {
                "agent": "Booking Agent",
                "response": "🏨 **Hotel Search Results**\n\n**Top Options for Paris:**\n\n1. **Hotel Le Marais** - $120/night ⭐⭐⭐⭐\n   - Boutique hotel in historic district\n   - Walking distance to major attractions\n\n2. **Modern Paris Hotel** - $95/night ⭐⭐⭐\n   - Contemporary design, great reviews\n   - Metro access to city center\n\n3. **Budget Inn Paris** - $65/night ⭐⭐\n   - Clean, basic amenities\n   - Good for short stays\n\nAll prices are estimates. Actual rates vary by season and availability.",
                "hotels_found": 3,
                "price_range": "$65-120/night"
            }
        else:
            return {
                "agent": "Coordinator Agent",
                "response": f"👋 Hello! I'm your Travel AI Agent. I can help you with:\n\n- **Trip Planning**: Create personalized itineraries\n- **Budget Analysis**: Estimate costs and check feasibility\n- **Hotel Booking**: Find and compare accommodation options\n- **Destination Research**: Learn about places to visit\n\nYou asked: *{user_message}*\n\nTry asking me to 'plan a trip to Paris' or 'find hotels in Tokyo'!",
                "capabilities": ["planning", "budgeting", "booking", "research"]
            }

# Page configuration
st.set_page_config(
    page_title="🌍 Travel AI Agent v2.0",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1em;
    }
    .agent-response {
        background-color: #f0f8ff;
        border-left: 4px solid #1f77b4;
        padding: 1em;
        margin: 1em 0;
        border-radius: 5px;
    }
    .user-message {
        background-color: #e8f4fd;
        border-left: 4px solid #2e86c1;
        padding: 1em;
        margin: 1em 0;
        border-radius: 5px;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 5px;
    }
    .status-online { background-color: #28a745; }
    .status-offline { background-color: #dc3545; }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if 'session_id' not in st.session_state:
        st.session_state.session_id = None

    if 'agent' not in st.session_state:
        st.session_state.agent = None

    if 'memory_service' not in st.session_state:
        st.session_state.memory_service = None

def initialize_services():
    """Initialize session and memory services"""
    try:
        session_mgr = get_session_manager()
        memory_svc = get_memory_service()

        # Create or load session
        if not st.session_state.session_id:
            session = session_mgr.create_session(st.session_state.user_id)
            st.session_state.session_id = session['session_id']

        st.session_state.memory_service = memory_svc
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize services: {e}")
        return False

def initialize_agent():
    """Initialize the coordinator agent"""
    try:
        agent = CoordinatorAgent()
        st.session_state.agent = agent
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {e}")
        return False

async def process_message(user_message: str) -> Dict[str, Any]:
    """Process user message through the coordinator agent"""
    try:
        # Prepare input data
        input_data = {
            'user_id': st.session_state.user_id,
            'session_id': st.session_state.session_id,
            'message': user_message,
            'timestamp': datetime.now().isoformat(),
            'conversation_history': st.session_state.messages[-5:] if len(st.session_state.messages) > 5 else st.session_state.messages
        }

        # Use mock agent if real agents not available
        if not AGENTS_AVAILABLE:
            agent = MockCoordinatorAgent()
        else:
            agent = st.session_state.agent

        # Process through agent
        response = await agent.process(input_data)

        return {
            'success': True,
            'response': response,
            'agent_used': response.get('agent', 'coordinator'),
            'processing_time': response.get('processing_time', 0)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'response': f"Sorry, I encountered an error: {e}"
        }

def display_message(message: Dict[str, Any], is_user: bool = False):
    """Display a message in the chat interface"""
    if is_user:
        with st.chat_message("user"):
            st.markdown(message['content'])
    else:
        with st.chat_message("assistant"):
            # Agent indicator
            agent_name = message.get('agent', 'AI')
            st.markdown(f"🤖 **{agent_name}**")

            # Response content
            content = message.get('content', message.get('response', ''))
            if isinstance(content, dict):
                # Format structured response
                if 'itinerary' in content:
                    display_itinerary(content['itinerary'])
                elif 'budget' in content:
                    display_budget(content['budget'])
                else:
                    st.json(content)
            else:
                st.markdown(content)

def display_itinerary(itinerary_data: Dict[str, Any]):
    """Display formatted itinerary"""
    st.markdown("### 🗓️ Your Travel Itinerary")

    if 'days' in itinerary_data:
        for day in itinerary_data['days']:
            with st.expander(f"📅 {day['title']}", expanded=True):
                st.markdown(f"**Theme:** {day.get('theme', 'General')}")
                st.markdown(f"**Highlights:** {day.get('highlights', 'N/A')}")

                if 'activities' in day:
                    st.markdown("**Activities:**")
                    for activity in day['activities']:
                        st.markdown(f"- {activity}")

                if 'tips' in day:
                    st.markdown("**💡 Tips:**")
                    for tip in day['tips']:
                        st.markdown(f"- {tip}")

def display_budget(budget_data: Dict[str, Any]):
    """Display formatted budget breakdown"""
    st.markdown("### 💰 Budget Analysis")

    if 'feasible' in budget_data:
        status = "✅ Feasible" if budget_data['feasible'] else "❌ Not Feasible"
        st.markdown(f"**Status:** {status}")

    if 'estimated_cost' in budget_data:
        st.markdown(f"**Estimated Total:** ${budget_data['estimated_cost']}")

    if 'breakdown' in budget_data:
        st.markdown("**Breakdown:**")
        breakdown = budget_data['breakdown']
        cols = st.columns(len(breakdown))
        for i, (category, amount) in enumerate(breakdown.items()):
            with cols[i]:
                st.metric(category.title(), f"${amount}")

def main():
    """Main application"""
    # Initialize session state
    initialize_session_state()

    # Title and header
    st.markdown('<div class="main-header">🌍 Travel AI Agent v2.0</div>', unsafe_allow_html=True)
    st.markdown("*Your intelligent multi-agent travel planning companion*")

    # Sidebar with system status
    with st.sidebar:
        st.header("🔧 System Status")

        # Agent status
        if AGENTS_AVAILABLE:
            st.markdown('<span class="status-indicator status-online"></span>Agents: Online', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-offline"></span>Agents: Demo Mode', unsafe_allow_html=True)
            st.info("🧪 Running with mock agents. Full AI features require Google ADK.")

        # Services status
        services_ok = initialize_services() if AGENTS_AVAILABLE else True
        if services_ok:
            st.markdown('<span class="status-indicator status-online"></span>Services: Online', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-indicator status-offline"></span>Services: Offline', unsafe_allow_html=True)

        # User info
        st.header("👤 User Info")
        st.text(f"User ID: {st.session_state.user_id[:12]}...")
        if st.session_state.session_id:
            st.text(f"Session: {st.session_state.session_id[:12]}...")

        # Quick actions
        st.header("⚡ Quick Actions")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        if st.button("📊 View Memory"):
            if st.session_state.memory_service:
                try:
                    memory = st.session_state.memory_service.load_user_preferences(st.session_state.user_id)
                    st.json(memory)
                except Exception as e:
                    st.error(f"Could not load memory: {e}")

        # Sample prompts
        st.header("💡 Sample Prompts")
        sample_prompts = [
            "Plan a 3-day trip to Paris on a $2000 budget",
            "Find hotels in Tokyo for next weekend",
            "What's the best time to visit Bali?",
            "Convert $1000 USD to EUR for my trip",
            "Suggest a food-focused itinerary for Bangkok"
        ]

        for prompt in sample_prompts:
            if st.button(prompt, key=f"sample_{hash(prompt)}"):
                st.session_state.sample_prompt = prompt
                st.rerun()

    # Check if we have a sample prompt to use
    if 'sample_prompt' in st.session_state:
        user_input = st.session_state.sample_prompt
        del st.session_state.sample_prompt
    else:
        user_input = st.chat_input("Ask me about your travel plans...")

    # Display chat history
    for message in st.session_state.messages:
        display_message(message, message.get('role') == 'user')

    # Process new message
    if user_input and AGENTS_AVAILABLE and services_ok:
        # Add user message to history
        user_message = {
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.messages.append(user_message)
        display_message(user_message, True)

        # Process with agent
        with st.spinner("🤔 Thinking..."):
            # Initialize agent if needed
            if not st.session_state.agent:
                if not initialize_agent():
                    st.error("Could not initialize agent")
                    return

            # Process message
            result = asyncio.run(process_message(user_input))

            # Create response message
            response_message = {
                'role': 'assistant',
                'content': result['response'],
                'agent': result.get('agent_used', 'coordinator'),
                'timestamp': datetime.now().isoformat(),
                'success': result['success']
            }

            # Add to history
            st.session_state.messages.append(response_message)

            # Display response
            display_message(response_message)

            # Show processing info
            if result.get('processing_time'):
                st.caption(f"⚡ Processed in {result['processing_time']:.2f}s")

    elif user_input:
        st.error("❌ System not fully initialized. Please check the sidebar status.")

    # Footer
    st.markdown("---")
    st.markdown("*Built with Google ADK + LangGraph • Multi-agent architecture • Session persistence*")

if __name__ == "__main__":
    main()
