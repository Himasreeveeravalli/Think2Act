import re
from typing import Dict, Any
from .base_agent import BaseAgent

class RequirementUnderstandingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Requirement Understanding Agent",
            role="Extract structured product specifications, budget limits (in ₹ Rupees), category, and user priorities from raw text requirements."
        )

    def process(self, raw_requirement: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert product requirements analyst. "
            "Given a user requirement, extract: category, max_price (in INR Rupees), min_price, min_rating, brand, key_features, use_case, and trade_offs. "
            "Respond ONLY with a valid JSON object."
        )
        
        prompt = f"Analyze these product requirements and extract constraints in Indian Rupees (₹):\n\"{raw_requirement}\""
        
        # Try LLM call
        llm_response = self.call_ollama(prompt, system_prompt)
        parsed_json = None
        if llm_response:
            parsed_json = self.extract_json_from_text(llm_response)
            
        if not parsed_json:
            # Smart Fallback Parser logic
            parsed_json = self._rule_based_analysis(raw_requirement)
            formatted_price = f"₹{parsed_json['max_price']:,.0f}" if parsed_json['max_price'] else 'Flexible'
            llm_response = (
                f"[Agent Thought Process]\n"
                f"1. Natural language requirement analyzed: '{raw_requirement}'\n"
                f"2. Extracted Category: {parsed_json['category']}\n"
                f"3. Extracted Max Budget: {formatted_price}\n"
                f"4. Key Specifications/Tags identified: {', '.join(parsed_json['key_features']) or 'General'}\n"
                f"5. Primary Use-case: {parsed_json['use_case']}"
            )
            
        return {
            "agent_name": self.name,
            "role": self.role,
            "parsed_constraints": parsed_json,
            "thought_trace": llm_response or "Analysis complete."
        }

    def _rule_based_analysis(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # Category detection
        category = "All"
        if any(w in text_lower for w in ["laptop", "notebook", "ultrabook", "macbook"]):
            category = "Laptops"
        elif any(w in text_lower for w in ["phone", "smartphone", "mobile"]):
            category = "Smartphones"
        elif any(w in text_lower for w in ["headphone", "earbud", "audio", "headset", "anc"]):
            category = "Headphones"
        elif any(w in text_lower for w in ["monitor", "display", "screen"]):
            category = "Monitors"
        elif any(w in text_lower for w in ["chair", "desk", "furniture"]):
            category = "Furniture"
            
        # Max price extraction in INR (handles lakh, k, rupees, ₹, under)
        max_price = None
        
        # Lakhs detection (e.g., 1.5 lakh, 1 lakh)
        lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|l)', text_lower)
        if lakh_match:
            try:
                max_price = float(lakh_match.group(1)) * 100000
            except ValueError:
                pass
                
        # Thousands k detection (e.g. 80k, 150k, 30k)
        if not max_price:
            k_match = re.search(r'(\d+(?:\.\d+)?)\s*k\b', text_lower)
            if k_match:
                try:
                    max_price = float(k_match.group(1)) * 1000
                except ValueError:
                    pass

        # Direct digits detection (₹1,50,000 or under 150000 or under 80000)
        if not max_price:
            price_matches = re.findall(r'(?:under|below|max|budget of|₹|rs\.?|inr)\s*₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)', text_lower)
            if price_matches:
                try:
                    clean_str = price_matches[0].replace(',', '')
                    val = float(clean_str)
                    # If user typed small USD number like 1500, treat as USD equivalent ~₹125,000 or direct INR
                    if val < 5000:
                        val = val * 85
                    max_price = val
                except ValueError:
                    max_price = None

        # Brand detection
        brand = None
        for b in ["TechApex", "Visionary", "Zenith", "SoundCraft", "ErgoFlex"]:
            if b.lower() in text_lower:
                brand = b
                break

        # Min rating detection
        min_rating = 4.0 if "high quality" in text_lower or "top rated" in text_lower or "best" in text_lower else 3.5

        # Feature extraction
        key_features = []
        if "gaming" in text_lower or "rtx" in text_lower:
            key_features.append("Gaming & GPU")
        if "ram" in text_lower or "16gb" in text_lower or "32gb" in text_lower:
            key_features.append("High Memory")
        if "battery" in text_lower or "travel" in text_lower:
            key_features.append("Battery Life")
        if "oled" in text_lower or "4k" in text_lower or "display" in text_lower:
            key_features.append("High-Res Display")
        if "anc" in text_lower or "noise" in text_lower:
            key_features.append("Active Noise Cancellation")

        use_case = "General Usage"
        if "gaming" in text_lower:
            use_case = "AAA Gaming & Graphics"
        elif "student" in text_lower or "college" in text_lower:
            use_case = "Student / Portability"
        elif "work" in text_lower or "editing" in text_lower or "office" in text_lower:
            use_case = "Professional Work & Content Creation"

        return {
            "category": category,
            "max_price": max_price,
            "min_price": None,
            "min_rating": min_rating,
            "brand": brand,
            "key_features": key_features,
            "use_case": use_case,
            "trade_offs": f"Focusing on best {category} balance for {use_case} within budget."
        }
