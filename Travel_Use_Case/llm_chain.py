import os
from dotenv import load_dotenv
from typing import Optional

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate 
from utils import parse_date
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------
# Schema
# -----------------------------
class TravelInfo(BaseModel):
    destination: Optional[str] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    budget: Optional[str] = Field(default=None)
    preferences: Optional[str] = Field(default=None)


# -----------------------------
# Extraction Prompt
# -----------------------------
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Extract travel information from user input.

    IMPORTANT RULES FOR DATES:
    - If user says "next weekend", extract exactly as: "next weekend"
    - If user says "this weekend", extract exactly as: "this weekend"
    - If user says "next Friday" or similar day, extract exactly: "next Friday"
    - If user says "tomorrow", extract exactly as: "tomorrow"
    - If user says "in 3 days" or "in 2 weeks", extract exactly as provided
    - NEVER convert relative dates to absolute dates yourself
    - For absolute dates like "March 28", "April 5th", extract as-is

    Fields to extract:
    - destination: The place they want to visit
    - start_date: When they want to start (as provided by user - relative or absolute)
    - end_date: When they want to end (as provided by user - relative or absolute)
    - budget: Their budget (with currency if mentioned)
    - preferences: Their travel style/preferences

    If a field is missing, return null.
    """),
    ("human", "{input}")
])


def extract_info(user_input: str) -> TravelInfo:
    structured_llm = llm.with_structured_output(TravelInfo)
    chain = extraction_prompt | structured_llm
    return chain.invoke({"input": user_input})


# -----------------------------
# General Chat (for Q&A)
# -----------------------------
def general_chat(user_input: str):
    prompt = f"""
    You are a knowledgeable travel assistant. Answer the user's travel-related question conversationally and helpfully.

    If they're asking about destinations, best times to visit, what to expect, or general travel advice, provide detailed, accurate information.

    If it's not travel-related, politely redirect to travel topics.

    Question: {user_input}

    Answer as a friendly travel expert.
    """
    return llm.invoke(prompt).content


# -----------------------------
# Itinerary Generator
# -----------------------------
def generate_itinerary(state, duration):
    # Parse dates for proper formatting
    start_date_parsed = parse_date(state.get('start_date'))
    end_date_parsed = parse_date(state.get('end_date'))

    start_date_str = start_date_parsed.strftime('%B %d, %Y') if start_date_parsed else state.get('start_date', 'Not specified')
    end_date_str = end_date_parsed.strftime('%B %d, %Y') if end_date_parsed else state.get('end_date', 'Not specified')

    budget_info = f"Budget: {state.get('budget')}" if state.get('budget') else "Budget: Not specified"
    preferences_info = f"Preferences: {state.get('preferences')}" if state.get('preferences') else "Preferences: General sightseeing"

    prompt = f"""
    Create a comprehensive and personalized travel itinerary for a trip to {state['destination']}.

    **Trip Details:**
    - Destination: {state['destination']}
    - Start Date: {start_date_str}
    - End Date: {end_date_str}
    - Duration: {duration} days
    - {budget_info}
    - {preferences_info}

    **Please provide a detailed day-by-day itinerary that includes:**

    **Daily Structure:**
    - Morning activities and breakfast suggestions
    - Afternoon excursions and lunch recommendations
    - Evening entertainment and dinner options
    - Local transportation tips

    **Additional Information:**
    - Best time to visit specific attractions
    - Weather considerations
    - Cultural etiquette and local customs
    - Safety tips and emergency contacts
    - Budget breakdown (if budget provided)
    - Packing suggestions based on activities

    **Make it engaging and practical, like a personal travel guide would provide.**
    """
    return llm.invoke(prompt).content