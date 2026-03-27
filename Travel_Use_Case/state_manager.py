def initialize_state():
    return {
        "destination": None,
        "start_date": None,
        "end_date": None,
        "budget": None,
        "preferences": None,
        "itinerary_generated": False,
        "awaiting_feedback": False,
        "itinerary_content": None
    }


def update_state(state, extracted_info):
    data = extracted_info.dict()

    for key, value in data.items():
        if value:
            state[key] = value

    return state


def reset_state():
    return initialize_state()