"""
Services - Core services for the Travel AI Agent
"""

from .callbacks import (
    CostTracker,
    DateValidator,
    BudgetValidator,
    APIRateLimiter,
    EventLogger,
    get_cost_tracker,
    get_event_logger
)

from .session_memory import (
    SessionManager,
    MemoryService,
    get_session_manager,
    get_memory_service
)

from .mcp_clients import (
    WeatherMCPClient,
    HotelFlightMCPClient,
    CurrencyConversionMCPClient,
    get_weather_client,
    get_hotel_flight_client,
    get_currency_client
)

__all__ = [
    # Callbacks
    "CostTracker",
    "DateValidator",
    "BudgetValidator",
    "APIRateLimiter",
    "EventLogger",
    "get_cost_tracker",
    "get_event_logger",
    # Session & Memory
    "SessionManager",
    "MemoryService",
    "get_session_manager",
    "get_memory_service",
    # MCP Clients
    "WeatherMCPClient",
    "HotelFlightMCPClient",
    "CurrencyConversionMCPClient",
    "get_weather_client",
    "get_hotel_flight_client",
    "get_currency_client"
]
