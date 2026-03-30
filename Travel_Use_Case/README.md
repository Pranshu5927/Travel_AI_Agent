# Travel AI Agent

A conversational travel planning assistant built with LangChain + GPT-4o-mini + Streamlit.
The agent maintains multi-turn conversation context, manages multiple concurrent trip plans,
and generates structured day-by-day itineraries from natural language input.



## What it does
- Accepts freeform travel requests ("5 days in Japan, April, $3000 budget, cultural focus")
- Asks clarifying follow-up questions to refine preferences
- Generates comprehensive itineraries: daily schedule, food, transport, budget breakdown
- Handles trip modifications mid-conversation ("make it more adventure-focused")
- Manages multiple trips simultaneously with isolated conversation histories
- Parses relative dates ("next weekend", "in 2 weeks") via dateutil

## Architecture
