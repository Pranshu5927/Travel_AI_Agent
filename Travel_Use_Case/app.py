import streamlit as st
from chat_handler import handle_user_input
from state_manager import initialize_state

st.set_page_config(page_title="Travel AI Agent 🌍")

st.title("🌍 Travel Planner Chatbot")

# -----------------------------
# Initialize session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "state" not in st.session_state:
    st.session_state.state = initialize_state()


# -----------------------------
# Display chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -----------------------------
# Chat input
# -----------------------------
user_input = st.chat_input("Tell me about your trip...")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # Get response
    response = handle_user_input(
        user_input,
        st.session_state.state,
        st.session_state.messages
    )

    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)