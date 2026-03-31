# Fitness Tracker Deployment Guide

This repo is prepared for a two-project Vercel deployment:

- `frontend/`: React + Vite web app
- `backend/`: FastAPI API on the Vercel Python runtime

The current structure is already monorepo-friendly, so no folder move is required.

## Stack

- Frontend: React, Vite, TypeScript, Tailwind, React Router, TanStack Query
- Backend: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic
- Database: Postgres via Neon free tier
- Photos: local disk in development, Vercel Blob in production

## 1. Local Development

### Backend

1. Create `backend/.env` from [backend/.env.example](backend/.env.example)
2. Set a local Postgres connection in `FITNESS_DATABASE_URL`
3. From `backend/`, run:

```powershell
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m alembic upgrade head
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_reference_data
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_demo_data
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### Frontend

1. Create `frontend/.env` from [frontend/.env.example](frontend/.env.example)
2. From `frontend/`, run:

```powershell
npm install
npm run dev
```

Frontend local URL: `http://localhost:5173`
Backend local URL: `http://localhost:8000/api/v1`

## 2. Neon Postgres Setup

1. Create a Neon project on the free tier
2. Copy the pooled Postgres connection string
3. Use it as `FITNESS_DATABASE_URL` in the backend Vercel project
4. Recommended runtime setting on Vercel:

```env
FITNESS_USE_NULL_POOL=true
```

## 3. Vercel Blob Setup

1. Create a Blob store in Vercel Storage
2. Copy the `BLOB_READ_WRITE_TOKEN`
3. Add these backend environment variables:

```env
FITNESS_STORAGE_BACKEND=vercel_blob
FITNESS_BLOB_READ_WRITE_TOKEN=your_token
```

In development, leave `FITNESS_STORAGE_BACKEND=local` and uploads will continue using `backend/media/`.

## 4. Deploy The Backend To Vercel

Create a Vercel project with:

- Root Directory: `backend`
- Framework Preset: `Other`

The backend uses:

- [backend/vercel.json](backend/vercel.json)
- [backend/api/index.py](backend/api/index.py)

Required backend environment variables:

```env
FITNESS_APP_ENV=production
FITNESS_DEBUG=false
FITNESS_API_V1_PREFIX=/api/v1
FITNESS_DATABASE_URL=postgresql+psycopg://...
FITNESS_CORS_ORIGINS=["http://localhost:5173","https://your-frontend-project.vercel.app"]
FITNESS_DEFAULT_PROFILE_ID=1
FITNESS_USE_NULL_POOL=true
FITNESS_STORAGE_BACKEND=vercel_blob
FITNESS_BLOB_READ_WRITE_TOKEN=vercel_blob_rw_token
FITNESS_BLOB_API_BASE_URL=https://blob.vercel-storage.com
```

After the backend project is deployed, run migrations from your machine:

```powershell
cd backend
$env:FITNESS_APP_ENV="production"
$env:FITNESS_DEBUG="false"
$env:FITNESS_DATABASE_URL="postgresql+psycopg://..."
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m alembic upgrade head
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_reference_data
```

Optional demo seed:

```powershell
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_demo_data
```

## 5. Deploy The Frontend To Vercel

Create a second Vercel project with:

- Root Directory: `frontend`
- Framework Preset: `Vite`

The frontend uses:

- [frontend/vercel.json](frontend/vercel.json)

Required frontend environment variables:

```env
VITE_API_BASE_URL=https://your-backend-project.vercel.app/api/v1
```

## 6. Production Notes

- The backend no longer needs SQLite.
- The backend no longer needs local file persistence in production.
- Progress photo metadata is stored in Postgres.
- Progress photo binaries should go to Vercel Blob in production.
- For local development, the existing local-disk media flow is still supported.

## 7. Quick Deploy Checklist

1. Push this repo to GitHub
2. Create Neon database
3. Create Vercel Blob store
4. Deploy backend project from `backend/`
5. Add backend env vars
6. Run Alembic migration against Neon
7. Seed reference data
8. Deploy frontend project from `frontend/`
9. Add `VITE_API_BASE_URL`
10. Update backend `FITNESS_CORS_ORIGINS` to include the frontend domain
