# 🌍 Travel AI Agent - Multi-Agent System v2

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google ADK](https://img.shields.io/badge/Google-ADK-red.svg)](https://adk.dev)
[![Status: In Development](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()

A sophisticated **multi-agent travel planning system** that combines Google Agent Development Kit (ADK) for intelligent reasoning with LangGraph for deterministic workflows. Plan your perfect trip through natural language conversations with an intelligent agent network that remembers preferences, estimates budgets, and provides personalized recommendations.

## 🎯 What's New (v2.0)

This is a complete architectural overhaul from v1:

| Feature | v1 (LangChain) | v2 (ADK + LangGraph) |
|---------|---|---|
| **Agents** | 1 monolithic agent | 6 specialized agents |
| **Skills** | Inline logic | 4 reusable skills |
| **Persistence** | No memory | User preferences + sessions |
| **Cost Tracking** | None | Full cost monitoring & callbacks |
| **External Data** | None | MCP integrations (weather, hotels, flights) |
| **Data Storage** | RAM only | JSON + CSV files |
| **Determinism** | N/A | LangGraph for bookings |

---

## ✨ Features

### 🤖 Multi-Agent Architecture

**6 Specialized Agents** (Google ADK):
- **Coordinator Agent**: Routes requests to appropriate agents
- **Itinerary Agent**: Generates day-by-day activity plans
- **Budget Agent**: Estimates costs and tracks spending
- **Destination Research Agent**: Researches and recommends destinations
- **Memory & Personalization Agent**: Learns and remembers user preferences
- **Booking Helper Agent**: Searches for hotels, flights, activities

### 🧠 Intelligent Planning
- **Natural Language**: Understand "Plan a trip to Paris next weekend"
- **Context Awareness**: Remember preferences across conversations
- **Personalized Recommendations**: Learn from user behavior
- **Smart Validation**: Check budget feasibility before planning

### 💰 Cost & Budget Management
- **Cost Tracking**: Monitor every API call and expense
- **Budget Validation**: Warn if trip exceeds budget
- **Detailed Breakdown**: Accommodation, food, activities, transport
- **Tier Comparison**: Budget vs. Moderate vs. Luxury options

### 📅 Comprehensive Planning
- **Day-by-Day Itineraries**: Morning, afternoon, evening activities
- **Flexible Dates**: "Next weekend", "in 3 days", specific dates
- **Theme-Based**: Cultural, adventure, relaxation, food-focused
- **Multiple Trips**: Manage 5 concurrent trip plans

### 🌐 External Integrations (MCP)
- **Weather Lookup**: Forecast for your destination during trip
- **Hotel Search**: Filter by budget tier and amenities
- **Flight Search**: Compare prices across airlines
- **Currency Conversion**: Convert budget to local currency

### 💾 Persistent Memory
- **User Profiles**: Save preferences and favorite destinations
- **Trip History**: Revisit and modify past trips
- **Session State**: Auto-save every interaction
- **Event Logging**: Full audit trail for debugging

### 🔒 Safety & Compliance
- **Budget Guardrails**: Don't exceed user budget
- **Date Validation**: Realistic travel dates
- **Rate Limiting**: Prevent API quota exceeded
- **Cost Awareness**: Every operation has a logged cost

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────┐
│     STREAMLIT WEB INTERFACE         │
│    (Chat UI + Trip Management)      │
└────────────┬────────────────────────┘
             │
    ┌────────▼──────────┐
    │  Session Manager  │  ← JSON persistence
    │  Memory Service   │  ← CSV user data
    └────────┬──────────┘
             │
    ┌────────▼────────────────────────┐
    │  Callback System & Validators   │
    ├─ Cost Tracking                  │
    ├─ Budget Validation              │
    ├─ Date Validation                │
    ├─ Rate Limiting                  │
    └────────┬────────────────────────┘
             │
    ┌────────▼────────────────────────────────┐
    │    Agent Orchestration Layer            │
    │  (Coordinator Agent - Google ADK)       │
    └────┬────┬────┬────┬────┬────────────────┘
         │    │    │    │    │
    ┌────▼────┬───┬──┬──┬────▼──────┐
    │Dest.    │Itin.│Bud.│Booking  │Memory
    │Research │    │    │Helper    │&Pers.
    │(ADK)    │(ADK)│(AD│(LangGr.) │(ADK)
    └────┬────┴───┬──┴──┴────┬─────┘
         │        │          │
    ┌────▼────────▼──────────▼──────┐
    │     Skills Layer               │
    ├─ Budget Estimation             │
    ├─ Destination Matching          │
    ├─ Itinerary Formatting          │
    └─ Currency Conversion           │
         │
    ┌────▼───────────────────────┐
    │  MCP Integrations          │
    ├─ Weather lookup            │
    ├─ Hotel/Flight search       │
    └─ Currency conversion       │
```

### Directory Structure

```
Travel_Use_Case/
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Base class and registry
│   ├── coordinator_agent.py    # Routes requests + Destination Research
│   ├── itinerary_agent.py      # Generates itineraries
│   ├── budget_agent.py         # Cost estimation & tracking
│   ├── booking_agent.py        # Hotel/flight search
│   └── memory_agent.py         # Preferences & personalization
│
├── skills/                      # Reusable domain skills
│   ├── __init__.py
│   └── travel_skills.py        # All 4 skills
│
├── services/                    # Core services
│   ├── __init__.py
│   ├── callbacks.py            # Cost tracker, validators, logger
│   ├── session_memory.py       # Session & memory management
│   └── mcp_clients.py          # MCP integrations
│
├── flows/                       # LangGraph workflows
│   └── __init__.py
│
├── mcp_servers/                 # MCP server implementations
│   └── __init__.py
│
├── data/                        # User data (persistent)
│   ├── users.csv               # User profiles
│   ├── trips.csv               # Trip history
│   ├── bookings.csv            # Booking history
│   └── sessions/               # Active sessions
│       ├── {user_id}_session.json
│       ├── {user_id}_costs.json
│       └── {user_id}_events.json
│
├── app.py                       # Streamlit entry point
├── utils.py                     # Helpers
├── requirements.txt             # Dependencies
│
├── ARCHITECTURE.md              # Detailed architecture
├── COMPONENTS.md                # Component documentation
├── DESIGN_NOTES.md              # Design decisions
├── TEST_CASES.md                # Test cases & samples
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Google ADK API key (optional, for Google features)

### Installation

1. **Clone & Setup**
   ```bash
   cd Travel_AI_Agent/Travel_Use_Case
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create `.env` file:
   ```
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=gsk-... (optional)
   ```

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

5. **Open Browser**
   Navigate to `http://localhost:8501`

---

## 💬 Example Conversations

### Example 1: Quick Trip Planning
```
USER: Plan a 3-day trip to Tokyo, $2000 budget, love food and culture

AGENT: 🌍 Tokyo Cultural Foodie Trip - 3 Days
       
       [Agents: Coordinator → Itinerary, Budget, Memory]
       
       ✅ Budget Analysis: $2000 is PERFECT for 3 days
       
       🗓️ Day 1: Arrival & Asakusa
       🎨 Day 2: Museums & Shibuya
       🍜 Day 3: Food tours & shopping
       
       💰 Budget Breakdown:
       • Hotels: $300
       • Food: $400 (you'll love this!)
       • Activities: $300
       • Transport: $100
       • Reserve: $900
       
       💡 Saved your culture+food preference!
```

### Example 2: Budget Constraints
```
USER: Bali trip, 2 weeks, only $1000

AGENT: ⚠️ Budget Analysis
       
       Realistic estimate for Bali (2 weeks): $1,200-1,400
       Your budget: $1,000
       
       Options:
       A) Reduce to 10 days → $850 ✓
       B) Increase budget to $1,200
       C) Different destination
       
       Bali is CHEAPEST during shoulder season!
```

### Example 3: Booking Integration
```
USER: Find me hotels in Paris for April 20-25

AGENT: 🏨 Hotel Search for Paris (April 20-25, 2 people)
       
       [Agents: Booking Helper + MCP Hotel Search]
       
       💰 Budget options:
       1. Hotel Le Marais - $60/night ✓ Best Value
       2. Boutique Paris - $120/night
       3. Luxury Hotel - $250/night
       
       ☀️ Weather: 15-20°C, mostly sunny
       
       Ready to book?
```

---

## 📊 Key Capabilities

### Agent Specialization
| Agent | Capability | Technology | Input | Output |
|-------|-----------|-----------|-------|--------|
| **Coordinator** | Route requests | Google ADK | User query | Agent plan |
| **Itinerary** | Generate plans | Google ADK | Destination, dates | Day-by-day activities |
| **Budget** | Cost estimation | Google ADK + Skills | Destination, duration | Budget breakdown |
| **Booking** | Search options | LangGraph + MCP | Destination, dates | Hotels, flights, activities |
| **Memory** | Learn preferences | Google ADK + CSV | User data | Personalized suggestions |
| **Destination** | Research info | Google ADK + Skills | Keywords | Destination details |

### Callback System
| Callback | Purpose | Trigger |
|----------|---------|---------|
| **Cost Tracker** | Monitor API spending | Every API call |
| **Budget Validator** | Check vs limit | After calculation |
| **Date Validator** | Validate dates | User input |
| **Rate Limiter** | Prevent quota exceeded | Before API call |
| **Event Logger** | Audit trail | Every action |

### Data Persistence
| Data | Format | Refresh | Use Case |
|------|--------|---------|----------|
| **Sessions** | JSON | Real-time | Active trip planning |
| **User Profiles** | CSV | Per-trip | Personalization |
| **Costs** | JSON | Per-call | Budget tracking |
| **Events** | JSON | Per-action | Debugging |

---

## 🎯 Design Philosophy

### ✅ Hybrid Approach

**Why two architectures?**
- **Google ADK**: Creative reasoning (itineraries, recommendations)
- **LangGraph**: Deterministic workflows (booking, payment, compliance)

```
Google ADK (Creative)           LangGraph (Reliable)
• Personalized itineraries      • Booking validation
• Smart recommendations         • Payment processing
• Context-aware responses       • Compliance workflows
• Learning preferences          • Audit trails
```

### ✅ Callback-Driven Safety

Every action has validation:
1. **Pre-execution**: Validate inputs (dates, budget)
2. **During execution**: Track costs and API calls
3. **Post-execution**: Check budget, log events

### ✅ Skill-Based Architecture

Reusable domain knowledge:
- Budget estimation (database of costs)
- Destination matching (preference matching)
- Itinerary formatting (activity templates)
- Currency conversion (exchange rates)

### ✅ MCP for External Data

Loose coupling to external services:
- Real APIs in production
- Mock data in development
- Easy to swap providers

---

## 🧪 Testing

### Run Tests
```bash
pytest tests/ -v
```

### Sample Test Cases
See [TEST_CASES.md](TEST_CASES.md) for:
- 8 functional test cases
- 8 edge case tests
- 3 regression tests
- Sample conversations

---

## 📚 Documentation

| Document | Content |
|----------|---------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design, diagrams, data flows |
| [COMPONENTS.md](COMPONENTS.md) | Agent/skill/service documentation |
| [DESIGN_NOTES.md](DESIGN_NOTES.md) | Design decisions, patterns, rationale |
| [TEST_CASES.md](TEST_CASES.md) | Test cases, samples, edge cases |

---

## 🔮 Roadmap

### Phase 1 (Current)
- ✅ Multi-agent architecture
- ✅ Cost tracking & validation
- ✅ Session persistence
- ✅ Basic MCP integrations

### Phase 2 (Next)
- [ ] Database migration (PostgreSQL)
- [ ] Multi-user support
- [ ] Real booking integrations
- [ ] Advanced personalization
- [ ] Mobile app

### Phase 3 (Future)
- [ ] Real-time collaboration
- [ ] Travel insurance integration
- [ ] Dynamic pricing
- [ ] Voice interface
- [ ] Offline mode

---

## ⚙️ Configuration

### Model Settings
```python
# In llm_chain.py
LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

### Agent Settings
```python
# Number of sessions to keep
MAX_SESSIONS = 5

# Session expiry (days)
SESSION_EXPIRY = 30

# Cost tracking
ENABLE_COST_TRACKING = True
```

### MCP Settings
```python
# MCP server URL
MCP_BASE_URL = "http://localhost:8000"

# Fallback to mock if unavailable
MCP_FALLBACK_TO_MOCK = True
```

---

## 🐛 Known Issues & Limitations

- **Google ADK**: Limited availability (beta)
- **MCP**: Mock data only (real APIs not implemented)
- **Database**: JSON/CSV only (not suited for > 1000 users)
- **Multi-user**: Not yet supported
- **Real Bookings**: Cannot actually book hotels/flights

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing`
5. Open PR

---

## 📄 License

MIT License - see LICENSE file

---

## 🙏 Credits

Built with:
- **Google ADK** - Agent reasoning
- **LangGraph** - Deterministic workflows
- **LangChain** - LLM orchestration
- **Streamlit** - Web interface
- **OpenAI** - Language models

---

## 📞 Support

- 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) for design overview
- 🔍 See [TEST_CASES.md](TEST_CASES.md) for examples
- 🛠️ Check [DESIGN_NOTES.md](DESIGN_NOTES.md) for decisions
- 📋 Review [COMPONENTS.md](COMPONENTS.md) for API docs

---

**Happy Travels! 🌟** *Built with ❤️ for travelers who deserve perfect trips*

---

**Last Updated**: April 2024 | **Version**: 2.0.0
