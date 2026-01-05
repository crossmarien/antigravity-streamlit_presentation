# AI Private Banking Dashboard - Implementation Blueprint

## 1. Project Structure
```text
ai_pb_dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI Application entry point
│   ├── api/                    # API Route definitions
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Auth dependencies
│   │   ├── routes_dashboard.py # PB Command Center endpoints
│   │   ├── routes_clients.py   # Client 360 endpoints
│   │   ├── routes_ai.py        # AI Generation & Streaming
│   │   ├── routes_compliance.py# Suitability checks
│   │   └── routes_audit.py     # Audit trail access
│   ├── core/                   # Core configs & security
│   │   ├── __init__.py
│   │   ├── config.py           # Env vars & settings
│   │   ├── auth.py             # JWT/OIDC Logic
│   │   └── logging.py          # Structlog config
│   ├── db/                     # Database
│   │   ├── __init__.py
│   │   ├── session.py          # SQLAlchemy SessionLocal
│   │   └── models.py           # Tables: Client, Portfolio, Audit, etc.
│   ├── services/               # Business Logic
│   │   ├── __init__.py
│   │   ├── portfolio_service.py
│   │   ├── risk_service.py
│   │   ├── compliance_service.py
│   │   └── ai/
│   │       ├── orchestrator.py # LLM Tool calling logic
│   │       └── rag.py          # Document retrieval
│   └── workers/                # Celery Background Tasks
│       ├── celery_app.py
│       └── tasks.py
├── ui/
│   ├── streamlit_app.py        # Main Streamlit Dashboard
│   └── components/             # Reusable UI widgets
├── tests/
│   ├── conftest.py
│   └── ...
├── requirements.txt
└── README.md
```

## 2. Core Modules Specification

### `app/db/models.py`
* **Tables**: `Client`, `Portfolio`, `Position`, `Instrument`, `Interaction`, `Alert`, `Recommendation`, `SuitabilityCheck`, `AuditLog`.
* **Details**: 
    * `AuditLog` is append-only.
    * `Recommendation` stores JSON drafts.

### `app/api/routes_ai.py`
* **POST /ai/insights**: Triggers RAG pipeline.
* **POST /ai/recommendations**: Async job submission for drift analysis.
* **GET /ai/stream**: SSE endpoint for streaming LLM tokens.

### `app/services/ai/orchestrator.py`
* **Tools**:
    * `get_client_data(id)`
    * `get_house_view(query)`
    * `check_compliance(draft)`
* **Logic**: Uses OpenAI/Anthropic/Gemini API to generate `RecommendationDraft` object (Pydantic).

### `ui/streamlit_app.py`
* **Tabs/Pages**:
    1. **Command Center**: Priority list sorted by `priority_score`.
    2. **Client 360**: Charts (Plotly) for Risk/Portfolio.
    3. **Recommendation**: Review draft, run compliance check, approve.

## 3. Database Schema (Schema Outline)

* **clients**: `id` (PK), `name`, `risk_profile`, `rm_id`.
* **portfolios**: `id` (PK), `client_id` (FK).
* **positions**: `id`, `portfolio_id` (FK), `instrument_id`, `quantity`, `mv_local`.
* **recommendations**: `id`, `client_id`, `status` (DRAFT/APPROVED/REJECTED), `content_json`.
* **audit_logs**: `id`, `entity_type`, `entity_id`, `action`, `user_id`, `timestamp`, `details_json`.

## 4. MVP Phase 1 (Next Step)
1. Define `app/db/models.py` with SQLAlchemy.
2. Setup `app/main.py` and `app/db/session.py`.
3. Create `ui/streamlit_app.py` to connect to a mock API or direct DB for testing.
