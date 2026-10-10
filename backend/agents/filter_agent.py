from typing import Dict, Any, List
from .base_agent import BaseAgent
from database import query_products

class CatalogSearchFilterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Catalog Search & Filter Agent",
            role="Query database, evaluate specification constraints, rank candidates by relevance match score."
        )

    def process(self, constraints: Dict[str, Any]) -> Dict[str, Any]:
        category = constraints.get("category")
        max_price = constraints.get("max_price")
        min_rating = constraints.get("min_rating")
        brand = constraints.get("brand")
        key_features = constraints.get("key_features", [])

        # Fetch initial dataset from SQLite
        raw_candidates = query_products(
            category=category,
            max_price=max_price,
            min_rating=min_rating,
            brand=brand
        )
        
        # If no strict category match, broaden to all candidates within budget
        if not raw_candidates and category != "All":
            raw_candidates = query_products(max_price=max_price, min_rating=min_rating)

        scored_candidates = []
        for prod in raw_candidates:
            score = self._calculate_match_score(prod, constraints)
            prod_copy = dict(prod)
            prod_copy["match_score"] = score
            scored_candidates.append(prod_copy)

        # Sort by match score descending
        scored_candidates.sort(key=lambda x: x["match_score"], reverse=True)

        thought_trace = (
            f"[Agent Search Execution]\n"
            f"1. Database query executed with filters: category='{category}', max_price={max_price}, min_rating={min_rating}.\n"
            f"2. Retrived {len(raw_candidates)} potential product candidate(s).\n"
            f"3. Evaluated feature alignment and calculated weighted match scores (Top score: {scored_candidates[0]['match_score']}% if candidates else 0%)."
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "candidate_count": len(scored_candidates),
            "candidates": scored_candidates[:5], # top 5 candidates
            "thought_trace": thought_trace
        }

    def _calculate_match_score(self, product: Dict[str, Any], constraints: Dict[str, Any]) -> int:
        score = 60 # base score
        
        max_price = constraints.get("max_price")
        if max_price and product["price"] <= max_price:
            score += 15
            # Extra points for being budget efficient (leaving room under max price)
            price_ratio = product["price"] / max_price
            if 0.6 <= price_ratio <= 0.95:
                score += 5

        # Rating score boost
        rating = product.get("rating", 0)
        score += int((rating / 5.0) * 15)

        # Tag / Feature matching
        prod_tags = [t.lower() for t in product.get("tags", [])]
        prod_name = product["name"].lower()
        prod_desc = product.get("description", "").lower()
        
        key_features = [f.lower() for f in constraints.get("key_features", [])]
        for feature in key_features:
            if any(feature in t for t in prod_tags) or feature in prod_name or feature in prod_desc:
                score += 10

        # Cap score at 99
        return min(99, score)
