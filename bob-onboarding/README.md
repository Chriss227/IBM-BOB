# Repo Accelerate

Repo Accelerate analyzes a public GitHub repository and returns:

- A Mermaid architecture map
- Three important system flows
- A practical developer onboarding guide
- English or Spanish output selected from the interface

The application uses React, Vite, Tailwind CSS, FastAPI, and Google Gemini.

## Local development

### Backend

```powershell
cd bob-onboarding
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item backend\.env.example backend\.env
```

Set the Gemini credential in `backend/.env`:

```dotenv
GEMINI_API_KEY=your_key
```

Start the API:

```powershell
python -m uvicorn backend.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API

`POST /analyze`

```json
{
  "url": "https://github.com/owner/repository",
  "language": "es"
}
```

`language` accepts `en` or `es` and defaults to `en`.

## Quality checks

```powershell
cd frontend
npm test -- --run
npm run build
```

```powershell
python -m pytest backend/tests
```

See [DEVELOPMENT.md](DEVELOPMENT.md), [DEPLOYMENT.md](DEPLOYMENT.md), and
[docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for operational details.
