# Repo Accelerate deployment

The existing deployment identifiers and domains are retained to avoid breaking
the live infrastructure.

## Backend on Render

Use the repository `render.yaml` or configure:

- Build: `chmod +x render-build.sh && ./render-build.sh`
- Start: `cd bob-onboarding/backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`

Required environment variable:

```dotenv
GEMINI_API_KEY=your_key
GEMINI_API_KEY_FALLBACK=your_fallback_key
FRONTEND_URL=https://your-vercel-app.vercel.app
```

## Frontend on Vercel

Set the root directory to `bob-onboarding/frontend` and configure:

```dotenv
VITE_API_URL=https://your-render-service.onrender.com
```

Build command: `npm run build`

Output directory: `dist`

## Verification

1. Open the backend `/health` endpoint.
2. Open the frontend in English and Spanish.
3. Analyze a small public repository.
4. Confirm the API response includes the requested `language`.
5. Confirm Mermaid renders and SVG download works.
