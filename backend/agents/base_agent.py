import json
import requests
import re
from typing import Dict, Any, Optional
from config import OLLAMA_HOST, OLLAMA_MODEL

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def call_ollama(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Attempt calling Ollama REST endpoint if available."""
        url = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        try:
            resp = requests.post(url, json=payload, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response")
        except Exception:
            pass # Ollama not available or connection refused; fallback will trigger
        return None

    def extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Utility to extract JSON object from LLM output."""
        try:
            # Look for JSON codeblock or raw json
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception:
            pass
        return None
