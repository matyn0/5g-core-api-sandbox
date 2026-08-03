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

Subscriptions are stored in memory and disappear when the API process restarts.
