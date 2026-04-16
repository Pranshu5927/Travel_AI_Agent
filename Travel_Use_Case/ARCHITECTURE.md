# 🏗️ System Architecture

## Overview

The Travel AI Agent is a **hybrid multi-agent system** that combines:
- **Google ADK** for intelligent reasoning and personalization
- **LangGraph** for deterministic booking flows and validation
- **MCP (Model Context Protocol)** for external data integration
- **JSON/CSV persistence** for session and user data management

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   STREAMLIT FRONTEND                         │
│         (Web UI for user interactions & chat)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────────┐    ┌──────────▼──────────┐
│  Session Manager   │    │  Memory Service      │
│  (JSON-based)      │    │  (CSV + JSON)        │
│  - Persist state   │    │  - User preferences  │
│  - Keep 5 sessions │    │  - Trip history      │
└────────────────────┘    └─────────────────────┘
        │                         │
        └─────────┬───────────────┘
                  │
        ┌─────────▼──────────────────────────────┐
        │   CALLBACK SYSTEM & VALIDATORS         │
        ├────────────────────────────────────────┤
        │ • Cost Tracker (Budget validation)     │
        │ • Event Logger (Observability)         │
        │ • Rate Limiter (API throttling)        │
        │ • Date/Budget Validators               │
        └─────────┬──────────────────────────────┘
                  │
        ┌─────────▼──────────────────────────────────────┐
        │         AGENT ORCHESTRATION LAYER              │
        │     (Coordinator Agent - Google ADK)           │
        └─┬───┬───┬────┬──────────┬────────────────────┘
          │   │   │    │          │
    ┌─────▼─┐ │   │    │   ┌──────▼─────┐    ┌──────────────┐
    │ Dest. │ │   │    │   │  Memory &  │    │  Coordinator │
    │Research│ │   │    │   │Personal.  │    │   (Router)   │
    │(Google)│ │   │    │   │ (Google)   │    │(Google ADK)  │
    └───────┘ │   │    │   └────────────┘    └──────────────┘
              │   │    │
        ┌─────▼─┐ │    │
        │Itiner.│ │    │
        │(Google)│ │    │
        └───────┘ │    │
                  │    │
            ┌─────▼─┐ ┌▼──────────┐
            │Budget │ │  Booking  │
            │(Google)│ │ (LangGraph)
            └───────┘ └───────────┘
                  │
        ┌─────────▼──────────────────┐
        │    SKILLS LAYER            │
        ├────────────────────────────┤
        │ • Budget Estimation Skill  │
        │ • Destination Matching     │
        │ • Itinerary Formatting     │
        │ • Currency Conversion      │
        └─────────┬──────────────────┘
                  │
        ┌─────────▼──────────────────────────────┐
        │    MCP INTEGRATIONS                    │
        ├────────────────────────────────────────┤
        │ • Weather Lookup                       │
        │ • Hotel/Flight Search                  │
        │ • Currency Exchange Rates              │
        └────────────────────────────────────────┘
```

## Component Details

### 1. **Frontend Layer (Streamlit)**
- User chat interface
- Trip management UI
- Session/history display
- Real-time response streaming

### 2. **Persistence Layer**
#### Session Manager
- JSON file-based storage (`data/sessions/`)
- Maintains up to 5 active sessions per user
- Auto-saves session state after each interaction
- 30-day expiry policy

#### Memory Service
- **users.csv**: User profiles and preferences
- **{user_id}_memory.json**: Personalized memory storage
- **{user_id}_costs.json**: Cost tracking data
- **{user_id}_events.json**: Audit trail and event logging

### 3. **Callback & Validation System**
```python
┌─ CostTracker
│  ├─ track API costs (OpenAI, Google)
│  ├─ validate against budget
│  └─ alert on budget warnings
│
├─ DateValidator
│  └─ validate trip dates (no end before start, etc.)
│
├─ BudgetValidator
│  ├─ estimate minimum costs
│  └─ warn if budget insufficient
│
├─ APIRateLimiter
│  └─ throttle requests (60 calls/min default)
│
└─ EventLogger
   └─ log all events for debugging
```

**Callbacks (Priority):**
1. **Cost Tracking** - Main priority (every API call)
2. **Budget Validation** - Check spending vs limit
3. **API Rate Limiting** - Prevent quota exceeded
4. **Date Validation** - Realistic trip dates

### 4. **Agent System (Google ADK)**

All agents implement `BaseAgent` interface:
```python
class BaseAgent:
    async def process(input_data) -> output_data
    def validate_input(required_fields, data) -> bool
    def log_action(action, details)
