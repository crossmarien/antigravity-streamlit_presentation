# AI Private Banking Advisory Dashboard

## 0) Target Outcome
Build a **web dashboard** for PBs where AI automates:
* client prioritization (who to contact today)
* portfolio/risk insights (explainable)
* recommendation drafting (compliance-checked)
* interaction logging + audit trail

Primary KPI: **reduce per-client prep time from ~45–60 min to ~10–15 min**.

## 1) Technology Stack (Python-Only)
* **Web UI**: Streamlit (MVP), potentially Plotly Dash or NiceGUI later.
* **Backend API**: FastAPI + Uvicorn + Pydantic.
* **Async Jobs**: Celery + Redis.
* **Storage**: PostgreSQL (OLTP), Redis (Cache), OpenSearch/pgvector (Search).
* **Observability**: OpenTelemetry, structlog, Prometheus.

## 2) Architecture
* **API Gateway**: FastAPI (Auth, RBAC).
* **Services**: Portfolio, Risk, AI, Compliance, Audit.
* **Data Flow**: Ingest -> Compute -> AI Gen -> Compliance -> Review -> Audit.

## 3) Repository Layout
```
ai_pb_dashboard/
  app/
    main.py                 # FastAPI entry
    api/
    core/
    db/
    services/
    workers/
  ui/
    streamlit_app.py
  tests/
```
