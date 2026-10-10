import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    search_histories = db.relationship('SearchHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_comparisons = db.relationship('SavedComparison', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False, index=True)
    currency = db.Column(db.String(10), default="₹")
    rating = db.Column(db.Float, default=4.0)
    review_count = db.Column(db.Integer, default=0)
    image_url = db.Column(db.Text, nullable=True)
    product_url = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    specs_json = db.Column(db.Text, nullable=True) # JSON string
    tags_json = db.Column(db.Text, nullable=True)  # JSON string
    source = db.Column(db.String(50), default="Demo Inventory")
    is_live = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def specs(self):
        if self.specs_json:
            try:
                return json.loads(self.specs_json)
            except Exception:
                return {}
        return {}

    @specs.setter
    def specs(self, val):
        self.specs_json = json.dumps(val)

    @property
    def tags(self):
        if self.tags_json:
            try:
                return json.loads(self.tags_json)
            except Exception:
                return []
        return []

    @tags.setter
    def tags(self, val):
        self.tags_json = json.dumps(val)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "model": self.model or "",
            "category": self.category,
            "price": self.price,
            "currency": self.currency,
            "rating": self.rating,
            "review_count": self.review_count,
            "image_url": self.image_url,
            "product_url": self.product_url or "#",
            "description": self.description or "",
            "specs": self.specs,
            "tags": self.tags,
            "source": self.source,
            "is_live": self.is_live
        }


class SearchHistory(db.Model):
    __tablename__ = 'search_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    raw_query = db.Column(db.Text, nullable=False)
    extracted_intent = db.Column(db.Text, nullable=True) # JSON string
    results_count = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def get_intent_dict(self):
        if self.extracted_intent:
            try:
                return json.loads(self.extracted_intent)
            except Exception:
                return {}
        return {}


class SavedComparison(db.Model):
    __tablename__ = 'saved_comparisons'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    product_ids_json = db.Column(db.Text, nullable=False) # JSON array of product IDs
    summary = db.Column(db.Text, nullable=True)
    winner_id = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def product_ids(self):
        try:
            return json.loads(self.product_ids_json)
        except Exception:
            return []
