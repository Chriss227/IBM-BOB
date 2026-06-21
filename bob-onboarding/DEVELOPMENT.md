# Repo Accelerate development guide

## Requirements

- Python 3.11+
- Node.js 18+
- Git
- A Google Gemini API key

## Backend

From `bob-onboarding/`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item backend\.env.example backend\.env
```

Configure:

```dotenv
GEMINI_API_KEY=your_key
```

Run:

```powershell
python -m uvicorn backend.main:app --reload --port 8000
```

API documentation is available at `http://127.0.0.1:8000/docs`.

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

The frontend reads `VITE_API_URL`; local development can use:

```dotenv
VITE_API_URL=http://127.0.0.1:8000
```

## Internationalization

Interface translations are defined in `frontend/src/i18n.js`. The selected
language is persisted under `repoAccelerateLanguage` and is sent to
`POST /analyze`. Backend prompts preserve commands, paths, and identifiers while
generating explanatory content in the requested language.

## Tests

```powershell
cd frontend
npm test -- --run
npm run build
```

```powershell
python -m pytest backend/tests
```
