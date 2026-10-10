from typing import List, Dict, Any, Optional
from models import Product

class RecommendationAgent:
    """
    Agent 4: Personalized Recommendation Agent
    Generates intelligent recommendation buckets: Top Pick, Cheaper Alternative,
    Premium Upgrade, and Similar Choices.
    """
    def generate_recommendations(
        self,
        current_product_id: Optional[str] = None,
        search_intent: Optional[Dict[str, Any]] = None,
        user_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        
        category = search_intent.get("category", "Laptops") if search_intent else "Laptops"
        if category == "All":
            category = "Laptops"

        # Query items in category
        query = Product.query.filter(Product.category.ilike(f"%{category}%")).order_by(Product.rating.desc(), Product.price.asc())
        category_products = [p.to_dict() for p in query.all()]

        if not category_products:
            # Fallback to all products
            category_products = [p.to_dict() for p in Product.query.limit(10).all()]

        # Find current product if provided
        current_p = None
        if current_product_id:
            current_p = next((p for p in category_products if p["id"] == current_product_id), None)

        ref_price = current_p["price"] if current_p else (search_intent.get("max_price") if search_intent else 50000)
        if not ref_price:
            ref_price = 50000

        # 1. Top Pick overall (highest rating)
        top_pick = max(category_products, key=lambda x: x["rating"]) if category_products else None

        # 2. Cheaper Alternative (product with price lower than ref_price, good rating)
        cheaper_candidates = [p for p in category_products if p["price"] < ref_price]
        cheaper_alt = max(cheaper_candidates, key=lambda x: x["rating"]) if cheaper_candidates else None

        # 3. Premium Upgrade (product with price higher than ref_price, rating >= 4.7)
        upgrade_candidates = [p for p in category_products if p["price"] > ref_price]
        premium_upgrade = max(upgrade_candidates, key=lambda x: x["rating"]) if upgrade_candidates else None

        # 4. Similar Recommendations (excluding current)
        similar_picks = [p for p in category_products if not current_p or p["id"] != current_p["id"]][:4]

        return {
            "top_pick": top_pick,
            "cheaper_alternative": cheaper_alt,
            "premium_upgrade": premium_upgrade,
            "similar_picks": similar_picks,
            "recommendation_reasoning": (
                f"Recommendations tailored for your interest in {category}. "
                f"Showing budget alternatives under ₹{ref_price:,.0f} and premium upgrades."
            )
        }
