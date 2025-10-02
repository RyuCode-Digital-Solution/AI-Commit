"""
Settings Manager for AI Commit
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Default values
DEFAULT_SETTINGS = {
    "gemini_api_key": "",
    "openai_api_key": "",
    "gemini_model": "gemini-2.5-flash",
    "openai_model": "gpt-4o-mini",
    "github_username": "",
    "github_token": "",
    "parent_folder": str(Path.home()),
    "recent_repos": [],
    "auto_push": True,
    "dark_mode": False
}

GEMINI_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-ultra",
    "gemini-1.0-pro",
    "gemini-1.0-nano"
]

OPENAI_MODELS = [
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-5-chat",
    "gpt-5-codex",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4.5",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4",
    "gpt-3.5-turbo",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-mini-high",
    "o3-pro",
    "o4-mini",
    "o4-mini-high",
    "gpt-oss-120b",
    "gpt-oss-20b"
]


class SettingsManager:
    def __init__(self, settings_file=None):
        # Determine settings file location
        if settings_file is None:
            if getattr(sys, 'frozen', False):
                # Running as compiled exe - use app data directory
                base_dir = self.get_app_data_directory()
            else:
                # Running as script - use current directory
                base_dir = os.getcwd()
            
            # Create settings directory if it doesn't exist
            os.makedirs(base_dir, exist_ok=True)
            self.settings_file = os.path.join(base_dir, 'settings.json')
        else:
            self.settings_file = settings_file
            
        self.settings = self.load_settings()
    
    def get_app_data_directory(self):
        """Get application data directory for settings"""
        # Try to use user's home directory first
        home_dir = Path.home()
        
        # Create "AI Commit RyuCode" folder in home directory
        app_dir = home_dir / "AI Commit RyuCode"
        
        # Alternative locations if home directory fails
        alternative_locations = [
            app_dir,
            Path(os.getenv('APPDATA', '')) / "AI Commit RyuCode",  # Windows
            Path(os.getenv('LOCALAPPDATA', '')) / "AI Commit RyuCode",  # Windows
            Path(os.getenv('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / "AI Commit RyuCode",  # Linux
            Path.home() / "Library" / "Application Support" / "AI Commit RyuCode",  # macOS
        ]
        
        # Use first available location
        for location in alternative_locations:
            try:
                location.mkdir(parents=True, exist_ok=True)
                if location.is_dir() and os.access(location, os.W_OK):
                    return str(location)
            except (OSError, PermissionError):
                continue
        
        # Fallback to current directory
        return os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    settings = DEFAULT_SETTINGS.copy()
                    settings.update(loaded_settings)
                    return settings
            else:
                # Create default settings file
                self.save_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            # Return defaults and try to save them
            try:
                self.save_settings()
            except:
                pass
        
        return DEFAULT_SETTINGS.copy()
    
    def save_settings(self) -> bool:
        """Save settings to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def add_recent_repo(self, repo_path: str):
        """Add repository to recent list"""
        if repo_path in self.settings["recent_repos"]:
            self.settings["recent_repos"].remove(repo_path)
        self.settings["recent_repos"].insert(0, repo_path)
        # Keep only last 10 repos
        self.settings["recent_repos"] = self.settings["recent_repos"][:10]
        self.save_settings()