# Repo Accelerate quick test

1. Set `GEMINI_API_KEY` in `backend/.env`.
2. Start the API with:

   ```powershell
   python -m uvicorn backend.main:app --reload --port 8000
   ```

3. Start the frontend:

   ```powershell
   cd frontend
   npm run dev
   ```

4. Open `http://localhost:5173`.
5. Switch between EN and ES and confirm the interface changes immediately.
6. Analyze a small public GitHub repository.
7. Confirm that Architecture, Key flows, and Onboarding guide are available as tabs.
8. Test Mermaid zoom, fit, source view, and SVG download.
9. Switch language after analysis and confirm the existing result remains visible with a regeneration action.
