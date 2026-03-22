import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_itinerary(destination, days, budget=None):
    prompt = f"""
    Create a detailed {days}-day travel itinerary for {destination}.
    
    Include:
    - Day-wise plan
    - Places to visit
    - Food recommendations
    - Travel tips
    
    Budget: {budget if budget else "Not specified"}
    
    Keep it structured and easy to read.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful travel planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content