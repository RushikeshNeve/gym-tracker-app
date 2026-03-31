# Backend Deployment

## Local

```powershell
copy .env.example .env
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m alembic upgrade head
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_reference_data
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

## Vercel

- Project root: `backend`
- Entrypoint: [api/index.py](api/index.py)
- Config: [vercel.json](vercel.json)

### Required env vars

```env
FITNESS_APP_ENV=production
FITNESS_DEBUG=false
FITNESS_API_V1_PREFIX=/api/v1
FITNESS_DATABASE_URL=postgresql+psycopg://...
FITNESS_CORS_ORIGINS=["https://your-frontend-project.vercel.app"]
FITNESS_USE_NULL_POOL=true
FITNESS_STORAGE_BACKEND=vercel_blob
FITNESS_BLOB_READ_WRITE_TOKEN=vercel_blob_rw_token
FITNESS_BLOB_API_BASE_URL=https://blob.vercel-storage.com
```

### Migrations

Run Alembic against the same production `FITNESS_DATABASE_URL` from your machine or CI:

```powershell
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m alembic upgrade head
```

### Seeding

Reference data:

```powershell
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_reference_data
```

Optional demo data:

```powershell
c:\Rushikesh\Tech\Projects\DailyUse\.venv\Scripts\python.exe -m app.seeds.seed_demo_data
```
