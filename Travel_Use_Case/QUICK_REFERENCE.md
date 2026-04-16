# 📖 Quick Reference Guide

## 🎯 Start Here

**New to this project?** Read in this order:

1. **[README_v2.md](README_v2.md)** - Project overview (5 min read)
2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What was built (10 min read)
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - How it works (15 min read)

---

## 📁 File Structure & Quick Links

### 🤖 Agent Implementations

| File | Purpose | Key Class |
|------|---------|-----------|
| [agents/base_agent.py](agents/base_agent.py) | Base class for all agents | `BaseAgent`, `AgentChain` |
| [agents/coordinator_agent.py](agents/coordinator_agent.py) | Routes requests + Destination Research | `CoordinatorAgent`, `DestinationResearchAgent` |
| [agents/itinerary_agent.py](agents/itinerary_agent.py) | **PRIORITY 1** - Generates itineraries | `ItineraryAgent` |
| [agents/budget_agent.py](agents/budget_agent.py) | **PRIORITY 2** - Cost estimation | `BudgetAgent` |
| [agents/booking_agent.py](agents/booking_agent.py) | **PRIORITY 3** - Hotel/flight search | `BookingHelperAgent` |
| [agents/memory_agent.py](agents/memory_agent.py) | **PRIORITY 4** - Personalization | `MemoryPersonalizationAgent` |
| [agents/__init__.py](agents/__init__.py) | Agent exports | All agents + registry |

**Quick Start**: See `COMPONENTS.md` Agent section for full API documentation

---

### 💼 Skills (Reusable Domain Logic)

| File | Skills | Classes |
|------|--------|---------|
| [skills/travel_skills.py](skills/travel_skills.py) | 4 domain skills | `BudgetEstimationSkill`, `DestinationMatchingSkill`, `ItineraryFormattingSkill`, `CurrencyConversionSkill` |
| [skills/__init__.py](skills/__init__.py) | Exports | All skills |

**What they do**:
- **BudgetEstimationSkill**: Estimate costs, validate budget
- **DestinationMatchingSkill**: Match user preferences to destinations
- **ItineraryFormattingSkill**: Format day plans consistently
- **CurrencyConversionSkill**: Convert between currencies

**Usage**: `from skills import BudgetEstimationSkill`

---

### ⚙️ Services (Core Infrastructure)

| File | Services | Purpose |
|------|----------|---------|
| [services/callbacks.py](services/callbacks.py) | 5 callback types | Cost tracking, validation, logging |
| [services/session_memory.py](services/session_memory.py) | Session + Memory | Persistence, user profiles |
| [services/mcp_clients.py](services/mcp_clients.py) | 3 MCP clients | External data integration |
| [services/__init__.py](services/__init__.py) | Exports | All services |

**Callbacks** (services/callbacks.py):
- `CostTracker` - Track API costs (MAIN PRIORITY)
- `DateValidator` - Validate travel dates
- `BudgetValidator` - Check budget feasibility
- `APIRateLimiter` - Prevent quota exceeded
- `EventLogger` - Audit trail logging

**Session & Memory** (services/session_memory.py):
- `SessionManager` - JSON file-based sessions
- `MemoryService` - User preferences + learning

**MCP Clients** (services/mcp_clients.py):
- `WeatherMCPClient` - Get weather forecasts
- `HotelFlightMCPClient` - Search hotels/flights
- `CurrencyConversionMCPClient` - Exchange rates

---

### 📚 Documentation Files

| File | Content | Length |
|------|---------|--------|
| [README_v2.md](README_v2.md) | Project overview, quick start | 400 lines |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Completion summary, statistics | 500 lines |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design, diagrams, data flows | 800 lines |
| [COMPONENTS.md](COMPONENTS.md) | Agent/skill/service APIs, examples | 1000 lines |
| [DESIGN_NOTES.md](DESIGN_NOTES.md) | Design decisions, patterns, rationale | 800 lines |
| [TEST_CASES.md](TEST_CASES.md) | Test cases, examples, edge cases | 700 lines |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | This file! | Navigation guide |

---

## 🔍 Finding What You Need

### "How do I...?"

