"""
Session and Memory Management Service.
Handles persistent session storage and user memory across conversations.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """Manage user sessions with persistence."""
    
    def __init__(self, sessions_dir: str = "data/sessions", max_sessions: int = 5):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.max_sessions = max_sessions
        self.sessions = {}
        self._load_all_sessions()
    
    def _load_all_sessions(self):
        """Load all existing sessions."""
        for session_file in self.sessions_dir.glob("*_session.json"):
            try:
                with open(session_file, 'r') as f:
                    session = json.load(f)
                    user_id = session_file.stem.replace("_session", "")
                    self.sessions[user_id] = session
            except Exception as e:
                logger.error(f"Error loading session {session_file}: {e}")
    
    def create_session(self, user_id: str) -> Dict[str, Any]:
        """Create a new session."""
        session = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "messages": [],
            "state": {
                "destination": None,
                "start_date": None,
                "end_date": None,
                "budget": None,
                "preferences": None,
                "itinerary_generated": False,
                "current_trip_id": None
            }
        }
        self.sessions[user_id] = session
        self._save_session(user_id)
        logger.info(f"Session created for user: {user_id}")
        return session
    
    def get_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user session."""
        if user_id not in self.sessions:
            return self.create_session(user_id)
        
        # Update last accessed
        self.sessions[user_id]["last_accessed"] = datetime.now().isoformat()
        self._save_session(user_id)
        return self.sessions[user_id]
    
    def update_session(self, user_id: str, updates: Dict[str, Any]):
        """Update session data."""
        if user_id not in self.sessions:
            self.create_session(user_id)
        
        # Deep merge updates
        self._deep_merge(self.sessions[user_id], updates)
        self.sessions[user_id]["last_accessed"] = datetime.now().isoformat()
        self._save_session(user_id)
        logger.debug(f"Session updated for user: {user_id}")
    
    def _deep_merge(self, target: Dict, source: Dict):
        """Deep merge source into target."""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def _save_session(self, user_id: str):
        """Save session to file."""
        session_file = self.sessions_dir / f"{user_id}_session.json"
        with open(session_file, 'w') as f:
            json.dump(self.sessions[user_id], f, indent=2)
    
    def cleanup_old_sessions(self):
        """Remove sessions older than 30 days."""
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for user_id, session in list(self.sessions.items()):
            last_accessed = datetime.fromisoformat(session.get("last_accessed", ""))
            if last_accessed < cutoff_date:
                session_file = self.sessions_dir / f"{user_id}_session.json"
                try:
                    session_file.unlink()
                    del self.sessions[user_id]
                    logger.info(f"Cleaned up old session: {user_id}")
                except Exception as e:
                    logger.error(f"Error cleaning session {user_id}: {e}")
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions."""
        return list(self.sessions.values())


class MemoryService:
    """Manage user preferences and conversation memory."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.data_dir / "users.csv"
        self.memory = {}
        self._init_users_file()
    
    def _init_users_file(self):
        """Initialize users CSV if not exists."""
        if not self.users_file.exists():
            import csv
            with open(self.users_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["user_id", "name", "preferences", "favorite_destinations", "budget_preference", "created_at"])
    
    def save_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Save user preferences."""
        import csv
        
        # Read existing users
        users = {}
        if self.users_file.exists():
            with open(self.users_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    users[row["user_id"]] = row
        
        # Update or create user
        prefs_str = json.dumps(preferences.get("travel_preferences", {}))
        fav_dests = json.dumps(preferences.get("favorite_destinations", []))
        
        users[user_id] = {
            "user_id": user_id,
            "name": preferences.get("name", ""),
            "preferences": prefs_str,
            "favorite_destinations": fav_dests,
            "budget_preference": preferences.get("budget_preference", ""),
            "created_at": users[user_id]["created_at"] if user_id in users else datetime.now().isoformat()
        }
        
        # Write back all users
        with open(self.users_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["user_id", "name", "preferences", "favorite_destinations", "budget_preference", "created_at"])
            writer.writeheader()
            for uid, user in users.items():
                writer.writerow(user)
        
        logger.info(f"User preferences saved: {user_id}")
    
    def load_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user preferences."""
        import csv
        
        if not self.users_file.exists():
            return None
        
        with open(self.users_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["user_id"] == user_id:
                    return {
                        "name": row["name"],
                        "travel_preferences": json.loads(row.get("preferences", "{}")),
                        "favorite_destinations": json.loads(row.get("favorite_destinations", "[]")),
                        "budget_preference": row.get("budget_preference", "")
                    }
        
        return None
    
    def store_memory(self, user_id: str, key: str, value: Any):
        """Store a memory key-value pair."""
        memory_file = self.data_dir / f"{user_id}_memory.json"
        
        memory = {}
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                memory = json.load(f)
        
        memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(memory_file, 'w') as f:
            json.dump(memory, f, indent=2)
    
    def recall_memory(self, user_id: str, key: str) -> Optional[Any]:
        """Retrieve a stored memory."""
        memory_file = self.data_dir / f"{user_id}_memory.json"
        
        if not memory_file.exists():
            return None
        
        with open(memory_file, 'r') as f:
            memory = json.load(f)
        
        if key in memory:
            return memory[key]["value"]
        
        return None


# Global instances
_session_manager = None
_memory_service = None

def get_session_manager(sessions_dir: str = "data/sessions") -> SessionManager:
    """Get or create session manager."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager(sessions_dir)
    return _session_manager

def get_memory_service(data_dir: str = "data") -> MemoryService:
    """Get or create memory service."""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService(data_dir)
    return _memory_service
