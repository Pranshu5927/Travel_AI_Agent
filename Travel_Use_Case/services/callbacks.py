"""
Callback system for tracking, validation, and cost monitoring.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class CostTracker:
    """Track API costs and budget constraints."""
    
    def __init__(self, user_id: str, budget: Optional[float] = None):
        self.user_id = user_id
        self.budget = budget
        self.costs = {
            "openai": 0.0,
            "google": 0.0,
            "other": 0.0
        }
        self.total_cost = 0.0
        self.call_count = 0
        self.log_file = Path(f"data/sessions/{user_id}_costs.json")
        self._load_costs()
    
    def _load_costs(self):
        """Load previous costs from file."""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                self.costs = data.get("costs", {})
                self.total_cost = data.get("total_cost", 0.0)
                self.call_count = data.get("call_count", 0)
    
    def _save_costs(self):
        """Save costs to file."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump({
                "costs": self.costs,
                "total_cost": self.total_cost,
                "call_count": self.call_count,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
    
    def add_cost(self, provider: str, amount: float, details: Dict[str, Any] = None):
        """Track API cost."""
        self.costs[provider] = self.costs.get(provider, 0.0) + amount
        self.total_cost += amount
        self.call_count += 1
        
        logger.info(f"Cost added: {provider} +${amount:.4f} (Total: ${self.total_cost:.4f})")
        
        if details:
            logger.debug(f"  Details: {details}")
        
        self._save_costs()
    
    def validate_budget(self) -> tuple[bool, Optional[str]]:
        """Check if cost exceeds budget."""
        if self.budget is None:
            return True, None
        
        if self.total_cost > self.budget:
            msg = f"Budget exceeded: ${self.total_cost:.2f} > ${self.budget:.2f}"
            return False, msg
        
        remaining = self.budget - self.total_cost
        if remaining < 10:
            msg = f"Warning: Low budget remaining: ${remaining:.2f}"
            return True, msg
        
        return True, None
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost summary."""
        return {
            "total": self.total_cost,
            "budget": self.budget,
            "remaining": self.budget - self.total_cost if self.budget else None,
            "breakdown": self.costs,
            "calls": self.call_count,
            "avg_cost_per_call": self.total_cost / self.call_count if self.call_count > 0 else 0
        }


class DateValidator:
    """Validate travel dates."""
    
    @staticmethod
    def validate_dates(start_date, end_date) -> tuple[bool, Optional[str]]:
        """Validate date logic."""
        if start_date and end_date:
            if start_date > end_date:
                return False, "End date must be after start date"
        return True, None


class BudgetValidator:
    """Validate budget constraints."""
    
    @staticmethod
    def validate_budget_feasibility(destination: str, budget: float, duration: int) -> tuple[bool, Optional[str]]:
        """Check if budget is realistic for destination."""
        # Rough minimum daily costs per destination (USD)
        min_daily_costs = {
            "paris": 100,
            "tokyo": 80,
            "bali": 30,
            "new york": 150,
            "london": 120,
            "bangkok": 25,
            "dubai": 120
        }
        
        # Default to moderate estimate
        min_daily = min_daily_costs.get(destination.lower(), 60)
        minimum_needed = min_daily * duration
        
        if budget < minimum_needed:
            return False, f"Minimum recommended budget for {destination} ({duration} days) is ${minimum_needed:.2f}"
        
        return True, None


class APIRateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.call_times = []
    
    def is_allowed(self) -> bool:
        """Check if next call is allowed."""
        import time
        now = time.time()
        
        # Remove calls older than 1 minute
        self.call_times = [t for t in self.call_times if now - t < 60]
        
        if len(self.call_times) >= self.calls_per_minute:
            return False
        
        self.call_times.append(now)
        return True
    
    def wait_if_needed(self):
        """Wait if rate limit reached."""
        import time
        if not self.is_allowed():
            logger.warning("Rate limit approached, waiting 1 second...")
            time.sleep(1)


class EventLogger:
    """Log all events for debugging and auditing."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.events = []
        self.log_file = Path(f"data/sessions/{user_id}_events.json")
        self._load_events()
    
    def _load_events(self):
        """Load previous events."""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                self.events = json.load(f)
    
    def _save_events(self):
        """Save events to file."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump(self.events, f, indent=2)
    
    def log_event(self, event_type: str, details: Dict[str, Any]):
        """Log an event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details
        }
        self.events.append(event)
        self._save_events()
        logger.info(f"Event logged: {event_type}")


# Global instances
_trackers = {}
_loggers = {}

def get_cost_tracker(user_id: str, budget: Optional[float] = None) -> CostTracker:
    """Get or create cost tracker for user."""
    if user_id not in _trackers:
        _trackers[user_id] = CostTracker(user_id, budget)
    return _trackers[user_id]

def get_event_logger(user_id: str) -> EventLogger:
    """Get or create event logger for user."""
    if user_id not in _loggers:
        _loggers[user_id] = EventLogger(user_id)
    return _loggers[user_id]
