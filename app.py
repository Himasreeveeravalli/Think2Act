import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db, User, Product, SearchHistory, SavedComparison
from services.catalog_seeder import seed_database
from agents.requirement_agent import RequirementAgent
from agents.search_agent import SearchAgent
from agents.comparison_agent import ComparisonAgent
from agents.recommendation_agent import RecommendationAgent

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize Multi-Agent Instances
req_agent = RequirementAgent()
search_agent = SearchAgent()
comp_agent = ComparisonAgent()
rec_agent = RecommendationAgent()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Initialize database tables & seed catalog on app launch
with app.app_context():
    db.create_all()
    seed_database()


# --------------------------------------------------------------------------
# Auth Routes
# --------------------------------------------------------------------------
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validations
        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Password confirmation does not match.', 'danger')
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists. Please sign in.', 'danger')
            return render_template('auth/register.html')

        # Create user
        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please sign in to your new account.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password. Please try again.', 'danger')
            return render_template('auth/login.html')

        login_user(user, remember=remember)
        flash(f'Welcome back, {user.full_name}!', 'success')

        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard'))

    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# --------------------------------------------------------------------------
# Dashboard & Core Shopping Routes
# --------------------------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch featured recommended products
    featured = Product.query.order_by(Product.rating.desc()).limit(8).all()
    featured_dicts = [p.to_dict() for p in featured]
    
    return render_template(
        'dashboard/index.html',
        featured_products=featured_dicts
    )

@app.route('/search')
@login_required
def search():
    raw_query = request.args.get('q', '').strip()
    selected_category = request.args.get('category', 'All')
    selected_max_price = request.args.get('max_price', type=float)
    selected_sort = request.args.get('sort_by', 'relevance')
    page = request.args.get('page', 1, type=int)

    # Agent 1: Extract Natural Language Intent
    if raw_query:
        intent = req_agent.process(raw_query)
    else:
        intent = {
            "raw_query": "",
            "category": selected_category,
            "max_price": selected_max_price,
            "min_price": None,
            "brand": None,
            "mandatory_specs": [],
            "intended_use": "General Search",
            "sort_by": selected_sort,
            "parsed_by": "Manual Filters"
        }

    # Override intent with explicit URL filters if provided
    if selected_category and selected_category != 'All':
        intent["category"] = selected_category
    if selected_max_price:
        intent["max_price"] = selected_max_price
    if selected_sort:
        intent["sort_by"] = selected_sort

    # Agent 2: Search Catalog & Live Market
    is_live = session.get('is_live_mode', False)
    search_response = search_agent.search_products(
        intent=intent,
        is_live_mode=is_live,
        page=page,
        per_page=12
    )

    # Log Search History if query exists
    if raw_query:
        history = SearchHistory(
            user_id=current_user.id,
            raw_query=raw_query,
            extracted_intent=json.dumps(intent),
            results_count=search_response["total_count"]
        )
        db.session.add(history)
        db.session.commit()

    return render_template(
        'dashboard/search.html',
        products=search_response["products"],
        total_count=search_response["total_count"],
        page=search_response["page"],
        total_pages=search_response["total_pages"],
        intent=intent,
        selected_category=intent.get("category", "All"),
        selected_max_price=intent.get("max_price"),
        selected_sort=intent.get("sort_by", "relevance")
    )

@app.route('/compare')
@login_required
def compare_page():
    compare_ids = session.get('compare_ids', [])
    
    # Also support product_id query params
    param_ids = request.args.getlist('id')
    if param_ids:
        compare_ids = list(set(compare_ids + param_ids))

    selected_products = []
    for pid in compare_ids:
        p = Product.query.get(pid)
        if p:
            selected_products.append(p.to_dict())
        else:
            # Check live market search for ID
            live_item = search_agent.market_service.search_live_market(query=pid)
            if live_item:
                selected_products.append(live_item[0])

    if not selected_products:
        return render_template(
            'dashboard/compare.html',
            products=[],
            matrix=[],
            product_analysis={},
            winner=None
        )

    # Default query intent for comparison
    intent = {
        "category": selected_products[0]["category"] if selected_products else "All",
        "intended_use": "Comprehensive Comparison"
    }

    # Agent 3: Generate Spec Matrix, Pros/Cons & Winner
    comp_result = comp_agent.process_comparison(selected_products, intent)

    return render_template(
        'dashboard/compare.html',
        products=selected_products,
        matrix=comp_result.get("matrix", []),
        product_analysis=comp_result.get("product_analysis", {}),
        winner=comp_result.get("winner")
    )

@app.route('/recommendations')
@login_required
def recommendations_page():
    current_pid = request.args.get('product_id')
    
    # Get user's recent search intent if available
    recent_history = SearchHistory.query.filter_by(user_id=current_user.id).order_by(SearchHistory.timestamp.desc()).first()
    intent = recent_history.get_intent_dict() if recent_history else {"category": "Laptops"}

    # Agent 4: Generate Personalized Recommendations
    recs = rec_agent.generate_recommendations(
        current_product_id=current_pid,
        search_intent=intent
    )

    return render_template(
        'dashboard/recommendations.html',
        recs=recs
    )

@app.route('/history')
@login_required
def history_page():
    history_items = SearchHistory.query.filter_by(user_id=current_user.id).order_by(SearchHistory.timestamp.desc()).all()
    return render_template(
        'dashboard/history.html',
        history_items=history_items
    )

@app.route('/clear-history', methods=['POST'])
@login_required
def clear_history():
    SearchHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Your search history log has been cleared.', 'info')
    return redirect(url_for('history_page'))


# --------------------------------------------------------------------------
# API Endpoints
# --------------------------------------------------------------------------
@app.route('/api/toggle-live-mode', methods=['POST'])
@csrf.exempt
def toggle_live_mode():
    data = request.get_json() or {}
    is_live = bool(data.get('is_live', False))
    session['is_live_mode'] = is_live
    return jsonify({"status": "success", "is_live_mode": is_live})

@app.route('/api/update-compare-session', methods=['POST'])
@csrf.exempt
def update_compare_session():
    data = request.get_json() or {}
    product_ids = data.get('product_ids', [])
    session['compare_ids'] = product_ids[:4]
    return jsonify({"status": "success", "compare_ids": session['compare_ids']})


if __name__ == '__main__':
    print("=================================================================")
    print(" Starting AI Multi-Agent E-Commerce Shopping Assistant Studio")
    print(" Server running at: http://127.0.0.1:5000")
    print("=================================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
