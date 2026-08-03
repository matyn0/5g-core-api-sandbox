# 5G Core API Sandbox

Cloud-native sandbox for simulating 5G NEF and NWDAF APIs.

## Goal

This project is a learning portfolio project focused on:

- 5G Standalone Core concepts
- NEF API exposure
- NWDAF analytics
- Python API development
- Docker
- Kubernetes
- Observability

## Requirements

- Python 3.10 or newer
- Git

## Setup

From the repository root, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the application and testing dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

## Run the API

```bash
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Run the Tests

The tests run the FastAPI application in-process, so Uvicorn does not need to be running.

```bash
python -m pytest -v
```

Tests use a separate in-memory SQLite database and do not modify local development data.

## Persistence

Subscriptions are stored in the local SQLite database `5g_core.db` and remain available after the API restarts. SQLAlchemy creates the required database table automatically when FastAPI starts.

The database connection can be changed with the `DATABASE_URL` environment variable. The default value is:

```text
sqlite:///./5g_core.db
```

The local database file is excluded from Git.

## Endpoints

| Method | Path |
| --- | --- |
| `GET` | `/health` |
| `GET` | `/nef/ue` |
| `GET` | `/nef/ue/{ue_id}/status` |
| `POST` | `/nef/subscriptions` |
| `GET` | `/nef/subscriptions` |
| `GET` | `/nef/subscriptions/{subscription_id}` |
| `DELETE` | `/nef/subscriptions/{subscription_id}` |
| `GET` | `/nwdaf/analytics/slice-load` |
| `GET` | `/nwdaf/analytics/slice-load/{slice_id}` |

## Current Limitations

UE and slice analytics data are static simulator fixtures. Database schema migrations are not implemented yet; missing tables are created automatically at startup.
