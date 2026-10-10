from typing import Dict, Any, List
from .base_agent import BaseAgent

class ProductComparisonAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Product Comparison & Recommendation Agent",
            role="Generate side-by-side comparisons, pros/cons analysis, spec matrix, and curated recommendations in Rupees (₹)."
        )

    def process(self, candidates: List[Dict[str, Any]], user_requirement: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        if not candidates:
            return {
                "agent_name": self.name,
                "role": self.role,
                "recommendation": None,
                "comparison_matrix": [],
                "thought_trace": "No candidate products were found matching the specified constraints."
            }

        candidate_summaries = []
        for p in candidates:
            p_price = p['price']
            candidate_summaries.append(f"{p['name']} (₹{p_price:,.0f})")

        prompt = (
            f"User Requirement: {user_requirement}\n"
            f"Candidates: {candidate_summaries}\n"
            f"Compare these products, list key advantages for each, and pick the best winner."
        )
        llm_response = self.call_ollama(prompt, "You are an expert product analyst.")

        comparison_matrix = self._build_comparison_matrix(candidates)
        winner_overall = candidates[0]
        best_value = min(candidates, key=lambda x: x["price"])
        pro_cons_map = self._generate_pros_cons(candidates)

        winner_price_val = winner_overall['price']
        best_val_price_val = best_value['price']
        winner_price_fmt = f"₹{winner_price_val:,.0f}"
        best_val_price_fmt = f"₹{best_val_price_val:,.0f}"

        summary_narrative = (
            f"After evaluating {len(candidates)} candidate products against your requirements, "
            f"the **{winner_overall['name']}** emerges as the **Top Overall Winner** with a match score of {winner_overall['match_score']}%. "
            f"If budget optimization is your primary goal, the **{best_value['name']}** at {best_val_price_fmt} offers the best value proposition."
        )

        thought_trace = (
            f"[Agent Comparison & Synthesis]\n"
            f"1. Conducted side-by-side evaluation across {len(candidates)} shortlisted products.\n"
            f"2. Constructed multi-attribute spec comparison grid with Rupee pricing.\n"
            f"3. Derived product pros, cons, and target persona fit.\n"
            f"4. Selected Top Recommended Winner: {winner_overall['name']} ({winner_price_fmt})."
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "winner_overall": winner_overall,
            "best_value": best_value,
            "comparison_matrix": comparison_matrix,
            "pros_cons": pro_cons_map,
            "summary_narrative": summary_narrative,
            "thought_trace": llm_response or thought_trace
        }

    def _build_comparison_matrix(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        spec_keys = set()
        for c in candidates:
            spec_keys.update(c.get("specs", {}).keys())
            
        matrix = []
        
        price_values = {}
        for c in candidates:
            c_price = c['price']
            price_values[c['id']] = f"₹{c_price:,.0f}"

        matrix.append({
            "feature": "Price",
            "values": price_values
        })
        matrix.append({
            "feature": "Rating",
            "values": {c["id"]: f"★ {c['rating']} ({c.get('review_count', 0)} reviews)" for c in candidates}
        })
        matrix.append({
            "feature": "Match Score",
            "values": {c["id"]: f"{c['match_score']}%" for c in candidates}
        })

        for key in sorted(spec_keys):
            formatted_key = key.replace("_", " ").title()
            values_map = {}
            for c in candidates:
                val = c.get("specs", {}).get(key, "N/A")
                values_map[c["id"]] = str(val)
            matrix.append({
                "feature": formatted_key,
                "values": values_map
            })

        return matrix

    def _generate_pros_cons(self, candidates: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[str]]]:
        pros_cons = {}
        for c in candidates:
            pros = []
            cons = []
            
            if c["rating"] >= 4.7:
                pros.append("Outstanding user satisfaction rating")
            if c.get("review_count", 0) > 300:
                pros.append("Battle-tested with high review volume")
            
            specs = c.get("specs", {})
            if "ram_gb" in specs:
                if specs["ram_gb"] >= 32:
                    pros.append("High 32GB RAM capacity for multitasking & rendering")
                elif specs["ram_gb"] <= 8:
                    cons.append("8GB RAM may bottleneck heavy workloads")

            if "battery_hours" in specs:
                if specs["battery_hours"] >= 12:
                    pros.append("Exceptional all-day battery life")
                elif specs["battery_hours"] <= 6:
                    cons.append("Moderate battery life requiring frequent charging")

            if "gpu" in specs and "RTX" in specs["gpu"]:
                pros.append(f"Dedicated graphics card ({specs['gpu']})")

            if "weight_kg" in specs:
                if specs["weight_kg"] <= 1.3:
                    pros.append(f"Ultra portable ({specs['weight_kg']} kg)")
                elif specs["weight_kg"] > 2.0:
                    cons.append(f"Slightly heavier chassis ({specs['weight_kg']} kg)")

            if not pros:
                pros.append("Solid feature balance in its price tier")
            if not cons:
                cons.append("Higher demand may lead to stock variability")

            pros_cons[c["id"]] = {
                "pros": pros,
                "cons": cons
            }
        return pros_cons
