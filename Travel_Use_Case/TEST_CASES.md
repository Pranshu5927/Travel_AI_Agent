# 🧪 Test Cases & Sample Conversations

## Table of Contents
1. [Sample Conversations](#sample-conversations)
2. [Test Cases](#test-cases)
3. [Edge Cases](#edge-cases)

---

## Sample Conversations

### Conversation 1: Basic Trip Planning
**User**: First-time user planning a simple trip

```
USER: I want to plan a trip to Paris next month
AGENT: 🌍 Welcome to Travel Planner! I'd love to help you plan your Paris trip!

         To create the perfect itinerary, I need a few details:
         📅 Specific dates: "next month" - which dates exactly?
         💰 Budget: What's your budget range? (e.g., $2000)
         🎯 Interests: What activities interest you?
            - Museums & culture
            - Dining & food
            - Shopping
            - Nightlife
         
         Tell me more details!

USER: April 20-25, budget is $3000, and I love museums and dining
AGENT: 🌍 Perfect! 5-day romantic Paris trip with $3000 budget
         
         [Agents invoked: Itinerary, Budget, Memory]
         
         📅 **Dates**: April 20-25, 2024 (5 days)
         💰 **Budget**: $3000
         🎯 **Theme**: Cultural & Culinary
         
         📊 **Budget Breakdown**:
         • Accommodation: $500 ($100/night moderate hotels)
         • Food: $350 ($70/day dining)
         • Activities: $450 (museums, experiences)
         • Transport: $200 (metro pass, transfers)
         • Reserve: $1500 (emergency, shopping)
         ✅ Budget Status: Great! You have $1500 extra
         
         🗓️ **Your 5-Day Itinerary**:
         
         **Day 1 - April 20 (Arrival & City Intro)**
         🌅 Morning: Arrive, check-in, rest
         🏛️ Afternoon: Eiffel Tower & Seine River Cruise (3 hours)
         🍽️ Evening: Dinner at Left Bank bistro
         
         **Day 2 - April 21 (Museums)**
         🎨 Morning: Louvre Museum (3 hours)
         🍴 Lunch: Café Marly
         🏰 Afternoon: Versailles Palace Day trip
         🍽️ Evening: Casual dinner in Montmartre
         
         **Day 3 - April 22 (Culture & Food)**
         ⛪ Morning: Notre-Dame & Sainte-Chapelle
         🥐 Lunch: French Bakery experience
         🛍️ Afternoon: Shopping on Champs-Élysées
         🍽️ Evening: Wine & cheese tasting
         
         **Day 4 - April 23 (Hidden Gems)**
         🎭 Morning: Musée d'Orsay
         🍽️ Lunch: Local restaurant recommendation
         🚶 Afternoon: Walk through Le Marais district
         🍽️ Evening: Fine dining experience (use extra budget)
         
         **Day 5 - April 24 (Leisure & Shopping)**
         ☕ Morning: Café experience
         🛍️ Afternoon: Last-minute shopping & souvenir hunting
         🍽️ Evening: Final dinner, pack for departure
         
         💡 **Travel Tips**:
         • Book Louvre & Versailles tickets online
         • Use Paris Visite pass for unlimited transport
         • Try local bistros for better value
         • Spring weather: 15-20°C, bring layers
         • Tip: 5-10% for restaurants (service included)
         
         ❤️ **Your Personalized Notes**:
         First-time visitor! We've saved your preferences.
         Next time to Paris, we'll remember this itinerary!

USER: Can you add more food experiences to day 3?
AGENT: 🔄 Updating itinerary for more food experiences...
         
         [Agents invoked: Itinerary (modify), Budget (validate)]
         
         **Updated Day 3 - April 22 (Culinary Focus)**
         ⛪ Morning: Notre-Dame & Sainte-Chapelle (1 hour)
         🍽️ Mid-morning: Croissant & coffee at traditional café
         🍴 Lunch: Cooking class - French cuisine basics (2 hours, $100)
         ☕ Afternoon: Visit Marché Bastille food market
         🥖 Late Afternoon: Boulangerie tour & tasting
         🍽️ Evening: Wine & cheese tasting experience
         
         💰 **Updated Budget**:
         Added cooking class: +$100
         Total food category now: $450 (+$100)
         New total: $3100
         ⚠️ Warning: Slightly over budget (100 more than planned)
         💡 Recommendation: Reduce shopping budget or use emergency reserve

USER: That's perfect, use the extra budget
AGENT: ✅ Done! Your itinerary has been locked.
         
         🎉 **Your Complete Paris Trip is Ready!**
         • Itinerary: Saved
         • Budget: $3100 (approved using reserve)
         • Preferences: Saved to your profile
         
         💾 **What's Next?**
         Would you like me to:
         1️⃣ Search for hotels?
         2️⃣ Find flight deals?
         3️⃣ Book activities?
         4️⃣ Save this and plan another trip?
```

---

### Conversation 2: Budget-Conscious Traveler
**User**: Experienced traveler with tight budget

```
USER: budget trip to bali, 2 weeks, $1500 max
AGENT: 💰 **Budget Bali Adventure** - 14 days, $1500
         
         [Agents invoked: Budget, Destination Research, Itinerary, Memory]
         
         ✅ **Budget Analysis**:
         Recommended for budget tier: $1,400-$1,600 ✓ PERFECT FIT
         
         **Breakdown**:
         • Accommodation: $224 ($16/night guesthouses)
         • Food: $210 ($15/day local warungs)
         • Activities: $280 ($20/day outdoor activities)
         • Transport: $140 ($10/day)
         • Reserve: $646 (19% buffer)
         
         💡 **Cost-Saving Tips**:
         ✓ Stay in Ubud (cheaper than Seminyak)
         ✓ Eat at local warungs (meals $2-3)
         ✓ Free temples and rice paddy walks
         ✓ Rent scooter ($5/day) vs taxis
         ✓ Book flights 2+ months in advance
         
         🎯 **Recommended Theme**: Adventure & Culture (low-cost)
         
         🗺️ **14-Day Budget Itinerary Highlights**:
         • Days 1-3: Ubud (cultural heart, cheapest)
         • Days 4-7: Hiking, temples, local experiences
         • Days 8-10: Beach time (Sanur, not touristy Seminyak)
         • Days 11-14: Remote villages, waterfall hikes
         
         📊 **Your Profile**:
         • Saved as budget traveler
         • Noted: Bali interest
         • Adventure preferences recognized
         
         🔍 **Weather Check**:
         April is dry season - Perfect timing! 🌞

USER: What about flights? I'm from New York
AGENT: ✈️ **Flight Search** - New York to Bali
         [Agents invoked: Booking Helper, MCP Flight Search, Cost Tracker]
         
         🔍 **Best Flight Options** (prices vary by season):
         
         1️⃣ **Budget Option** - $480 (Best value)
            • Airline: AirAsia X
            • Departure: Tue 10:00 AM (JFK)
            • Arrival: Thu 10:00 PM (DPS)
            • Duration: 20h 45m (1 stop in Kuala Lumpur)
            • Rating: 3.8/5
            💡 Tip: Book now for April rates
         
         2️⃣ **Balanced Option** - $650
            • Airline: United
            • Duration: 18h 30m (1 stop)
            • Rating: 4.2/5
            🎯 Recommended for your budget
         
         3️⃣ **Premium Option** - $900
            • Airline: Singapore Airlines
            • Duration: 17h 15m (1 stop)
            • Rating: 4.7/5
            👑 Most comfortable
         
         💰 **Updated Budget Calculation**:
         • Flight (recommended): $650
         • Trip costs: $1,500
         • **Total: $2,150**
         
         ⚠️ **Important**: This exceeds your budget!
         🤔 **Options**:
         A) Take budget flight ($480) → Total $1,980 ✓
         B) Increase budget to $2,150
         C) Reduce trip length to 10 days
         D) Different destination with cheaper flights

USER: Let me reduce to 10 days instead
AGENT: ✅ **Updated 10-Day Bali Trip**
         
         💰 **Revised Budget**:
         • Flights (budget): $480
         • Accommodation (10 nights): $160
         • Food (10 days): $150
         • Activities: $200
         • Transport: $100
         • Reserve: $310
         **Total: $1,400** ✅ Under budget!
         
         🗓️ **Optimized 10-Day Itinerary** (Same highlights, condensed)
         
         ✈️ **Flight Booked**:
         Would you like me to proceed with:
         • Flight: AirAsia X ($480)
         • Check-in at Ubud guesthouse ($16/night)
         • Reserve activities
         
         Yes, let's lock this itinerary! ✓
```

---

### Conversation 3: Group Trip Planning
**User**: Planning trip for family/group

```
USER: Plan Tokyo trip for 4 people, 1 week, $5000 total budget
AGENT: 👨‍👩‍👧‍👦 **Group Trip Coordinator** - 4 people, 7 days
         
         [Agents invoked: Budget, Itinerary, Booking, Personalization]
         
         📊 **Per-Person Budget**: $1,250
         
         **Group Budget Breakdown** (4 people):
         • Accommodation (shared rooms): $800 ($114/night)
         • Flights (4x): Already included in $5000? 
           ⚠️ Note: Budget seems low if flights needed
           💡 Tip: Flights NYC-Tokyo = $800-1200 per person
           Total flights alone: $3,200-4,800
         
         ⚡ **Important Question**: Does $5000 include flights or just trip?
         
         Assuming flights included (tight budget):
         • Flights (4x): ~$4,000
         • Accommodation: $600
         • Food: $300
         • Activities: Limited
         
         💡 **Recommendation**: Increase budget to $8,000+ for comfortable trip
         
USER: Flights are separate, $5000 is just for the trip
AGENT: ✅ **Much better!** $5,000 for 7-day Tokyo trip (4 people)
         
         📊 **Per-Person in Tokyo**: $1,250 (7 days)
         
         **Budget Breakdown**:
         • Accommodation: $1,400 ($50/person/night, shared)
         • Food: $1,200 ($40/person/day × 4 × 7)
         • Activities: $1,400 ($50/person)
         • Transport: $600 (metro passes × 4)
         • Reserve: $400
         **Total: $5,000** ✅ Perfect fit!
         
         👥 **Group Considerations**:
         • Need accessible attractions?
         • Any dietary restrictions?
         • Age ranges? (Kids, teens, adults, seniors?)
         • Activity preferences vary?
         
         🗓️ **Sample Group Itinerary** (family-friendly):
         
         **Day 1**: Arrival, Shibuya district, dinner together
         **Day 2**: Senso-ji Temple (cultural), Asakusa exploration
         **Day 3**: Team activity - Robot Restaurant show, Shinjuku
         **Day 4**: Split activities:
           • Group A: Imperial Palace + gardens (cultural)
           • Group B: Akihabara + shopping (tech-focused)
           • Evening: Reunion dinner
         **Day 5**: Nikko day trip (nature, temples - full group)
         **Day 6**: Flexible day - individual interests + team meal
         **Day 7**: Last-minute shopping, farewell dinner
         
         💳 **Group Logistics**:
         • Recommend IC card for all (transport pass)
         • Book accommodation near central metro
         • Reserve group restaurants in advance
         • Plan activities that split options
         
         📱 **Next Steps**:
         1. Confirm dates and member details
         2. Input specific preferences for each person
         3. Book hotels (group discount?)
         4. Reserve group activities
```

---

## Test Cases

### TC-001: Itinerary Generation
**Scenario**: Generate itinerary for basic trip

**Input**:
```python
{
    "destination": "Paris",
    "start_date": "2024-04-20",
    "end_date": "2024-04-25",
    "preferences": {
        "activities": ["museums", "dining"],
        "vibe": "romantic",
        "pace": "moderate"
    },
    "duration": 5
}
```

**Expected Output**:
- ✅ 5 day plans generated
- ✅ Each day has morning, afternoon, evening
- ✅ Practical tips included
- ✅ Highlights extracted
- ✅ Summary generated

---

### TC-002: Budget Validation
**Scenario**: Validate if budget is sufficient

**Input**:
```python
{
    "destination": "Tokyo",
    "duration": 7,
    "budget": 2000,
    "budget_tier": "moderate"
}
```

**Expected Output**:
- ✅ Breakdown shows needed ~$2,800
- ✅ Validation: is_feasible = False
- ✅ Recommendation: "Increase budget by $800"
- ✅ Percentage sufficient: ~71%

---

### TC-003: Hotel Search
**Scenario**: Search hotels with preferences

**Input**:
```python
{
    "action": "search_hotels",
    "destination": "Bali",
    "check_in": "2024-04-20",
    "check_out": "2024-04-27",
    "guests": 2,
    "budget_tier": "budget"
}
```

**Expected Output**:
- ✅ 3+ hotel options returned
- ✅ Prices: $20-50/night (budget tier)
- ✅ Ratings displayed
- ✅ Recommendations: Best value, Budget, Premium

---

### TC-004: Memory Persistence
**Scenario**: Save and retrieve user preferences

**Steps**:
1. Save preferences for user123
   - Activities: ["hiking", "food"]
   - Budget: "moderate"
   - Favorites: ["Japan", "Thailand"]

2. Load preferences for user123
   - Should retrieve exactly what was saved

3. Get recommendations for same user
   - Should mention hiking, food, Japan preferences

**Expected**:
- ✅ Preferences saved to CSV
- ✅ Preferences loaded correctly
- ✅ Recommendations reflect saved preferences

---

### TC-005: Cost Tracking
**Scenario**: Track API costs and validate budget

**Input**:
```python
user_id = "user123"
budget = 100
add_cost("openai", 25.50)   # Add $25.50
add_cost("google", 15.30)   # Add $15.30
validate_budget()
```

**Expected**:
- ✅ Total: $40.80
- ✅ Remaining: $59.20
- ✅ Is valid: True (still under budget)
- ✅ Cost saved to file

---

### TC-006: Multi-Agent Coordination
**Scenario**: Coordinator routes to multiple agents

**Input**:
```
User: "Plan a 5-day trip to Tokyo for $4000 with adventure activities"
```

**Expected Agents Invoked**:
1. ✅ Memory Agent (load preferences)
2. ✅ Destination Research (Tokyo info)
3. ✅ Itinerary Agent (generate adventure itinerary)
4. ✅ Budget Agent (validate $4000 is sufficient)
5. ✅ Booking Agent (search hotels/flights)

**Output**: Comprehensive response from all agents

---

## Edge Cases

### EC-001: Invalid Dates
**Input**: 
```python
start_date = "2024-04-25"
end_date = "2024-04-20"  # End before start
```

**Expected**:
- ✅ DateValidator catches error
- ❌ Return: "End date must be after start date"
- Response: Ask user for correction

---

### EC-002: Unrealistic Budget
**Input**:
```python
destination = "Paris"
duration = 7
budget = 100  # Way too low
```

**Expected**:
- ✅ BudgetValidator warns
- ✅ Message: "Minimum $1,050 recommended"
- ✅ Offer options: increase budget, reduce days, different destination

---

### EC-003: Rate Limit Exceeded
**Scenario**: User makes 100 requests in 1 minute

**Expected**:
- ✅ APIRateLimiter blocks after 60th request
- ✅ Message: "Too many requests, please wait"
- ✅ Subsequent requests queued

---

### EC-004: Budget Exceeded During Planning
**Scenario**: User keeps adding premium activities

```
Initial: $3,000 budget
Add activity 1: +$200 → Total: $3,200 ⚠️
Add activity 2: +$300 → Total: $3,500 ❌ OVER BUDGET
```

**Expected**:
- ✅ CostTracker flags overage
- ✅ EventLogger records: "budget_exceeded"
- ✅ Response: "Over budget by $500. Reduce activities or increase budget?"

---

### EC-005: New User with No Preferences
**Scenario**: First-time user, no saved preferences

**Expected**:
- ✅ Memory Agent loads default preferences
- ✅ Memory score: 0.0
- ✅ Personalization level: "low"
- ✅ Recommendations: Generic, ask for preferences

---

### EC-006: MCP Server Down
**Scenario**: Weather/Hotel API unavailable

**Expected**:
- ✅ Try actual API
- ✅ Fallback to mock data
- ✅ Log event: "mcp_fallback_used"
- ✅ Continue planning (don't crash)

---

### EC-007: Session Expiry
**Scenario**: User doesn't interact for 30 days

**Expected**:
- ✅ SessionManager marks for cleanup
- ✅ Old sessions deleted
- ✅ User can still access via preferences (Memory Service)
- ✅ New session created on next login

---

### EC-008: Concurrent Requests
**Scenario**: User makes multiple requests simultaneously

**Expected**:
- ✅ Session locked during update
- ✅ Requests queued
- ✅ No race conditions
- ✅ Consistent state maintained

---

## Regression Tests

### RT-001: Backward Compatibility
- ✅ Old session files load correctly
- ✅ Old preference formats supported
- ✅ Migration helpers for updates

### RT-002: Data Integrity
- ✅ Sessions save correctly
- ✅ Memory persistent across restarts
- ✅ Costs calculated accurately

### RT-003: Performance
- ✅ Itinerary generation < 5 seconds
- ✅ Budget calculation < 1 second
- ✅ MCP calls < 3 seconds

---

*Run test cases with: `pytest tests/ -v`*
