import os
import re
import json
from typing import Dict, Any, Optional
from config import Config

class RequirementAgent:
    """
    Agent 1: Requirement Understanding & Intent Extraction Agent
    Converts unstructured user text into structured query constraints.
    """
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")

    def process(self, raw_text: str) -> Dict[str, Any]:
        """Runs Gemini API or intelligent heuristic NLP parser to extract structured intent."""
        if not raw_text or not raw_text.strip():
            return self._empty_intent()

        # Try Gemini API if key is available
        if self.api_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)
                system_prompt = (
                    "You are a structured e-commerce search requirement parser. "
                    "Extract structured JSON with keys: category (Laptops, Smartphones, Headphones, Smartwatches, Tablets, All), "
                    "max_price (number in INR ₹ or null), min_price (number in INR ₹ or null), brand (string or null), "
                    "mandatory_specs (array of strings), optional_preferences (array of strings), intended_use (string), sort_by (price_asc, price_desc, rating_desc, relevance)."
                )
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_prompt}\nUser Query: \"{raw_text}\""
                )
                if response and response.text:
                    json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                    if json_match:
                        parsed = json.loads(json_match.group(0))
                        parsed["raw_query"] = raw_text
                        parsed["parsed_by"] = "Gemini AI Model"
                        return parsed
            except Exception as e:
                print(f"[RequirementAgent] Gemini API fallback to local parser: {e}")

        # Intelligent Regex & Heuristic NLP Parser Fallback
        return self._heuristic_parse(raw_text)

    def _heuristic_parse(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()

        # 1. Category Detection
        category = "All"
        if any(w in text_lower for w in ["laptop", "notebook", "ultrabook", "macbook"]):
            category = "Laptops"
        elif any(w in text_lower for w in ["phone", "smartphone", "mobile", "iphone", "galaxy"]):
            category = "Smartphones"
        elif any(w in text_lower for w in ["headphone", "earbud", "audio", "headset", "anc", "airpods", "tws"]):
            category = "Headphones"
        elif any(w in text_lower for w in ["watch", "smartwatch", "apple watch", "fitbit", "garmin"]):
            category = "Smartwatches"
        elif any(w in text_lower for w in ["tablet", "ipad", "tab"]):
            category = "Tablets"

        # 2. Price Extraction (Rupees ₹, Lakhs, K, Numbers)
        max_price = None
        min_price = None

        # Lakhs check (e.g. 1.5 lakh, 1 lakh)
        lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|l)\b', text_lower)
        if lakh_match:
            try:
                max_price = float(lakh_match.group(1)) * 100000
            except ValueError:
                pass

        # Thousands K check (e.g. 50k, 10k, 40k)
        if not max_price:
            k_match = re.search(r'(\d+(?:\.\d+)?)\s*k\b', text_lower)
            if k_match:
                try:
                    max_price = float(k_match.group(1)) * 1000
                except ValueError:
                    pass

        # Under/Below/Max Price pattern
        if not max_price:
            under_match = re.search(r'(?:under|below|less than|max|budget of|within|rs\.?|inr|₹)\s*₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)', text_lower)
            if under_match:
                try:
                    val = float(under_match.group(1).replace(',', ''))
                    # If number is small like 500, check if user meant 50000 or USD
                    if val < 5000 and "laptop" in text_lower:
                        val = val * 85 # treat as USD if laptop under 500/1000
                    max_price = val
                except ValueError:
                    pass

        # Direct numbers if no explicit budget keyword found but category is present
        if not max_price:
            num_matches = re.findall(r'\b(\d{4,6})\b', text_lower)
            if num_matches:
                try:
                    max_price = float(num_matches[0])
                except ValueError:
                    pass

        # 3. Brand Detection
        known_brands = [
            "Apple", "HP", "Dell", "Lenovo", "ASUS", "Acer", "Samsung", "Google",
            "OnePlus", "Xiaomi", "Redmi", "POCO", "Nothing", "Sony", "Bose",
            "boAt", "Anker", "Noise", "Garmin", "Amazfit"
        ]
        detected_brand = None
        for b in known_brands:
            if b.lower() in text_lower:
                detected_brand = b
                break

        # 4. Mandatory Specs & Features
        mandatory_specs = []
        if "16gb" in text_lower or "16 gb" in text_lower:
            mandatory_specs.append("16GB RAM")
        elif "8gb" in text_lower or "8 gb" in text_lower:
            mandatory_specs.append("8GB RAM")
        elif "32gb" in text_lower or "32 gb" in text_lower:
            mandatory_specs.append("32GB RAM")

        if "512gb" in text_lower or "512 gb" in text_lower:
            mandatory_specs.append("512GB SSD")
        elif "1tb" in text_lower or "1 tb" in text_lower:
            mandatory_specs.append("1TB SSD")
        elif "256gb" in text_lower or "256 gb" in text_lower:
            mandatory_specs.append("256GB Storage")

        if "anc" in text_lower or "noise cancel" in text_lower or "noise-cancel" in text_lower:
            mandatory_specs.append("Active Noise Cancellation (ANC)")
        if "camera" in text_lower or "photo" in text_lower:
            mandatory_specs.append("High Resolution Camera")
        if "battery" in text_lower or "long battery" in text_lower:
            mandatory_specs.append("Long Battery Life")
        if "gaming" in text_lower or "rtx" in text_lower:
            mandatory_specs.append("Gaming Graphics")
        if "oled" in text_lower or "amoled" in text_lower:
            mandatory_specs.append("OLED Display")

        # 5. Intended Use Case
        intended_use = "General Usage"
        if "programming" in text_lower or "coding" in text_lower or "developer" in text_lower:
            intended_use = "Software Engineering & Programming"
        elif "gaming" in text_lower:
            intended_use = "AAA Gaming & Graphics Work"
        elif "editing" in text_lower or "video" in text_lower:
            intended_use = "Content Creation & Video Editing"
        elif "student" in text_lower or "college" in text_lower or "school" in text_lower:
            intended_use = "Student & Academic Study"
        elif "office" in text_lower or "business" in text_lower or "work" in text_lower:
            intended_use = "Business & Productivity"

        # 6. Sorting preferences
        sort_by = "relevance"
        if "cheapest" in text_lower or "low price" in text_lower or "cheap" in text_lower:
            sort_by = "price_asc"
        elif "expensive" in text_lower or "high end" in text_lower or "premium" in text_lower:
            sort_by = "price_desc"
        elif "top rated" in text_lower or "best" in text_lower:
            sort_by = "rating_desc"

        return {
            "raw_query": text,
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "brand": detected_brand,
            "mandatory_specs": mandatory_specs,
            "optional_preferences": [f"Optimized for {intended_use}"],
            "intended_use": intended_use,
            "sort_by": sort_by,
            "parsed_by": "Rule-Based Natural Language Engine"
        }

    def _empty_intent(self) -> Dict[str, Any]:
        return {
            "raw_query": "",
            "category": "All",
            "min_price": None,
            "max_price": None,
            "brand": None,
            "mandatory_specs": [],
            "optional_preferences": [],
            "intended_use": "General",
            "sort_by": "relevance",
            "parsed_by": "Default"
        }
