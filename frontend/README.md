# Frontend Deployment

## Local

```powershell
copy .env.example .env
npm install
npm run dev
```

Default local API target:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Vercel

- Project root: `frontend`
- Framework preset: `Vite`
- Config: [vercel.json](vercel.json)

### Required env var

```env
VITE_API_BASE_URL=https://your-backend-project.vercel.app/api/v1
```

### Notes

- React Router SPA navigation is handled by the rewrite in [vercel.json](vercel.json)
- If `VITE_API_BASE_URL` is omitted in development, the app falls back to `http://localhost:8000/api/v1`
