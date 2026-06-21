# Repo Accelerate testing guide

## Frontend

```powershell
cd frontend
npm test -- --run
npm run build
```

The Vitest suite covers:

- API language payloads and errors
- Interface language switching and persistence
- Tabbed result navigation
- Language mismatch regeneration
- Mermaid parsing, rendering, zoom, source view, and invalid syntax

## Backend

```powershell
python -m pytest backend/tests
```

The backend suite covers:

- English defaults and Spanish propagation
- Localized prompts and fallback flows
- Mermaid and JSON fence cleanup
- Request validation and service errors
- Repository reading and Gemini client behavior

## Browser QA

Verify desktop and mobile layouts, keyboard tab navigation, language switching,
Mermaid controls, and the absence of console errors.
