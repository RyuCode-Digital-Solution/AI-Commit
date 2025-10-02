"""
AI Provider for generating commit messages using Gemini and OpenAI
"""

import os
from typing import Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from src.core.settings_manager import SettingsManager


class AIProvider:
    def __init__(self, settings_manager: SettingsManager):
        self.settings_manager = settings_manager
    
    def generate_commit_message(self, diff: str, provider: str) -> str:
        """Generate commit message using AI"""
        diff_truncated = diff[:3000] if len(diff) > 3000 else diff
        
        if provider == "gemini":
            return self._generate_with_gemini(diff_truncated)
        else:  # chatgpt
            return self._generate_with_openai(diff_truncated)
    
    def _generate_with_gemini(self, diff: str) -> str:
        """Generate commit message using Gemini"""
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Install with: pip install google-generativeai")
        
        api_key = self.settings_manager.get("gemini_api_key")
        if not api_key:
            raise ValueError("Gemini API Key not set. Please configure in Settings.")
        
        genai.configure(api_key=api_key)
        model_name = self.settings_manager.get("gemini_model", "gemini-2.5-flash")
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Generate a clear commit message following conventional commits format.

Git diff:
{diff}

Format: <type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore
Use English, be concise. Return only the commit message."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    def _generate_with_openai(self, diff: str) -> str:
        """Generate commit message using OpenAI"""
        if not OPENAI_AVAILABLE:
            raise ImportError("openai not installed. Install with: pip install openai")
        
        api_key = self.settings_manager.get("openai_api_key")
        if not api_key:
            raise ValueError("OpenAI API Key not set. Please configure in Settings.")
        
        client = OpenAI(api_key=api_key)
        model_name = self.settings_manager.get("openai_model", "gpt-4o-mini")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that generates clear and concise git commit messages following conventional commits format."
                },
                {
                    "role": "user", 
                    "content": f"Generate a commit message for the following changes:\n\n{diff}\n\nFormat: <type>(<scope>): <subject>\n\nTypes: feat, fix, docs, style, refactor, test, chore\nUse English, be concise. Return only the commit message."
                }
            ],
            temperature=0.7,
            max_tokens=200,
            timeout=30
        )
        return response.choices[0].message.content.strip()