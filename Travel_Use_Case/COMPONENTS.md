# 📚 Component Documentation

## Table of Contents
1. [Agents](#agents)
2. [Skills](#skills)
3. [Services](#services)
4. [MCP Clients](#mcp-clients)
5. [Data Models](#data-models)

---

## Agents

### 1. **Coordinator Agent** (Google ADK)
**File**: `agents/coordinator_agent.py`

**Purpose**: Orchestrates all other agents based on user intent

**Key Methods**:
- `process(input_data)` - Main entry point
- `_determine_plan()` - Analyzes user input, decides which agents to invoke
- `_execute_plan()` - Executes the determined sequence
- `_generate_response()` - Creates conversational response

**Input**:
```python
{
    "user_input": str,        # User's natural language query
    "user_id": str,           # Unique user identifier
    "session_state": {}       # Current session state
}
```

**Output**:
```python
{
    "success": bool,
    "response": str,          # Conversational response to user
    "actions_taken": [],      # List of agents invoked
    "state_updates": {},      # Session state changes
    "metadata": {}            # Execution details
}
```

**Example**:
```python
user_input = "Plan a 5-day trip to Paris with $3000 budget"
coordinator_result = await coordinator.process({
    "user_input": user_input,
    "user_id": "user123",
    "session_state": {...}
})
# Result: Invokes Destination Research, Itinerary, Budget, Memory agents
```

---

### 2. **Itinerary Agent** (Google ADK) - PRIORITY 1
**File**: `agents/itinerary_agent.py`

**Purpose**: Generate detailed, themed itineraries for trips

**Key Methods**:
- `process(input_data)` - Generate itinerary
- `_generate_itinerary()` - Create day-by-day plan
- `_determine_theme()` - Analyze preferences for activity theme
- `_create_day_plan()` - Create activities for a single day

**Input**:
```python
{
    "destination": str,         # e.g., "Paris"
    "start_date": str,          # e.g., "2024-04-20" or "next weekend"
    "end_date": str,            # e.g., "2024-04-25" or "next sunday"
    "preferences": {
        "activities": [...],    # ["museums", "dining", "museums"]
        "vibe": str,            # "romantic", "cultural", "adventurous"
        "pace": str             # "slow", "moderate", "fast"
    },
    "budget": float,            # Total trip budget
    "user_id": str              # For personalization
}
```

**Output**:
```python
{
    "success": bool,
    "itinerary": {
        "destination": str,
        "duration": int,        # Number of days
        "days": [               # Array of day plans
            {
                "day": 1,
                "date": "2024-04-20",
                "morning": {
                    "activity": "Louvre Museum",
                    "time": "9:00 AM",
                    "duration": "3 hours",
                    "notes": "..."
                },
                "afternoon": {...},
                "evening": {...},
                "meals": {...},
                "transportation": str,
                "tips": [...]
            }
        ],
        "highlights": [...],      # Top activities
        "practical_tips": {...}   # Destination-specific tips
    },
    "summary": str,              # Text summary
    "metadata": {}
}
```

**Themes Supported**:
- `cultural`: Museums, historical sites, temples
- `adventure`: Hiking, water sports, extreme activities
- `relaxation`: Beach, spa, yoga
- `food`: Food tours, cooking classes
- `urban`: Shopping, nightlife
- `mixed`: Balanced mix of activities

**Example**:
```python
itinerary_result = await itinerary_agent.process({
    "destination": "Paris",
    "start_date": "next weekend",
    "end_date": "next sunday",
    "preferences": {"activities": ["museums", "dining"], "vibe": "romantic"},
    "duration": 2
})
# Returns: 2-day romantic Paris itinerary with museum visits and dining
```

---

### 3. **Budget Agent** (Google ADK) - PRIORITY 2
**File**: `agents/budget_agent.py`

**Purpose**: Estimate costs, track spending, validate budget feasibility

**Key Methods**:
- `process(input_data)` - Estimate and validate budget
- `_generate_recommendations()` - Provide cost-saving tips
- `compare_budget_tiers()` - Compare budget/moderate/luxury costs
- `refine_budget()` - Adjust budget based on changes

**Input**:
```python
{
    "destination": str,         # e.g., "Paris"
    "duration": int,            # Number of days
    "budget": float,            # User's budget (optional)
    "budget_tier": str,         # "budget", "moderate", "luxury"
    "user_id": str,             # For cost tracking
    "currency": str             # "USD", "EUR", etc.
}
```

**Output**:
```python
{
    "success": bool,
    "budget_breakdown": {
        "accommodation": {
            "daily": 100.00,
            "total": 500.00
        },
        "food": {
            "daily": 40.00,
            "total": 200.00
        },
        "activities": {
            "daily": 60.00,
            "total": 300.00
        },
        "transport": {
            "daily": 25.00,
            "total": 125.00
        },
        "total": 1125.00
    },
    "feasibility": {
        "is_feasible": bool,      # Is budget sufficient?
        "budget_provided": float,
        "minimum_recommended": float,
        "difference": float,
        "percentage_sufficient": float
    },
    "recommendations": [          # Cost-saving tips
        "⚠️ Budget insufficient by $400...",
        "🏨 Accommodation: $100/night",
        "💡 Consider booking in advance..."
    ]
}
```

**Budget Tiers**:
```
Tier      Accommodation/night  Food/day  Activities/day
─────────────────────────────────────────────────────
Budget    $30                  $15       $20
Moderate  $80                  $40       $60
Luxury    $200                 $100      $150
```

**Destination Multipliers** (adjust base costs):
```
Tokyo:    1.8x (expensive)
Paris:    1.9x (expensive)
Bali:     0.4x (budget-friendly)
Bangkok:  0.5x (budget-friendly)
```

**Example**:
```python
budget_result = await budget_agent.process({
    "destination": "Paris",
    "duration": 5,
    "budget_tier": "moderate",
    "budget": 3000
})
# Returns: Budget breakdown showing ~$1200 needed
# Recommendation: You have extra $1800 for premium experiences!
```

---

### 4. **Booking Helper Agent** (LangGraph Flows) - PRIORITY 3
**File**: `agents/booking_agent.py`

**Purpose**: Search and assist with hotel, flight, activity bookings

**Key Methods**:
- `process(input_data)` - Main booking orchestrator
- `_search_hotels()` - Search hotel options
- `_search_flights()` - Search flights
- `_get_recommendations()` - Personalized booking suggestions

**Input**:
```python
{
    "action": str,              # "search_hotels", "search_flights", "get_recommendations"
    "destination": str,
    "check_in": str,            # YYYY-MM-DD
    "check_out": str,           # YYYY-MM-DD
    "origin": str,              # (for flights) departure city
    "guests": int,              # Number of guests
    "budget_tier": str,         # "budget", "moderate", "luxury"
    "preferences": {}
}
```

**Output**:
```python
{
    "success": bool,
    "results": {
        "hotels": [
            {
                "name": "Hotel name",
                "stars": 4,
                "price_per_night": 120,
                "rating": 4.5,
                "amenities": ["WiFi", "Pool", "Gym"],
                "location": "Downtown"
            }
        ],
        "weather": [...]          # Weather forecast during stay
    },
    "recommendations": [
        "✨ Best Value: ...",
        "💰 Budget Option: ...",
        "👑 Premium Option: ...",
        "💡 Book early for better rates"
    ]
}
```

**Uses LangGraph for**:
- Hotel booking confirmation flow
- Payment validation
- Reservation confirmation
- Error recovery

**Example**:
```python
booking_result = await booking_agent.process({
    "action": "search_hotels",
    "destination": "Paris",
    "check_in": "2024-04-20",
    "check_out": "2024-04-25",
    "guests": 2,
    "budget_tier": "moderate"
})
# Returns: 3+ hotel options with prices and ratings
```

---

### 5. **Memory & Personalization Agent** (Google ADK) - PRIORITY 4
**File**: `agents/memory_agent.py`

**Purpose**: Remember user preferences and provide personalization

**Key Methods**:
- `process(input_data)` - Main entry point
- `_save_preferences()` - Store user preferences
- `_load_preferences()` - Retrieve user profile
- `_get_personalized_recommendations()` - Suggest based on history
- `learn_from_interactions()` - Update preferences from behavior

**Input**:
```python
{
    "action": str,              # "save_preferences", "load_preferences", etc.
    "user_id": str,
    "preferences": {            # (optional for save)
        "name": str,
        "travel_preferences": {
            "activities": [...],
            "vibe": str,
            "pace": str
        },
        "favorite_destinations": [...],
        "budget_preference": str  # "budget", "moderate", "luxury"
    }
}
```

**Output**:
```python
{
    "success": bool,
    "preferences": {...},
    "recommendations": [
        "🎯 Based on your interest in...",
        "❤️ Since you enjoyed...",
        "🌟 Welcome back to..."
    ],
    "memory_score": 0.75,        # 0-1: how much we know about user
    "personalization_level": str # "high" or "low"
}
```

**Memory Score Calculation**:
- Has name: +0.1
- Has preferences: +0.3
- Has favorites: +0.3
- Has budget preference: +0.2
- Total: 0.0-1.0

**Example**:
```python
memory_result = await memory_agent.process({
    "action": "load_preferences",
    "user_id": "user123"
})
# Returns: Stored preferences with memory_score = 0.85
# Recommendations: "Welcome back! Based on your love of Paris museums..."
```

---

### 6. **Destination Research Agent** (Google ADK)
**File**: `agents/coordinator_agent.py`

**Purpose**: Research destinations and provide information

**Key Methods**:
- `process(input_data)` - Main entry point
- `_search_destinations()` - Search by keywords
- `_recommend_destinations()` - Match preferences to destinations
- `_get_destination_info()` - Get detailed info about a destination

**Destinations Supported**:
- Paris, Tokyo, Bali, New York (expandable)

---

## Skills

### 1. **BudgetEstimationSkill**
**File**: `skills/travel_skills.py`

```python
class BudgetEstimationSkill:
    @staticmethod
    def estimate_budget(destination, duration, tier) -> breakdown
    @staticmethod
    def validate_budget(budget, destination, duration) -> feasibility
```

**Cost Database**:
```python
COST_ESTIMATES = {
    "accommodation": {"budget": 30, "moderate": 80, "luxury": 200},
    "food": {"budget": 15, "moderate": 40, "luxury": 100},
    "activities": {"budget": 20, "moderate": 60, "luxury": 150},
    "transport": {"budget": 10, "moderate": 25, "luxury": 50}
}

DESTINATION_MULTIPLIERS = {
    "tokyo": 1.8,
    "paris": 1.9,
    "bali": 0.4,
    "bangkok": 0.5
}
```

---

### 2. **DestinationMatchingSkill**
**File**: `skills/travel_skills.py`

```python
class DestinationMatchingSkill:
    @staticmethod
    def match_destinations(preferences, num_results=5) -> list[Match]
```

Matches destinations based on:
- Activities (hiking, diving, museums, etc.)
- Vibe (relaxing, cultural, energetic)
- Region preference

---

### 3. **ItineraryFormattingSkill**
**File**: `skills/travel_skills.py`

```python
class ItineraryFormattingSkill:
    @staticmethod
    def format_day_plan(day, activities, restaurants, accommodation) -> plan
    @staticmethod
    def create_itinerary_structure(destination, duration, theme) -> structure
```

---

### 4. **CurrencyConversionSkill**
**File**: `skills/travel_skills.py`

```python
class CurrencyConversionSkill:
    @staticmethod
    def convert_currency(amount, from_currency, to_currency) -> result
```

Supports: USD, EUR, GBP, JPY, INR, IDR, THB

---

## Services

### 1. **Session Manager**
**File**: `services/session_memory.py`

**Purpose**: Persist session state across restarts

```python
class SessionManager:
    def create_session(user_id) -> session
    def get_session(user_id) -> session
    def update_session(user_id, updates) -> None
    def cleanup_old_sessions() -> None
```

**Data Structure**:
```python
{
    "user_id": str,
    "created_at": str,          # ISO timestamp
    "last_accessed": str,
    "messages": [...],          # Chat history
    "state": {
        "destination": str,
        "start_date": str,
        "end_date": str,
        "budget": float,
        "preferences": {},
        "itinerary_generated": bool
    }
}
```

**Storage**: `data/sessions/{user_id}_session.json`

**Policy**: Keep last 5 sessions, expire after 30 days

---

### 2. **Memory Service**
**File**: `services/session_memory.py`

**Purpose**: Store user preferences and history

```python
class MemoryService:
    def save_user_preferences(user_id, preferences) -> None
    def load_user_preferences(user_id) -> preferences
    def store_memory(user_id, key, value) -> None
    def recall_memory(user_id, key) -> value
```

**Files**:
- `data/users.csv` - User profiles
- `data/{user_id}_memory.json` - Key-value memory storage

---

### 3. **Callback System**
**File**: `services/callbacks.py`

#### **CostTracker**
```python
class CostTracker:
    def add_cost(provider, amount, details) -> None
    def validate_budget() -> (is_valid, message)
    def get_cost_summary() -> summary
```

Tracks:
- OpenAI costs
- Google ADK costs
- Total spending

**Storage**: `data/sessions/{user_id}_costs.json`

#### **EventLogger**
```python
class EventLogger:
    def log_event(event_type, details) -> None
```

Logs all events for debugging and auditing.

**Storage**: `data/sessions/{user_id}_events.json`

#### **Validators**
```python
class DateValidator:
    @staticmethod
    def validate_dates(start_date, end_date) -> (is_valid, message)

class BudgetValidator:
    @staticmethod
    def validate_budget_feasibility(destination, budget, duration) -> (is_valid, message)

class APIRateLimiter:
    def is_allowed() -> bool
    def wait_if_needed() -> None
```

---

### 4. **MCP Clients**
**File**: `services/mcp_clients.py`

#### **WeatherMCPClient**
```python
async def get_weather_forecast(location, days=7) -> forecast
```

Returns: Temperature, conditions, humidity, wind speed

#### **HotelFlightMCPClient**
```python
async def search_hotels(destination, check_in, check_out, guests, budget_tier) -> hotels
async def search_flights(origin, destination, departure, return, passengers) -> flights
```

#### **CurrencyConversionMCPClient**
```python
async def convert_currency(amount, from_currency, to_currency) -> result
```

**All clients have mock data fallback for development**

---

## Data Models

### Session State
```python
{
    "destination": Optional[str],
    "start_date": Optional[str],      # ISO format or relative
    "end_date": Optional[str],
    "budget": Optional[float],
    "preferences": Optional[Dict],
    "itinerary_generated": bool,
    "current_trip_id": Optional[str]
}
```

### User Preferences
```python
{
    "name": str,
    "travel_preferences": {
        "activities": List[str],
        "vibe": str,
        "pace": str
    },
    "favorite_destinations": List[str],
    "budget_preference": str
}
```

### Itinerary
```python
{
    "destination": str,
    "duration": int,
    "days": [
        {
            "day": int,
            "date": str,
            "morning": {activity, time, duration, notes},
            "afternoon": {...},
            "evening": {...},
            "meals": {...},
            "transportation": str,
            "tips": List[str]
        }
    ],
    "highlights": List[str],
    "practical_tips": Dict
}
```

---

*For more details, see individual source files in their respective directories.*
