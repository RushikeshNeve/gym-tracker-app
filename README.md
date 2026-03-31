# Gym Tracker App

This repository now contains the migrated fitness tracker project prepared for deployment, while still preserving the earlier Streamlit-era history already in the repo.

## Current App

The current production-ready app is split into:

- `frontend/`: React + Vite + TypeScript
- `backend/`: FastAPI + SQLAlchemy + Alembic

Current stack:

- Frontend: React, Vite, TypeScript, Tailwind, React Router, TanStack Query
- Backend: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic
- Database: Postgres via Neon
- Photo storage: local disk in development, Vercel Blob in production

## Deployment

This repo is prepared for a two-project Vercel deployment:

- Frontend project from `frontend/`
- Backend project from `backend/`

Useful docs:

- [backend/README.md](backend/README.md)
- [frontend/README.md](frontend/README.md)
- [backend/.env.example](backend/.env.example)
- [frontend/.env.example](frontend/.env.example)

## Local Development

### Backend

1. Create `backend/.env` from [backend/.env.example](backend/.env.example)
2. Set `FITNESS_DATABASE_URL`
3. Run:

```powershell
cd backend
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m alembic upgrade head
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_reference_data
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_demo_data
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### Frontend

1. Create `frontend/.env` from [frontend/.env.example](frontend/.env.example)
2. Run:

```powershell
cd frontend
npm install
npm run dev
```

## Production Notes

- SQLite is no longer used by the migrated app.
- Progress photo metadata is stored in Postgres.
- Progress photo binaries should use Vercel Blob in production.
- Local file storage is only for development mode.

## Legacy Streamlit History

The GitHub repo already contains earlier Streamlit-based fitness tracker history on prior commits and branches. This push preserves that history while adding the migrated React + FastAPI application on top.
