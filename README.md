# Multi-Agent Product Requirements & Comparison Studio

An intelligent full-stack system powered by a **3-Agent AI Pipeline** that understands natural language product requirements, searches and filters a customizable catalog database, and generates interactive side-by-side spec comparison matrices.

---

## 🤖 Multi-Agent Architecture

```
[ Natural Language User Request ]
               │
               ▼
┌──────────────────────────────────────────────┐
│  Agent 1: Requirement Understanding Agent     │
│  • Parses category, budget, specs & use-case │
└──────────────────────┬───────────────────────┘
                       │ Constraints JSON
                       ▼
┌──────────────────────────────────────────────┐
│  Agent 2: Catalog Search & Filtering Agent    │
│  • Queries SQLite database & scores match %  │
└──────────────────────┬───────────────────────┘
                       │ Ranked Candidates
                       ▼
┌──────────────────────────────────────────────┐
│  Agent 3: Comparison & Synthesis Agent        │
│  • Generates spec matrix, pros/cons & winner │
└──────────────────────┬───────────────────────┘
                       │ Final Payload
                       ▼
[ Interactive Dashboard Frontend (HTML / JS / Tailwind) ]
```

### Agent Roles:
1. **Requirement Analyst Agent (`backend/agents/requirement_agent.py`)**: Extracts category, max/min budget, key feature requirements, rating thresholds, and trade-offs.
2. **Catalog Search & Filter Agent (`backend/agents/filter_agent.py`)**: Queries SQLite product catalog, applies constraint filters, and ranks candidate products by dynamic match score.
3. **Product Comparison Agent (`backend/agents/comparison_agent.py`)**: Synthesizes side-by-side feature grids, pros & cons, and selects top overall winner & best budget alternative.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- Installed packages: `fastapi`, `uvicorn`, `pydantic`, `requests`

### Running the Application

To launch the backend server & frontend dashboard:

```bash
python run.py
```

Open your browser at: **`http://127.0.0.1:8000`**

---

## 📂 Project Structure

```
product-comparison-agents/
├── backend/
│   ├── app.py                   # FastAPI REST server & static host
│   ├── config.py                # System & LLM configuration
│   ├── database.py              # SQLite database manager & seeds
│   ├── agents/
│   │   ├── base_agent.py        # Base agent with Ollama/HF/Fallback handler
│   │   ├── requirement_agent.py # Agent 1: NLP requirement parser
│   │   ├── filter_agent.py      # Agent 2: Catalog searcher & match scorer
│   │   ├── comparison_agent.py  # Agent 3: Spec matrix builder & pros/cons
│   │   └── orchestrator.py      # Multi-Agent Workflow Coordinator
│   └── data/
│       └── catalog_seed.json    # Customizable seed product dataset
├── static/
│   ├── index.html               # Frontend dashboard UI
│   ├── app.js                   # Interactive client-side state & API consumer
│   └── styles.css               # Styling & agent trace step cards
├── requirements.txt             # Dependency list
├── run.py                       # One-click launcher
└── README.md                    # System documentation
```

---

## 🔌 API Endpoints

- `POST /api/pipeline/run` - Executes the full multi-agent pipeline from raw prompt text.
- `GET /api/products` - Filter catalog products by category, price, search keyword.
- `GET /api/categories` - Returns distinct catalog categories.
- `POST /api/compare` - Compare arbitrary list of product IDs selected manually.

---

## 💡 LLM Engine Options

- **Ollama / Local LLM**: If Ollama is running locally at `http://localhost:11434`, agents automatically leverage local models (e.g. `llama3`, `mistral`, `phi3`).
- **Built-in Smart Fallback Engine**: If no LLM endpoint is active, the system automatically uses structured rule-based NLP extraction so it runs 100% out-of-the-box without requiring API keys.
