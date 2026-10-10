import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from config import BASE_DIR
from database import init_db, query_products, get_product_by_id, get_all_categories
from agents.orchestrator import MultiAgentOrchestrator
from agents.comparison_agent import ProductComparisonAgent

app = FastAPI(
    title="Multi-Agent Product Requirements & Comparison Engine",
    version="1.0.0",
    description="Backend API powered by multi-agent AI pipeline for requirement extraction, product catalog search/filtering, spec comparison, and recommendations."
)

# Initialize Database on launch
init_db()

orchestrator = MultiAgentOrchestrator()
comp_agent = ProductComparisonAgent()

# Static Files Path
STATIC_DIR = BASE_DIR.parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class RequirementRequest(BaseModel):
    requirement_text: str

class CustomCompareRequest(BaseModel):
    product_ids: List[str]
    user_requirement: Optional[str] = "Manual product selection comparison."

@app.get("/")
def read_root():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Multi-Agent Product Comparison API is running."}

@app.post("/api/pipeline/run")
def run_agent_pipeline(req: RequirementRequest):
    if not req.requirement_text or not req.requirement_text.strip():
        raise HTTPException(status_code=400, detail="Requirement text cannot be empty.")
    
    result = orchestrator.run_pipeline(req.requirement_text)
    return result

@app.get("/api/products")
def get_products(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    search: Optional[str] = None
):
    products = query_products(
        category=category,
        max_price=max_price,
        min_price=min_price,
        min_rating=min_rating,
        query_text=search
    )
    return {"count": len(products), "products": products}

@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

@app.get("/api/categories")
def list_categories():
    return {"categories": get_all_categories()}

@app.post("/api/compare")
def compare_selected_products(req: CustomCompareRequest):
    candidates = []
    for pid in req.product_ids:
        p = get_product_by_id(pid)
        if p:
            p["match_score"] = 90
            candidates.append(p)
            
    if not candidates:
        raise HTTPException(status_code=400, detail="No valid product IDs provided.")
        
    result = comp_agent.process(candidates, req.user_requirement or "Manual selection", {})
    return {"candidates": candidates, "comparison": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
