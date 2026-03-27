import streamlit as st
import re
from chat_handler import handle_user_input
from state_manager import initialize_state

st.set_page_config(page_title="Travel AI Agent 🌍", layout="wide")

st.title("🌍 Travel Planner")

# -----------------------------
# SESSION INIT
# -----------------------------
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
    st.session_state.conversations["Chat 1"] = {
        "messages": [],
        "state": initialize_state()
    }

# -----------------------------
# SIDEBAR (CHAT HISTORY)
# -----------------------------
st.sidebar.title("🧭 Your Trips")

# New Trip button at the top
if st.sidebar.button("➕ New Trip", key="new_trip_sidebar"):
    new_chat = f"Trip {len(st.session_state.conversations) + 1}"
    st.session_state.conversations[new_chat] = {
        "messages": [],
        "state": initialize_state()
    }
    st.session_state.current_chat = new_chat
    st.rerun()  # Refresh to show new trip

st.sidebar.markdown("---")

# List existing trips
for chat_name in st.session_state.conversations.keys():
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        if st.button(chat_name, key=f"select_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()
    with col2:
        if st.button("🗑️", key=f"delete_{chat_name}", help="Delete this trip"):
            if len(st.session_state.conversations) > 1:
                del st.session_state.conversations[chat_name]
                if st.session_state.current_chat == chat_name:
                    st.session_state.current_chat = list(st.session_state.conversations.keys())[0]
                st.rerun()
            else:
                st.sidebar.error("Cannot delete the last trip")

    # Show trip summary
    trip_state = st.session_state.conversations[chat_name]["state"]
    if trip_state["destination"]:
        st.sidebar.caption(f"📍 {trip_state['destination']}")
        if trip_state["start_date"]:
            st.sidebar.caption(f"📅 {trip_state['start_date']}")
        if trip_state["itinerary_generated"]:
            st.sidebar.caption("✅ Itinerary ready")

st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: Each trip maintains its own conversation and itinerary")

# -----------------------------
# CURRENT CHAT
# -----------------------------
chat = st.session_state.conversations[st.session_state.current_chat]

messages = chat["messages"]
state = chat["state"]

# Trip header
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"📍 {st.session_state.current_chat}")
    if state["destination"]:
        st.caption(f"Destination: {state['destination']}")
    if state["start_date"] and state["end_date"]:
        st.caption(f"Dates: {state['start_date']} - {state['end_date']}")
with col2:
    if st.button("🔄 New Itinerary", help="Start planning a new itinerary for this trip"):
        state.clear()
        state.update(initialize_state())
        messages.clear()
        st.rerun()

# Display messages
for msg in messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Plan your trip...")

if user_input:
    # Check if destination was set before this message
    destination_was_none = state["destination"] is None

    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    response = handle_user_input(user_input, state, messages)

    messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)

    # Rename chat if destination was just set
    if destination_was_none and state["destination"] and not st.session_state.current_chat.startswith(state["destination"]):
        new_chat_name = f"{state['destination']} Trip"
        # Ensure unique name
        counter = 1
        original_name = new_chat_name
        while new_chat_name in st.session_state.conversations:
            new_chat_name = f"{original_name} {counter}"
            counter += 1

        # Rename the chat
        st.session_state.conversations[new_chat_name] = st.session_state.conversations[st.session_state.current_chat]
        del st.session_state.conversations[st.session_state.current_chat]
        st.session_state.current_chat = new_chat_name
        st.rerun()

    # Handle destination change (when user switches destinations)
    if response.startswith("Starting a new trip to"):
        # Extract destination from response
        match = re.search(r"Starting a new trip to (.+)!", response)
        if match:
            new_destination = match.group(1).strip()
            new_chat_name = f"{new_destination} Trip"
            # Ensure unique name
            counter = 1
            original_name = new_chat_name
            while new_chat_name in st.session_state.conversations:
                new_chat_name = f"{original_name} {counter}"
                counter += 1

            # Rename the chat
            st.session_state.conversations[new_chat_name] = st.session_state.conversations[st.session_state.current_chat]
            del st.session_state.conversations[st.session_state.current_chat]
            st.session_state.current_chat = new_chat_name
            st.rerun()