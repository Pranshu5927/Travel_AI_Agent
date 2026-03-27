# 🌍 Travel AI Agent

A sophisticated conversational AI travel planning assistant built with Streamlit and LangChain. Plan your perfect trip through natural language conversations with an intelligent agent that remembers context, handles multiple trips, and provides personalized recommendations.

## ✨ Features

### 🧠 Intelligent Conversation
- **Natural Language Processing**: Understands complex travel requests and preferences
- **Context Awareness**: Maintains conversation history and remembers your preferences
- **Multi-Trip Management**: Handle multiple travel plans simultaneously
- **Smart Date Parsing**: Handles relative dates like "next weekend", "tomorrow", "in 2 weeks"

### 📅 Trip Planning
- **Comprehensive Itineraries**: Day-by-day plans with activities, food, and transportation
- **Flexible Preferences**: Supports budget, activity types, and travel styles
- **Weather & Cultural Info**: Includes local tips, safety information, and weather considerations
- **Budget Breakdown**: Provides cost estimates and packing suggestions

### 🎯 Agentic Behavior
- **Follow-up Questions**: Asks relevant questions to refine your trip
- **Modification Support**: Easily change dates, destinations, or preferences
- **Travel Assistance**: Ready for flight booking, hotel recommendations, and more
- **Personalized Recommendations**: Adapts suggestions based on your preferences

### 💾 Data Management
- **Persistent Sessions**: Save and resume trip planning across sessions
- **Trip History**: View and manage multiple travel plans
- **Export Ready**: Structured data for future integrations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Travel_AI_Agent/Travel_Use_Case
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit langchain-openai python-dotenv dateutil
   ```

4. **Set up environment variables**
   Create a `.env` file in the Travel_Use_Case directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 💬 Usage Examples

### Basic Trip Planning
```
User: I want to visit Paris next weekend
Agent: Generates a 2-day itinerary for Paris with activities, food, and transportation tips
```

### Advanced Planning with Preferences
```
User: Plan a 5-day trip to Japan in April with a $3000 budget, focusing on cultural experiences
Agent: Creates detailed itinerary with temples, traditional cuisine, and budget breakdown
```

### Trip Modifications
```
User: Actually, make it more adventure-focused and extend to 7 days
Agent: Regenerates itinerary with hiking, outdoor activities, and adjusted timeline
```

### Multiple Trip Management
- Create separate trips for different destinations
- Switch between trips using the sidebar
- Each trip maintains its own conversation history

## 🏗️ Architecture

```
Travel_Use_Case/
├── app.py                 # Main Streamlit application
├── chat_handler.py        # Conversation logic and state management
├── llm_chain.py          # LangChain integration and AI prompts
├── state_manager.py      # Session state handling
├── utils.py              # Date parsing and utility functions
├── prompts.py            # Additional prompt templates
├── itinerary.py          # Legacy itinerary generation
└── .env                  # Environment variables
```

### Key Components

- **app.py**: Web interface with chat UI and trip management
- **chat_handler.py**: Processes user input, manages conversation flow
- **llm_chain.py**: Handles AI interactions, information extraction, and content generation
- **state_manager.py**: Manages conversation state and trip data
- **utils.py**: Date parsing utilities for natural language dates

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Model Settings
- **Model**: GPT-4o-mini (configurable in llm_chain.py)
- **Temperature**: 0 for consistent responses

## 🎨 UI Features

### Sidebar
- **Trip Management**: Create, select, and delete trips
- **Trip Status**: Shows destination, dates, and completion status
- **Navigation**: Easy switching between different travel plans

### Main Chat
- **Trip Header**: Displays current trip info and new itinerary button
- **Chat Interface**: Clean, intuitive conversation flow
- **Message History**: Persistent conversation history

## 🔮 Future Enhancements

### Planned Features
- **Flight Booking Integration**: Direct flight search and booking
- **Hotel Recommendations**: Accommodation suggestions with pricing
- **Transportation Planning**: Train, bus, and car rental options
- **Weather Integration**: Real-time weather forecasts
- **Currency Conversion**: Multi-currency budget planning
- **Photo Recommendations**: Best photography spots and tips

### Technical Improvements
- **Database Integration**: Persistent storage for trip data
- **User Authentication**: Multi-user support
- **Mobile App**: React Native companion app
- **Voice Interface**: Speech-to-text travel planning
- **Offline Mode**: Basic functionality without internet

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **LangChain**: For powerful AI orchestration
- **OpenAI**: For the GPT models powering the intelligence
- **Dateutil**: For robust date parsing capabilities

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check the documentation for common solutions
- Join our community discussions

---

**Happy Travels! 🌟**

*Built with ❤️ for travelers who deserve perfect trips*</content>
<parameter name="filePath">e:\D_drive\Personal Dev\Projects\Travel_AI_Agent\Travel_Use_Case\README.md