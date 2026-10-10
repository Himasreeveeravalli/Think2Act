from typing import List, Dict, Any

class ComparisonAgent:
    """
    Agent 3: Product Comparison Agent
    Generates comprehensive side-by-side specification matrices (including all product attributes),
    pros/cons analysis, rating evaluations, and AI winner recommendation.
    """
    def process_comparison(
        self,
        products: List[Dict[str, Any]],
        user_intent: Dict[str, Any]
    ) -> Dict[str, Any]:
        if not products:
            return {"error": "No products selected for comparison."}

        # 1. Collect all unique technical specification keys across all selected products
        spec_keys = set()
        for p in products:
            for k in p.get("specs", {}).keys():
                spec_keys.add(k)

        # Logical sorting of specification keys
        priority_order = [
            "Processor", "RAM", "Storage", "Display", "Graphics", "Battery", "Battery Life",
            "Weight", "OS", "Noise Cancelling", "Type", "Drivers", "Audio", "Bluetooth",
            "Codecs", "Sensors", "GPS", "Water Resistance", "Pen", "Calling", "Dimensions",
            "Stock Status", "Discount", "Charging"
        ]
        sorted_keys = [k for k in priority_order if k in spec_keys]
        sorted_keys.extend([k for k in sorted(spec_keys) if k not in sorted_keys])

        # 2. Build Comprehensive Matrix
        matrix = []

        # --- SECTION: GENERAL INFORMATION ---
        matrix.append({
            "section": "General Overview",
            "feature": "Brand",
            "values": {p["id"]: p.get('brand', 'N/A') for p in products}
        })
        matrix.append({
            "section": "General Overview",
            "feature": "Model / Edition",
            "values": {p["id"]: p.get('model', 'Standard Edition') or 'N/A' for p in products}
        })
        matrix.append({
            "section": "General Overview",
            "feature": "Category",
            "values": {p["id"]: p.get('category', 'N/A') for p in products}
        })
        matrix.append({
            "section": "General Overview",
            "feature": "Data Source",
            "values": {p["id"]: p.get('source', 'Catalog') for p in products}
        })

        # --- SECTION: PRICE & POPULARITY ---
        matrix.append({
            "section": "Price & Ratings",
            "feature": "Price",
            "values": {p["id"]: f"{p.get('currency', '₹')}{p.get('price', 0):,.0f}" for p in products}
        })
        matrix.append({
            "section": "Price & Ratings",
            "feature": "Customer Rating",
            "values": {p["id"]: f"⭐ {p.get('rating', 0)} / 5.0" for p in products}
        })
        matrix.append({
            "section": "Price & Ratings",
            "feature": "User Reviews Count",
            "values": {p["id"]: f"{p.get('review_count', 0):,} verified reviews" for p in products}
        })

        # --- SECTION: SUMMARY & TAGS ---
        matrix.append({
            "section": "Overview & Highlights",
            "feature": "Description Summary",
            "values": {p["id"]: p.get('description', 'No description available.') for p in products}
        })
        matrix.append({
            "section": "Overview & Highlights",
            "feature": "Key Tags / Highlights",
            "values": {p["id"]: ", ".join(p.get('tags', [])) if p.get('tags') else 'Standard' for p in products}
        })

        # --- SECTION: ALL TECHNICAL SPECIFICATIONS ---
        for key in sorted_keys:
            matrix.append({
                "section": "Technical Specifications",
                "feature": key,
                "values": {p["id"]: p.get("specs", {}).get(key, "N/A") for p in products}
            })

        # 3. Analyze Pros, Cons, and Score per Product
        product_analysis = {}
        winner_id = None
        best_score = -1

        intended_use = user_intent.get("intended_use", "General Usage")
        max_budget = user_intent.get("max_price")

        for p in products:
            pros = []
            cons = []
            calc_score = p.get("match_score", 70)

            # Rating evaluation
            if p.get("rating", 0) >= 4.7:
                pros.append(f"Top-tier user satisfaction rating (⭐ {p['rating']})")
                calc_score += 10
            elif p.get("rating", 0) < 4.2:
                cons.append(f"Lower user rating compared to peers (⭐ {p['rating']})")
                calc_score -= 5

            # Price evaluation
            if max_budget and p["price"] <= max_budget * 0.8:
                pros.append(f"Great budget saver (₹{max_budget - p['price']:,.0f} under budget)")
                calc_score += 8
            elif max_budget and p["price"] > max_budget:
                cons.append("Exceeds target budget limit")
                calc_score -= 15

            # Specs evaluation
            specs = p.get("specs", {})
            if "RAM" in specs and ("16GB" in specs["RAM"] or "18GB" in specs["RAM"] or "32GB" in specs["RAM"]):
                pros.append(f"High memory capacity ({specs['RAM']})")
            if "Storage" in specs and ("512GB" in specs["Storage"] or "1TB" in specs["Storage"]):
                pros.append(f"Fast NVMe SSD storage ({specs['Storage']})")
            if "Battery" in specs or "Battery Life" in specs:
                bat_val = str(specs.get("Battery") or specs.get("Battery Life"))
                if any(x in bat_val.lower() for x in ["18 hours", "30 hours", "40 hours", "14 days", "5000 mah"]):
                    pros.append(f"Long battery life ({bat_val})")
            if "Display" in specs and ("OLED" in specs["Display"] or "120Hz" in specs["Display"] or "Retina" in specs["Display"]):
                pros.append(f"High quality display ({specs['Display']})")
            if "Noise Cancelling" in specs and "ANC" in str(specs["Noise Cancelling"]):
                pros.append(f"Active Noise Cancellation ({specs['Noise Cancelling']})")

            if not pros:
                pros.append("Solid overall build quality and features")
            if not cons:
                cons.append("No major drawbacks identified")

            product_analysis[p["id"]] = {
                "pros": pros,
                "cons": cons,
                "score": min(100, max(20, calc_score))
            }

            if calc_score > best_score:
                best_score = calc_score
                winner_id = p["id"]

        winner_product = next((p for p in products if p["id"] == winner_id), products[0])

        return {
            "matrix": matrix,
            "product_analysis": product_analysis,
            "winner": {
                "product_id": winner_product["id"],
                "name": winner_product["name"],
                "reason": f"Selected as the Best Overall Match for {intended_use} with optimal specifications."
            }
        }
