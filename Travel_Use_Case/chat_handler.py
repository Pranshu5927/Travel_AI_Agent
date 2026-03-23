from llm_chain import extract_info, llm
from state_manager import update_state


def handle_user_input(user_input, state, chat_history):

    # Step 1: Extract structured info
    extracted = extract_info(user_input)

    print("🧠 Extracted Info:", extracted)

    # Step 2: Update state
    state = update_state(state, extracted)

    # Step 3: Decision logic

    if not state["destination"]:
        return "Where would you like to travel?"

    if not state["start_date"] or not state["end_date"]:
        return "Could you share your travel dates?"

    if not state["budget"]:
        return "Do you have a budget in mind?"

    if not state["preferences"]:
        return "What kind of trip do you prefer? (adventure, relaxing, cultural, etc.)"

    # Step 4: Generate itinerary
    prompt = f"""
    Create a detailed travel itinerary:

    Destination: {state['destination']}
    Start Date: {state['start_date']}
    End Date: {state['end_date']}
    Budget: {state['budget']}
    Preferences: {state['preferences']}

    Provide a day-wise plan with:
    - Activities
    - Food suggestions
    - Travel tips
    """

    response = llm.invoke(prompt)

    return response.content