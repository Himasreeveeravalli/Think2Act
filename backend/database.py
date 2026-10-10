import json
import sqlite3
from typing import List, Dict, Any, Optional
from config import DB_PATH, SEED_JSON_PATH

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed: bool = False):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    if force_reseed and DB_PATH.exists():
        try:
            DB_PATH.unlink()
        except Exception:
            pass

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        rating REAL NOT NULL,
        review_count INTEGER DEFAULT 0,
        image_url TEXT,
        tags TEXT, -- stored as JSON string
        specs TEXT, -- stored as JSON string
        description TEXT
    );
    """)
    conn.commit()
    
    # Check if image_url column exists in old database structure
    cursor.execute("PRAGMA table_info(products)")
    columns = [row["name"] for row in cursor.fetchall()]
    if "image_url" not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
        conn.commit()

    # Seed or Update products from JSON
    if SEED_JSON_PATH.exists():
        with open(SEED_JSON_PATH, "r", encoding="utf-8") as f:
            seed_data = json.load(f)
            for item in seed_data:
                cursor.execute("""
                    INSERT OR REPLACE INTO products (id, name, category, brand, price, rating, review_count, image_url, tags, specs, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item["id"],
                    item["name"],
                    item["category"],
                    item["brand"],
                    item["price"],
                    item["rating"],
                    item.get("review_count", 0),
                    item.get("image_url", ""),
                    json.dumps(item.get("tags", [])),
                    json.dumps(item.get("specs", {})),
                    item.get("description", "")
                ))
            conn.commit()
    conn.close()

def query_products(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    brand: Optional[str] = None,
    query_text: Optional[str] = None
) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if category and category.lower() != "all":
        sql += " AND LOWER(category) LIKE ?"
        params.append(f"%{category.lower()}%")
        
    if max_price is not None:
        sql += " AND price <= ?"
        params.append(max_price)
        
    if min_price is not None:
        sql += " AND price >= ?"
        params.append(min_price)
        
    if min_rating is not None:
        sql += " AND rating >= ?"
        params.append(min_rating)

    if brand:
        sql += " AND LOWER(brand) LIKE ?"
        params.append(f"%{brand.lower()}%")
        
    if query_text:
        sql += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(tags) LIKE ?)"
        term = f"%{query_text.lower()}%"
        params.extend([term, term, term])
        
    sql += " ORDER BY rating DESC, price ASC"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        item = dict(row)
        item["tags"] = json.loads(item["tags"]) if item["tags"] else []
        item["specs"] = json.loads(item["specs"]) if item["specs"] else {}
        products.append(item)
        
    return products

def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    item["tags"] = json.loads(item["tags"]) if item["tags"] else []
    item["specs"] = json.loads(item["specs"]) if item["specs"] else {}
    return item

def get_all_categories() -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [r["category"] for r in rows]