```

#### **Priority 1: Itinerary Agent**
- **Role**: Generate day-by-day itineraries
- **Input**: destination, dates, preferences, duration
- **Output**: 
  ```json
  {
    "destination": "Paris",
    "duration": 5,
    "days": [
      {
        "day": 1,
        "morning": "Louvre Museum",
        "afternoon": "Seine River Cruise",
        "evening": "Dinner at local restaurant"
      }
    ],
    "highlights": ["Eiffel Tower", "Notre-Dame", ...],
    "practical_tips": {...}
  }
  ```

#### **Priority 2: Budget Agent**
- **Role**: Estimate costs, create budget breakdowns
- **Input**: destination, duration, tier, budget
- **Output**:
  ```json
  {
    "breakdown": {
      "accommodation": 500,
      "food": 300,
      "activities": 400,
      "transport": 150,
      "total": 1350
    },
    "feasibility": {...},
    "recommendations": [...]
  }
  ```

#### **Priority 3: Booking Helper Agent**
- **Role**: Search and recommend hotels, flights, activities
- **Uses**: LangGraph for booking flows (deterministic)
- **Input**: destination, dates, preferences
- **Output**: Hotel/flight options with recommendations

#### **Priority 4: Memory & Personalization Agent**
- **Role**: Remember preferences, provide personalized recommendations
- **Input**: user_id, preferences, destination
- **Output**: Personalized suggestions based on history
- **Methods**:
  - `save_preferences()` - Store user preferences
  - `load_preferences()` - Retrieve user profile
  - `learn_from_interactions()` - Update based on behavior

#### **Additional Agents**
- **Destination Research Agent**: Information about destinations
- **Coordinator Agent**: Orchestrates all agents, routes requests

### 5. **Skills Layer**

Reusable domain-specific functions:

#### **BudgetEstimationSkill**
```python
estimate_budget(destination, duration, tier) -> breakdown
validate_budget(budget, destination, duration) -> feasibility
```

#### **DestinationMatchingSkill**
```python
match_destinations(preferences) -> ranked_list
```

#### **ItineraryFormattingSkill**
```python
format_day_plan(day, activities, restaurants) -> day_plan
create_itinerary_structure(destination, duration) -> structure
```

#### **CurrencyConversionSkill**
```python
convert_currency(amount, from_curr, to_curr) -> result
```

### 6. **MCP Integration Layer**

Model Context Protocol servers for external data:

```
WeatherMCPClient
├─ get_weather_forecast(location, days)
└─ Returns: forecast data with temp, conditions, etc.

HotelFlightMCPClient
├─ search_hotels(destination, check_in, check_out)
├─ search_flights(origin, destination, dates)
└─ Returns: options with prices, ratings, etc.

CurrencyConversionMCPClient
└─ convert_currency(amount, from, to)
```

**MCP Fall-back**: Mock data for development

### 7. **Data Flow**

```
User Input
    │
    ▼
Coordinator Agent (Google ADK)
    │
    ├─ Analyzes intent
    ├─ Routes to appropriate agent(s)
    │
    ▼
Memory Agent
    ├─ Load user preferences
    ├─ Session state
    └─ Event logging
    │
    ▼
Primary Agent(s) [Based on request]
    │
    ├─ Itinerary Agent -> Generate itinerary
    ├─ Budget Agent -> Estimate costs
    ├─ Booking Agent -> Search hotels/flights
    └─ Destination Agent -> Research info
    │
    ▼
Skills & Validators
    ├─ Apply business logic
    ├─ Validate constraints
    └─ Format output
    │
    ▼
MCP Clients [As needed]
    ├─ Weather lookup
    ├─ Hotel/flight search
    └─ Currency conversion
    │
    ▼
Callback System
    ├─ Cost tracking
    ├─ Budget validation
    ├─ Event logging
    └─ Rate limiting
    │
    ▼
Response Formatting
    │
    ▼
Frontend Display
```

## Session & Memory Architecture

```
┌─ SessionManager
│  ├─ Create session when user starts
│  ├─ Store in data/sessions/{user_id}_session.json
│  ├─ Update on every interaction
│  └─ Cleanup after 30 days
│
└─ MemoryService
   ├─ Load user preferences (data/users.csv)
   ├─ Store trip history
   ├─ Track user interactions
   └─ Enable personalization
```

## Callback Flow

```
User Action
    │
    ▼
Process Request
    │
    ├─ [DateValidator] Check dates valid
    │  └─ ERROR: Invalid dates? → Notify user
    │
    ├─ [APIRateLimiter] Check rate limit
    │  └─ ERROR: Too many calls? → Queue request
    │
    ├─ [BudgetValidator] Check budget feasibility
    │  └─ WARNING: Budget low? → Alert user
    │
    ▼
Execute Agent
    │
    ▼
[CostTracker] Track API costs
    ├─ Add cost: OpenAI = +$0.0015
    ├─ Total spent: $12.45
    └─ Check: $12.45 < $100 limit?
    │
    ├─ ERROR: Exceeded budget? → STOP
    ├─ WARNING: Low budget? → Alert
    └─ OK: Continue
    │
    ▼
[EventLogger] Log event
    └─ {timestamp, type, details}
    │
    ▼
Return Response
```

## Hybrid Approach Benefits

```
Google ADK (Agent Reasoning)          LangGraph (Deterministic)
├─ Itinerary generation            ├─ Booking validation flow
├─ Recommendations                 ├─ Payment processing
├─ Personalization                 ├─ Confirmation workflow
├─ Conversation                    └─ Error recovery
└─ User preference learning
```

**Best of Both Worlds:**
- **Google ADK**: For creative, context-aware responses
- **LangGraph**: For reliable, compliant operations

## Deployment Architecture

```
LOCAL DEVELOPMENT
├─ Streamlit dev server (localhost:8501)
├─ JSON/CSV files for data
├─ Mock MCP servers
└─ Single user

PRODUCTION (Future)
├─ FastAPI backend
├─ PostgreSQL for persistence
├─ Real MCP servers
├─ Multi-user support
├─ Redis for sessions
└─ Async execution
```

---

*Architecture designed for scalability and maintainability*
