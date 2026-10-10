from typing import List, Dict, Any, Optional
from models import Product
from services.market_api import MarketAPIService

class SearchAgent:
    """
    Agent 2: Search & Filtering Agent
    Queries local catalog + live market feeds, applies constraints, normalizes results,
    computes relevance match scores, and provides pagination.
    """
    def __init__(self):
        self.market_service = MarketAPIService()

    def search_products(
        self,
        intent: Dict[str, Any],
        is_live_mode: bool = False,
        page: int = 1,
        per_page: int = 12
    ) -> Dict[str, Any]:
        
        category = intent.get("category", "All")
        max_price = intent.get("max_price")
        min_price = intent.get("min_price")
        brand = intent.get("brand")
        raw_query = intent.get("raw_query", "")
        sort_by = intent.get("sort_by", "relevance")
        mandatory_specs = intent.get("mandatory_specs", [])

        results = []

        # 1. Search Local Database
        query = Product.query
        
        if category and category.lower() != "all":
            query = query.filter(Product.category.ilike(f"%{category}%"))

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))

        # Fetch local candidates
        local_products = query.all()
        for p in local_products:
            p_dict = p.to_dict()
            p_dict["match_score"] = self._calculate_match_score(p_dict, intent)
            results.append(p_dict)

        # 2. Fetch Live Market Feed if in Live Mode or if local results are few
        if is_live_mode or len(results) < 4:
            live_results = self.market_service.search_live_market(
                query=raw_query or category,
                category=category,
                max_price=max_price
            )
            for item in live_results:
                # deduplicate by name similarity
                if not any(r["name"].lower() == item["name"].lower() for r in results):
                    item["match_score"] = self._calculate_match_score(item, intent)
                    results.append(item)

        # 3. Filter by text relevance if query text exists
        if raw_query and not (category != "All" or max_price or brand):
            q_terms = [t.lower() for t in raw_query.split() if len(t) > 2]
            if q_terms:
                filtered = []
                for p in results:
                    searchable_text = f"{p['name']} {p['brand']} {p['category']} {p['description']} {' '.join(p['tags'])}".lower()
                    if any(term in searchable_text for term in q_terms):
                        filtered.append(p)
                if filtered:
                    results = filtered

        # 4. Sorting
        if sort_by == "price_asc":
            results.sort(key=lambda x: x["price"])
        elif sort_by == "price_desc":
            results.sort(key=lambda x: x["price"], reverse=True)
        elif sort_by == "rating_desc":
            results.sort(key=lambda x: (x["rating"], x["match_score"]), reverse=True)
        else: # relevance
            results.sort(key=lambda x: (x["match_score"], x["rating"]), reverse=True)

        # 5. Pagination
        total_count = len(results)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_products = results[start_idx:end_idx]

        return {
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": max(1, (total_count + per_page - 1) // per_page),
            "products": paginated_products,
            "intent": intent
        }

    def _calculate_match_score(self, product: Dict[str, Any], intent: Dict[str, Any]) -> int:
        score = 70 # baseline score
        
        # Category match
        req_cat = intent.get("category", "All")
        if req_cat != "All" and req_cat.lower() in product["category"].lower():
            score += 10
            
        # Price constraint match
        max_price = intent.get("max_price")
        if max_price:
            p_price = product["price"]
            if p_price <= max_price:
                score += 10
                # Bonus if it's exceptionally good budget value
                if p_price <= max_price * 0.85:
                    score += 5
            else:
                score -= 25

        # Brand match
        req_brand = intent.get("brand")
        if req_brand and req_brand.lower() in product["brand"].lower():
            score += 10

        # Mandatory specs match
        mandatory_specs = intent.get("mandatory_specs", [])
        specs_str = str(product.get("specs", {})).lower() + " " + " ".join(product.get("tags", [])).lower()
        for spec in mandatory_specs:
            if any(term.lower() in specs_str for term in spec.split()):
                score += 5

        # Rating bonus
        if product.get("rating", 0) >= 4.5:
            score += 5

        return min(100, max(10, score))
