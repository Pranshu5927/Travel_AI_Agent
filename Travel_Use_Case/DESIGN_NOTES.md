# 📐 Design Notes & Architecture Decisions

## Table of Contents
1. [Design Philosophy](#design-philosophy)
2. [Callback System Design](#callback-system-design)
3. [Session & Memory Design](#session--memory-design)
4. [Skill Architecture](#skill-architecture)
5. [MCP Integration](#mcp-integration)
6. [Agent Design Patterns](#agent-design-patterns)
7. [Hybrid Approach Rationale](#hybrid-approach-rationale)
8. [Scalability & Future Work](#scalability--future-work)

---

## Design Philosophy

### Core Principles

1. **Modularity**: Each component is independently testable and replaceable
2. **Extensibility**: Easy to add new agents, skills, MCP integrations
3. **Observability**: Every action is logged and traceable
4. **Fault Tolerance**: Graceful degradation with fallbacks
5. **User Privacy**: Local-first data storage, no unnecessary cloud calls

### Decision: Google ADK + LangGraph Hybrid

We chose a **hybrid approach** rather than pure agent reasoning because:

| Aspect | Google ADK | LangGraph | Solution |
|--------|-----------|-----------|----------|
| **Reasoning** | ✅ Excellent | ❌ Limited | Use ADK for creative tasks |
| **Determinism** | ❌ Variable | ✅ Guaranteed | Use LangGraph for critical flows |
| **Compliance** | ❌ Hard to audit | ✅ Traceable | LangGraph for bookings |
| **Speed** | ❌ Slower | ✅ Fast | LangGraph for validation |

**Result**: 
- Google ADK: Itinerary generation, recommendations, personalization
- LangGraph: Booking flows, payment validation, compliance

---

## Callback System Design

### Why Callbacks Matter

Travel planning involves **real costs** and **real constraints**:
- API costs accumulate (OpenAI: $0.0025/token)
- User budgets are hard limits
- Compliance requirements exist (payment, date validity)

### Three-Layer Callback Architecture

```
Layer 1: PRE-EXECUTION (Input Validation)
├─ DateValidator: "Is end date after start date?"
├─ BudgetValidator: "Is budget realistic for destination?"
└─ APIRateLimiter: "Have we exceeded rate limit?"

Layer 2: EXECUTION (Tracking)
├─ CostTracker: "Add $0.15 for this OpenAI call"
└─ EventLogger: "Log that user viewed itinerary"

Layer 3: POST-EXECUTION (Validation)
├─ CostTracker: "Total spent: $45.20, Budget: $100 - OK"
├─ BudgetValidator: "Still under budget warning threshold"
└─ EventLogger: "Record final state for audit"
```

### Cost Tracking Implementation

```python
# Every time an expensive operation occurs:
cost_tracker = get_cost_tracker("user123", budget=100)

# OpenAI call for itinerary generation
response = await openai_api.create_completion(...)
cost_tracker.add_cost("openai", 0.0015, {"tokens": 500})

# Google ADK call for recommendations  
response = await google_api.generate_recommendations(...)
cost_tracker.add_cost("google", 0.005, {"api": "google"})

# Budget validation
is_valid, message = cost_tracker.validate_budget()
if not is_valid:
    return {"error": message, "spent": cost_tracker.total_cost}
```

### Why JSON Files for Persistence?

**Costs** need to be:
- ✅ Persistent (survive app restarts)
- ✅ Queryable (show cost history)
- ✅ Portable (export for reports)
- ✅ Simple (no database setup)

JSON files satisfy all these requirements for single-user local deployment.

---

## Session & Memory Design

### Session vs Memory: What's the Difference?

| Aspect | Session | Memory |
|--------|---------|--------|
| **Scope** | Current trip planning | Across all trips |
| **Lifespan** | Until trip complete | Permanent (unless deleted) |
| **Example** | "Current itinerary draft" | "User prefers museums" |
| **Storage** | `{user_id}_session.json` | `users.csv` + `{user_id}_memory.json` |

### Session State Machine

```
[Empty]
  │
  ├─ User provides destination
  │  └─ [Destination Set]
  │      │
  │      ├─ User provides dates
  │      │  └─ [Dates Set]
  │      │      │
  │      │      ├─ User provides budget
  │      │      │  └─ [Budget Set]
  │      │      │
  │      │      └─ User asks for itinerary
  │      │         └─ [Itinerary Generated]
  │      │
  │      └─ User changes destination
  │         └─ [Reset] → [Empty]
  │
  └─ User asks general question
     └─ [General Chat]
```

### Why Keep 5 Sessions?

```
Max Sessions = 5 means:
- User can plan 5 trips simultaneously
- Each session is independent
- No loss of previous work
- Clear UI showing all trips

More than 5 would:
- Clutter UI
- Consume disk space
- Slow down session management

Less than 5 would:
- Force users to delete old trips
- Lose planning context
```

### Memory Scoring Algorithm

We calculate `memory_score` (0.0 to 1.0) to measure how much we know:

```python
def calculate_memory_score(preferences):
    score = 0.0
    
    if preferences.get("name"):
        score += 0.1  # We know their name
    
    if preferences.get("travel_preferences"):
        score += 0.3  # We know activity preferences
    
    if preferences.get("favorite_destinations"):
        score += 0.3  # We know where they like to go
    
    if preferences.get("budget_preference"):
        score += 0.2  # We know budget comfort level
    
    return score  # 0.0 (new user) to 1.0 (full profile)
```

**Why this matters**:
- Score 0.0-0.3: Treat as new user, ask lots of questions
- Score 0.3-0.7: Some personalization possible
- Score 0.7-1.0: Heavy personalization, quick recommendations

---

## Skill Architecture

### Why Separate "Skills" from "Agents"?

```
Agents (Context-aware)              Skills (Stateless)
├─ Make decisions                   ├─ Execute actions
├─ Remember conversation            ├─ Reusable functions
├─ Handle errors                    ├─ Pure logic
└─ Complex reasoning                └─ Testable

Example:
Itinerary Agent needs to estimate costs
  → Uses BudgetEstimationSkill
  → Skill calculates independently
  → Agent uses result in decision-making
```

### Skill Composition Pattern

```python
# Agents use skills like building blocks

class ItineraryAgent:
    async def process(self, input_data):
        # Use currency conversion skill
        converted_budget = CurrencyConversionSkill.convert_currency(
            amount=input_data["budget"],
            from_currency="USD",
            to_currency=input_data["currency"]
        )
        
        # Use formatting skill
        itinerary = ItineraryFormattingSkill.create_itinerary_structure(
            destination=input_data["destination"],
            duration=input_data["duration"],
            theme=theme
        )
        
        # Return formatted result
        return itinerary
```

### Why These 4 Skills?

| Skill | Used By | Frequency | Complexity |
|-------|---------|-----------|-----------|
| **Budget Estimation** | Budget Agent, Coordinator | Every trip | Medium |
| **Destination Matching** | Destination Research | On request | Low |
| **Itinerary Formatting** | Itinerary Agent | Every trip | Low |
| **Currency Conversion** | Budget Agent, Booking | On demand | Low |

**To Add New Skills**:
1. Create class inheriting `BaseSkill`
2. Implement `@staticmethod` methods (stateless)
3. Register in skill factory
4. Use in agents

---

## MCP Integration

### Why MCP (Model Context Protocol)?

Traditional integration has problems:
```python
# ❌ Direct API calls = tight coupling
def get_weather(location):
    return openweathermap_api.get(location)
    # Hard to test, hard to swap providers

# ✅ MCP wrapper = loose coupling
def get_weather(location):
    return mcp_client.get_weather(location)
    # Easy to mock, easy to swap
```

### MCP Client Pattern

```python
class WeatherMCPClient:
    async def get_weather_forecast(location, days):
        try:
            # Try to call real MCP server
            response = await mcp_server.call(
                resource="weather",
                action="get_forecast",
                params={...}
            )
            return response
        except ConnectionError:
            # Fall back to mock data for development
            return self._mock_weather_data(location, days)
```

**Benefits**:
- Real data in production
- Mock data in development
- No external dependencies required
- Easy to test

### Why These 3 MCP Services?

| Service | Use Case | Availability |
|---------|----------|--------------|
| **Weather** | Show forecast during trip | High |
| **Hotels/Flights** | Key booking decisions | High |
| **Currency** | Budget conversion | High |

Alternative MCPs (future):
- Maps/Distance for activity routing
- Restaurant reviews for food recommendations
- Event calendars for activity timing

---

## Agent Design Patterns

### Pattern 1: BaseAgent Interface

All agents implement the same contract:

```python
class BaseAgent(ABC):
    @abstractmethod
    async def process(self, input_data: Dict) -> Dict:
        """
        Process input and return output.
        Every agent must implement this.
        """
        pass
    
    def validate_input(self, required_fields, data):
        """Helper for input validation"""
        
    def log_action(self, action, details):
        """Helper for logging"""
```

**Benefits**:
- Consistent interface
- Easy to compose agents
- Simple testing
- Easy to replace agents

### Pattern 2: Agent Priority Order

```
User Query
  │
  ├─ Priority 1: Memory Agent
  │  └─ Load user context, preferences
  │     └─ Used by: All other agents
  │
  ├─ Priority 2: Coordinator Agent
  │  └─ Determine which agents to invoke
  │     └─ Routes to 3+ agents
  │
  ├─ Priority 3: Primary Agent (based on query)
  │  ├─ Destination Research (if asking about places)
  │  ├─ Itinerary (if asking about activities)
  │  ├─ Budget (if asking about costs)
  │  └─ Booking (if asking about reservations)
  │
  └─ Priority 4: Response Agent
     └─ Format all results into response
```

### Pattern 3: Agent Composition

```python
async def execute_query(user_input):
    # Create agent chain
    chain = AgentChain([
        memory_agent,        # Load context
        coordinator_agent,   # Determine plan
        destination_agent,   # Research if needed
        itinerary_agent,     # Generate if needed
        budget_agent,        # Calculate if needed
        booking_agent        # Search if needed
    ])
    
    # Execute in sequence
    result = await chain.execute({
        "user_input": user_input,
        "user_id": user_id
    })
    
    return result
```

---

## Hybrid Approach Rationale

### The Problem with Pure Google ADK

```python
# Pure ADK = everything goes through LLM reasoning
async def plan_trip(user_input):
    # Even for booking confirmation, we ask the model
    response = await google_adk_agent.process(user_input)
    # Model might decide to book without confirmation!
    # Or add payment without validation!
    # Too much freedom = too much risk
```

### The Problem with Pure LangGraph

```python
# Pure LangGraph = everything is deterministic
async def plan_trip(user_input):
    # Generate itinerary (if-else logic)
    if destination == "Paris":
        itinerary = predefined_paris_itinerary
    elif destination == "Tokyo":
        itinerary = predefined_tokyo_itinerary
    else:
        return "I only know Paris and Tokyo"
    # No creativity, no personalization, boring!
```

### The Hybrid Solution

```python
# Google ADK for creative thinking
class ItineraryAgent:  # Uses Google ADK
    async def generate(destination, preferences):
        # "What would be a perfect 3-day Paris itinerary
        #  for someone who loves museums and food?"
        response = await google_adk.generate_itinerary(...)
        # Result: Creative, personalized itinerary

# LangGraph for critical operations
class BookingFlow:  # Uses LangGraph
    async def confirm_booking(hotel_id, user_id):
        # 1. Validate: Is user's budget sufficient?
        # 2. Confirm: Show user exact charges
        # 3. Process: Safe payment workflow
        # 4. Record: Log everything
        # No model reasoning in critical path!
```

### What Goes Where?

```
Google ADK (Reasoning)           LangGraph (Determinism)
├─ Recommendations              ├─ Booking workflow
├─ Personalization              ├─ Payment validation
├─ Creative suggestions         ├─ Compliance checks
├─ Conversation handling        ├─ State machines
├─ User preference learning     ├─ Error recovery
└─ Context-aware responses      └─ Audit trails
```

---

## Scalability & Future Work

### Current (Single User)
```
Streamlit Frontend
    │
    └─ File System (JSON/CSV)
       ├─ Sessions: data/sessions/
       ├─ Users: data/users.csv
       └─ History: event logs
```

### Future (Multi-User)
```
React Frontend ── FastAPI Backend ── PostgreSQL DB
                     │
                     ├─ Redis (sessions)
                     ├─ Celery (async tasks)
                     ├─ Google ADK (agentic)
                     └─ LangGraph (flows)
```

### Phase 2 Improvements

1. **Database Migration**
   - CSV → PostgreSQL
   - Sessions → Redis
   - Transactions for consistency

2. **Authentication**
   - JWT tokens
   - Google/GitHub OAuth
   - Rate limiting per user

3. **Async Processing**
   - Long itinerary generation → background job
   - Email notifications
   - Batch processing

4. **Advanced Features**
   - Real-time collaboration
   - Team trip planning
   - Booking integration APIs
   - Travel insurance
   - Travel insurance
   - Dynamic pricing

5. **Analytics**
   - User behavior tracking
   - Popular destinations
   - Budget trends
   - Recommendation effectiveness

### Performance Considerations

**Current Targets**:
- Itinerary generation: < 5 seconds
- Budget calculation: < 1 second  
- Session load: < 100ms
- MCP API calls: < 3 seconds

**Optimization Opportunities**:
- Cache destination information
- Pre-compute common itineraries
- Async MCP calls
- Response streaming
- Database indexing

---

## Lessons Learned

### 1. Keep Costs Visible
Initially, we didn't track OpenAI costs. After first 100 API calls, realized ~$20 spent without awareness. **Now**: Every call logged with cost.

### 2. Session Persistence is Critical
Lost user's trip planning when app crashed. **Now**: Auto-save after every action.

### 3. Fallback Data Saves Sessions
When weather API was down, entire flow crashed. **Now**: Mock data prevents failures.

### 4. Validation > Trust
Assumed budget input was always valid. User entered "3k" not "3000". **Now**: Validators everywhere.

### 5. Agent Composition > Monolith
Single large agent did everything, was hard to test/modify. **Now**: Small focused agents, easy to test.

---

## References

- **Google ADK**: https://adk.dev
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **MCP Spec**: https://modelcontextprotocol.io/
- **System Design Patterns**: https://refactoring.guru/design-patterns

---

*Document updated: April 2024*