| Question | File | Location |
|----------|------|----------|
| **Understand the system?** | ARCHITECTURE.md | Section: Architecture Overview |
| **Use the Budget Agent?** | COMPONENTS.md | Section: Budget Agent |
| **Implement a new agent?** | agents/base_agent.py | Class: BaseAgent |
| **Add a new skill?** | skills/travel_skills.py | Any skill class |
| **Track costs?** | services/callbacks.py | Class: CostTracker |
| **Save preferences?** | services/session_memory.py | Class: MemoryService |
| **Run the app?** | README_v2.md | Section: Quick Start |
| **See examples?** | TEST_CASES.md | Section: Sample Conversations |
| **Understand design?** | DESIGN_NOTES.md | Full document |

---

## 🎯 Key Concepts Quick Explanation

### Agents
- **What**: Specialized AI entities that handle specific domains
- **How**: Google ADK for reasoning
- **Why**: Modular, extensible architecture
- **Files**: `agents/` directory
- **Docs**: COMPONENTS.md → Agents section

### Skills
- **What**: Reusable domain-specific logic
- **How**: Static methods, no state
- **Why**: Shareable, testable, composable
- **Files**: `skills/travel_skills.py`
- **Docs**: COMPONENTS.md → Skills section

### Services
- **What**: Core infrastructure components
- **How**: Session manager, memory, callbacks, MCP
- **Why**: Separation of concerns
- **Files**: `services/` directory
- **Docs**: COMPONENTS.md → Services section

### Callbacks
- **What**: Pre/during/post action validation
- **How**: Cost tracking, validation, logging
- **Why**: Safety, compliance, observability
- **Files**: `services/callbacks.py`
- **Docs**: DESIGN_NOTES.md → Callback System Design

### MCP (Model Context Protocol)
- **What**: External data integration
- **How**: Loose coupling to APIs
- **Why**: Easy to test, swap providers
- **Files**: `services/mcp_clients.py`
- **Docs**: DESIGN_NOTES.md → MCP Integration

---

## 📊 Data & Persistence

### File Locations

```
data/
├── users.csv                    # User profiles
├── sessions/
│   ├── {user_id}_session.json  # Current trip state
│   ├── {user_id}_costs.json    # Cost tracking
│   └── {user_id}_events.json   # Event audit trail
├── trips.csv                    # Trip history (future)
└── bookings.csv                 # Booking history (future)
```

### What Gets Saved Where

| Data | File | Format | Purpose |
|------|------|--------|---------|
| User Preferences | users.csv | CSV | Load preferences next time |
| Session State | {user_id}_session.json | JSON | Resume trip planning |
| API Costs | {user_id}_costs.json | JSON | Track spending |
| Events | {user_id}_events.json | JSON | Debugging, audit |

---

## 🧪 Testing & Examples

### Run All Tests
```bash
pytest tests/ -v
```

### See Examples
- **Sample Conversations**: TEST_CASES.md → Sample Conversations section
- **Test Cases**: TEST_CASES.md → Test Cases section
- **Edge Cases**: TEST_CASES.md → Edge Cases section

### Example Conversation
See TEST_CASES.md "Conversation 1: Basic Trip Planning" for realistic flow

---

## ⚡ Quick API Reference

### Create a Session
```python
from services import get_session_manager

session_mgr = get_session_manager()
session = session_mgr.create_session("user123")
```

### Track Costs
```python
from services import get_cost_tracker

tracker = get_cost_tracker("user123", budget=100)
tracker.add_cost("openai", 0.0015)
is_valid, msg = tracker.validate_budget()
```

### Save Preferences
```python
from services import get_memory_service

memory = get_memory_service()
memory.save_user_preferences("user123", {
    "travel_preferences": {...},
    "favorite_destinations": [...]
})
```

### Use a Skill
```python
from skills import BudgetEstimationSkill

breakdown = BudgetEstimationSkill.estimate_budget(
    "Paris", 5, "moderate"
)
```

### Use an Agent
```python
from agents import ItineraryAgent

agent = ItineraryAgent()
result = await agent.process({
    "destination": "Paris",
    "duration": 5,
    "preferences": {...}
})
```

---

## 📋 Checklist for Developers

