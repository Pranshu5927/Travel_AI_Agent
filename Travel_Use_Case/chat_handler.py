from llm_chain import extract_info, general_chat, generate_itinerary
from state_manager import update_state, reset_state
from utils import parse_date, calculate_duration


def handle_user_input(user_input, state, chat_history):

    # -----------------------------
    # Step 1: Extract info
    # -----------------------------
    extracted = extract_info(user_input)

    # -----------------------------
    # Step 2: Detect destination change → reset
    # -----------------------------
    if extracted.destination and state["destination"]:
        if extracted.destination.lower() != state["destination"].lower():
            state.clear()
            state.update(reset_state())
            return f"Starting a new trip to {extracted.destination}! Tell me your travel dates."

    # -----------------------------
    # Step 3: Update state
    # -----------------------------
    # Check if new information was provided after itinerary generation
    new_info_provided = False
    if state["itinerary_generated"] and (extracted.destination or extracted.start_date or extracted.end_date or extracted.budget or extracted.preferences):
        new_info_provided = True

    state = update_state(state, extracted)

    # Handle "next weekend" or "this weekend" - infer end date
    if state["start_date"] and not state["end_date"]:
        start_lower = state["start_date"].lower().strip()
        if "weekend" in start_lower:
            # If start is "next weekend" or similar, end is the next day (Sunday)
            state["end_date"] = state["start_date"].replace("weekend", "sunday").replace("next", "next")
            if "next weekend" in start_lower:
                state["end_date"] = "next sunday"
            elif "this weekend" in start_lower:
                state["end_date"] = "this sunday"

    # If end date is not provided but start is, try to infer end as a few days later
    if state["start_date"] and not state["end_date"] and "weekend" not in state["start_date"].lower():
        state["end_date"] = state["start_date"]  # Default: same day, will be handled later

    # -----------------------------
    # Step 4: Parse dates
    # -----------------------------
    start = parse_date(state["start_date"]) if state["start_date"] else None
    end = parse_date(state["end_date"]) if state["end_date"] else None

    duration = calculate_duration(start, end)

    # -----------------------------
    # Step 5: Handle general questions
    # -----------------------------
    if not extracted.destination and not state["destination"]:
        return general_chat(user_input)

    # -----------------------------
    # Step 6: Ask missing info
    # -----------------------------
    if not state["destination"]:
        return "Where would you like to travel?"

    if not state["start_date"] or not state["end_date"]:
        return "Could you share your travel dates?"

    # Budget & preferences are OPTIONAL now

    # -----------------------------
    # Step 7: Generate itinerary
    # -----------------------------
    if not state["itinerary_generated"]:
        itinerary = generate_itinerary(state, duration)
        state["itinerary_generated"] = True
        state["awaiting_feedback"] = True
        state["itinerary_content"] = itinerary

        return itinerary + "\n\n---\nWhat do you think? Would you like me to:\n• Make changes to this itinerary?\n• Check flights and transportation?\n• Add more details or suggestions?\n• Start planning something else?"

    # -----------------------------
    # Step 8: Agentic follow-up loop
    # -----------------------------
    if state["awaiting_feedback"]:
        user_input_lower = user_input.lower()

        # Handle new information provided
        if new_info_provided:
            # Recalculate dates and duration if they changed
            start = parse_date(state["start_date"]) if state["start_date"] else None
            end = parse_date(state["end_date"]) if state["end_date"] else None
            duration = calculate_duration(start, end)
            # Regenerate itinerary with new information
            itinerary = generate_itinerary(state, duration)
            state["itinerary_content"] = itinerary
            return f"I've updated your itinerary with the new information!\n\n{itinerary}\n\n---\nWhat do you think? Would you like me to:\n• Make changes to this itinerary?\n• Check flights and transportation?\n• Add more details or suggestions?\n• Start planning something else?"

        # Handle regeneration requests
        if any(word in user_input_lower for word in ["regenerate", "update", "refresh", "new itinerary"]):
            state["itinerary_generated"] = False
            return "I'll regenerate your itinerary with the latest information!"

        # Handle itinerary modifications
        if any(word in user_input_lower for word in ["change", "modify", "different", "adjust", "not happy", "water", "adventure", "food", "cuisine", "restaurant", "spend", "more time", "love"]):
            state["itinerary_generated"] = False
            state["awaiting_feedback"] = False
            return "I'd be happy to adjust the itinerary! What specific changes would you like to make? For example, different activities, timing, or budget considerations?"

        # Handle flight/transport requests
        if any(word in user_input_lower for word in ["flight", "transport", "book", "travel", "fly"]):
            state["awaiting_feedback"] = False
            return "Great! I'll help you find the best transportation options. What are your preferences for travel (budget, speed, direct flights, etc.)?"

        # Handle additional details
        if any(word in user_input_lower for word in ["more", "details", "suggestions", "add", "recommend"]):
            state["awaiting_feedback"] = False
            return "I'd love to provide more details! What specific aspects would you like me to expand on? (accommodation recommendations, local cuisine, safety tips, etc.)"

        # Handle positive feedback
        if any(word in user_input_lower for word in ["good", "great", "love", "perfect", "yes", "like it"]):
            state["awaiting_feedback"] = False
            return "Wonderful! I'm glad you like the itinerary. Now that we have a plan, would you like me to help with:\n• Finding flights and transportation?\n• Booking recommendations?\n• Packing suggestions?\n• Local tips and hidden gems?"

        # Handle new planning
        if any(word in user_input_lower for word in ["new", "different", "another", "else"]):
            state.clear()
            state.update(reset_state())
            return "Let's plan something new! Where would you like to go this time?"

        # Default response for unclear feedback
        return "I want to make sure this itinerary is perfect for you. Could you let me know if you'd like to make any changes, or if there's anything specific you'd like me to help with next?"

    # -----------------------------
    # Step 9: Ongoing conversation
    # -----------------------------
    if "change" in user_input.lower() or "modify" in user_input.lower():
        state["itinerary_generated"] = False
        state["awaiting_feedback"] = False
        return "Sure! What would you like to change about the itinerary?"

    if "flight" in user_input.lower() or "transport" in user_input.lower():
        return "Great! I'll help you find the best transportation options. What are your preferences?"

    return general_chat(user_input)