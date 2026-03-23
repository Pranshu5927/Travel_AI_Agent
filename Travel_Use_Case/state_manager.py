def initialize_state():
    return {
        "destination": None,
        "start_date": None,
        "end_date": None,
        "budget": None,
        "preferences": None
    }


def update_state(state, extracted_info):
    extracted_dict = extracted_info.dict()

    for key, value in extracted_dict.items():
        if value:
            state[key] = value

    return state


def is_ready_for_itinerary(state):
    required_fields = ["destination", "start_date", "end_date"]
    return all(state[field] for field in required_fields)