### Before Adding Features
- [ ] Read ARCHITECTURE.md for system overview
- [ ] Read DESIGN_NOTES.md for patterns
- [ ] Check COMPONENTS.md for existing APIs
- [ ] Review TEST_CASES.md for testing approach

### When Adding an Agent
- [ ] Inherit from BaseAgent in agents/base_agent.py
- [ ] Implement async process() method
- [ ] Add validation with validate_input()
- [ ] Use log_action() for debugging
- [ ] Register in agent registry
- [ ] Write unit tests
- [ ] Update COMPONENTS.md

### When Adding a Skill
- [ ] Create static methods (no state)
- [ ] Add to skill factory in __init__.py
- [ ] Write unit tests
- [ ] Document in COMPONENTS.md

### When Adding a Callback
- [ ] Inherit relevant base class
- [ ] Add to callbacks.py
- [ ] Integrate with agents/services
- [ ] Test for edge cases
- [ ] Document in DESIGN_NOTES.md

---

## 🚀 Getting Started

### 1. Run the App
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 2. Understand the Code
```bash
# Read these in order:
1. README_v2.md           (overview)
2. ARCHITECTURE.md        (design)
3. agents/base_agent.py   (base class)
4. agents/itinerary_agent.py (example)
```

### 3. Test the System
```bash
# See TEST_CASES.md for examples
pytest tests/ -v
```

### 4. Extend It
```bash
# Follow patterns in DESIGN_NOTES.md
# Use COMPONENTS.md for API reference
```

---

## 📞 Where to Find Answers

| Question Type | Source | Location |
|---------------|--------|----------|
| How does X work? | ARCHITECTURE.md | System Architecture section |
| What is X? | COMPONENTS.md | Component documentation |
| Why did we design it this way? | DESIGN_NOTES.md | Design philosophy section |
| How do I use X? | COMPONENTS.md | API reference section |
| What are edge cases? | TEST_CASES.md | Edge Cases section |
| Can I see an example? | TEST_CASES.md | Sample Conversations |
| How do I set up? | README_v2.md | Quick Start section |
| What's complete? | PROJECT_SUMMARY.md | Completed Deliverables |

---

## 💡 Tips & Tricks

### Debugging
- Check `data/sessions/{user_id}_events.json` for event logs
- Check `data/sessions/{user_id}_costs.json` for cost tracking
- Use `log_action()` in agents for debug output

### Testing
- See TEST_CASES.md for edge cases
- Run sample conversations in TEST_CASES.md
- Use mock MCP clients for development

### Extending
- Use skill pattern for reusable logic
- Use agent pattern for reasoning tasks
- Use LangGraph for deterministic flows
- Always add logging and error handling

### Performance
- Cache destination information
- Batch API calls where possible
- Use async/await for I/O
- Monitor cost tracker for unexpected expenses

---

## 📦 Dependencies

See `requirements.txt` for complete list. Key packages:
- `google-adk` - Agent reasoning
- `langchain` - LLM orchestration
- `langgraph` - Workflow management
- `streamlit` - Web interface
- `python-dotenv` - Configuration
- `pydantic` - Data validation

---

## ✅ Verification Checklist

When the system is ready, verify:
- [ ] All 6 agents initialized
- [ ] All 4 skills loadable
- [ ] Session manager creates JSON files
- [ ] Cost tracker logs expenses
- [ ] MCP clients handle fallback
- [ ] App starts on localhost:8501
- [ ] Trip can be created and saved
- [ ] Preferences can be saved/loaded

---

## 🎓 Learning Path

**Beginner**: 
1. README_v2.md
2. ARCHITECTURE.md overview
3. Run app.py
4. Try sample conversations

**Intermediate**:
1. COMPONENTS.md
2. DESIGN_NOTES.md
3. agents/base_agent.py
4. agents/itinerary_agent.py

**Advanced**:
1. All agent implementations
2. skills/travel_skills.py
3. services/callbacks.py
4. Extend with new agent

---

**Last Updated**: April 17, 2024
**Project Status**: ✅ Complete
**Version**: 2.0.0

---

*For detailed help, consult the documentation files. For quick answers, use this reference guide!*
