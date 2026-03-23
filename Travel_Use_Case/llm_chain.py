import os
from dotenv import load_dotenv
from typing import Optional

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)

# -----------------------------
# Pydantic Schema
# -----------------------------
class TravelInfo(BaseModel):
    destination: Optional[str] = Field(default=None)
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)
    budget: Optional[str] = Field(default=None)
    preferences: Optional[str] = Field(default=None)


# -----------------------------
# Prompt
# -----------------------------
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Extract travel information from the user input.

    Fields to extract:
    - destination
    - start_date
    - end_date
    - budget
    - preferences

    If any field is missing, return null.
    """),
    ("human", "{input}")
])


# -----------------------------
# Structured Extraction
# -----------------------------
def extract_info(user_input: str) -> TravelInfo:
    structured_llm = llm.with_structured_output(TravelInfo)
    chain = extraction_prompt | structured_llm
    response = chain.invoke({"input": user_input})
    return response