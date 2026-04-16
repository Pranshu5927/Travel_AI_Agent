"""
MCP Server Integrations for External Data.
These connect to external services via MCP for travel-related information.
"""

import logging
import json
import httpx
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class WeatherMCPClient:
    """Fetch weather data via MCP."""
    
    def __init__(self, api_base: str = "http://localhost:8000"):
        self.api_base = api_base
        self.client = httpx.AsyncClient(base_url=api_base)
    
    async def get_weather_forecast(
        self,
        location: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get weather forecast for a destination."""
        try:
            response = await self.client.get(
                "/weather/forecast",
                params={"location": location, "days": days}
            )
            
            if response.status_code == 200:
                return response.json()
            
            logger.warning(f"Weather API returned {response.status_code} for {location}")
            return self._mock_weather_data(location, days)
        
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            return self._mock_weather_data(location, days)
    
    def _mock_weather_data(self, location: str, days: int) -> Dict[str, Any]:
        """Return mock weather data for development."""
        return {
            "location": location,
            "forecast": [
                {
                    "day": i + 1,
                    "temperature_high": 25 + i % 5,
                    "temperature_low": 18 + i % 5,
                    "condition": "Partly Cloudy",
                    "humidity": 65,
                    "wind_speed": 12
                }
                for i in range(days)
            ],
            "source": "mock"
        }


class HotelFlightMCPClient:
    """Fetch hotel and flight data via MCP."""
    
    def __init__(self, api_base: str = "http://localhost:8000"):
        self.api_base = api_base
        self.client = httpx.AsyncClient(base_url=api_base)
    
    async def search_hotels(
        self,
        destination: str,
        check_in: str,
        check_out: str,
        guests: int = 2,
        budget_tier: str = "moderate"
    ) -> Dict[str, Any]:
        """Search for hotels."""
        try:
            response = await self.client.get(
                "/hotels/search",
                params={
                    "destination": destination,
                    "check_in": check_in,
                    "check_out": check_out,
                    "guests": guests,
                    "tier": budget_tier
                }
            )
            
            if response.status_code == 200:
                return response.json()
            
            return self._mock_hotel_results(destination)
        
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
            return self._mock_hotel_results(destination)
    
    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        passengers: int = 1
    ) -> Dict[str, Any]:
        """Search for flights."""
        try:
            response = await self.client.get(
                "/flights/search",
                params={
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                    "passengers": passengers
                }
            )
            
            if response.status_code == 200:
                return response.json()
            
            return self._mock_flight_results(origin, destination)
        
        except Exception as e:
            logger.error(f"Error searching flights: {e}")
            return self._mock_flight_results(origin, destination)
    
    def _mock_hotel_results(self, destination: str) -> Dict[str, Any]:
        """Return mock hotel results."""
        return {
            "destination": destination,
            "hotels": [
                {
                    "name": f"{destination} Hotel {i}",
                    "stars": 3 + (i % 3),
                    "price_per_night": 80 + (i * 40),
                    "rating": 4.0 + (i * 0.2),
                    "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
                    "location": f"Downtown {destination}"
                }
                for i in range(3)
            ],
            "source": "mock"
        }
    
    def _mock_flight_results(self, origin: str, destination: str) -> Dict[str, Any]:
        """Return mock flight results."""
        return {
            "origin": origin,
            "destination": destination,
            "flights": [
                {
                    "airline": f"Airline {i}",
                    "departure_time": "10:00 AM",
                    "arrival_time": "8:00 PM",
                    "duration": "8h 30m",
                    "price": 400 + (i * 100),
                    "stops": i,
                    "rating": 4.0 + (i * 0.1)
                }
                for i in range(3)
            ],
            "source": "mock"
        }


class CurrencyConversionMCPClient:
    """Fetch currency conversion rates via MCP."""
    
    def __init__(self, api_base: str = "http://localhost:8000"):
        self.api_base = api_base
        self.client = httpx.AsyncClient(base_url=api_base)
    
    async def convert_currency(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> Dict[str, Any]:
        """Convert currency with live rates."""
        try:
            response = await self.client.get(
                "/currency/convert",
                params={
                    "amount": amount,
                    "from": from_currency,
                    "to": to_currency
                }
            )
            
            if response.status_code == 200:
                return response.json()
            
            return self._mock_conversion(amount, from_currency, to_currency)
        
        except Exception as e:
            logger.error(f"Error converting currency: {e}")
            return self._mock_conversion(amount, from_currency, to_currency)
    
    def _mock_conversion(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Return mock conversion."""
        rates = {
            ("USD", "EUR"): 0.92,
            ("USD", "GBP"): 0.79,
            ("USD", "JPY"): 149.50,
            ("EUR", "USD"): 1.09,
            ("GBP", "USD"): 1.27
        }
        
        rate = rates.get((from_currency.upper(), to_currency.upper()), 1.0)
        converted = amount * rate
        
        return {
            "amount": amount,
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper(),
            "converted_amount": round(converted, 2),
            "exchange_rate": rate,
            "timestamp": datetime.now().isoformat(),
            "source": "mock"
        }


# Global MCP client instances
_weather_client = None
_hotel_flight_client = None
_currency_client = None


def get_weather_client(api_base: str = "http://localhost:8000") -> WeatherMCPClient:
    """Get weather MCP client."""
    global _weather_client
    if _weather_client is None:
        _weather_client = WeatherMCPClient(api_base)
    return _weather_client


def get_hotel_flight_client(api_base: str = "http://localhost:8000") -> HotelFlightMCPClient:
    """Get hotel/flight MCP client."""
    global _hotel_flight_client
    if _hotel_flight_client is None:
        _hotel_flight_client = HotelFlightMCPClient(api_base)
    return _hotel_flight_client


def get_currency_client(api_base: str = "http://localhost:8000") -> CurrencyConversionMCPClient:
    """Get currency conversion MCP client."""
    global _currency_client
    if _currency_client is None:
        _currency_client = CurrencyConversionMCPClient(api_base)
    return _currency_client
