# Project Status

Last updated: 2026-08-03

## Purpose

Local-first FastAPI sandbox for learning and simulating 5G NEF and NWDAF APIs.

## Current State

- Current branch: `main`
- Latest milestone: SQLite subscription persistence
- Automated tests: 13 passing
- API framework: FastAPI
- Database: SQLite with SQLAlchemy
- Database file: `5g_core.db`, excluded from Git
- Subscription data survives API restarts
- Tests use a separate in-memory SQLite database

## Completed Work

- Added NEF UE endpoints
- Added NEF subscription CRUD endpoints
- Added NWDAF slice-load analytics endpoints
- Added 13 automated API tests
- Fixed subscription ID overwriting
- Added SQLite persistence
- Added automatic database table creation
- Added isolated database testing
- Documented setup, testing, endpoints, and persistence

## Current Endpoints

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

## Verification

```bash
python -m pytest -v
sqlite3 -readonly 5g_core.db "PRAGMA integrity_check;"
```

Expected:

```text
13 passed
ok
```

## Current Limitations

- UE and slice analytics data remain static fixtures
- Database migrations are not implemented
- Docker support is not implemented
- CI/CD is not configured
- No authentication or authorization exists

## Next Milestone

Add Docker and Docker Compose support for running the FastAPI application consistently across devices.

## Next Exact Action

Plan the container structure, database volume, environment variables, and health check before creating Docker files.

## Device Notes

The current Mac uses `app/.venv`. A clean clone should follow the README and create `.venv` in the repository root.

## Resume on Another Device

```bash
git pull --ff-only
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

Read this file before beginning new work.

## End-of-Session Checklist

1. Run all tests.
2. Update this report.
3. Review `git status` and `git diff`.
4. Commit the code and report together.
5. Push the commit to GitHub.
6. Confirm the working tree is clean.
