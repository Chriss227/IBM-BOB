# 🧪 Quick Test Guide - Gemini API Key Format

## Prerequisites

You need a valid Gemini API key. Get one here: https://aistudio.google.com/app/apikey

## Test 1: Verify API Key Format

Your API key should start with one of these:
- ✅ `AQ.` (new format) - Example: `AQ.Ab8RN6IxkvazkDr16g5K...`
- ✅ `AIza` (old format) - Example: `AIzaSyDxxxxxxxxx...`

## Test 2: Update Environment Variables

### Option A: Local Testing

1. Open `bob-onboarding/backend/.env`
2. Update the line:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Replace `your_actual_api_key_here` with your real API key

### Option B: Production (Render)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your service
3. Click **Environment** tab
4. Find `GEMINI_API_KEY`
5. Update with your new API key
6. Click **Save Changes**

## Test 3: Run the Backend

### Windows (PowerShell):
```powershell
cd bob-onboarding/backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
python gemini_client.py
```

### Expected Output:
```
Testing Gemini API client...

Sending test prompt: 'Explain what FastAPI is in one sentence.'

Calling Gemini API (attempt 1/3)...
Gemini API call successful (response length: XXX chars)
✅ Success! Response:
[Response from Gemini]
```

### If You See Warnings:
```
⚠️  Warning: API key doesn't match expected format
   Expected: Starts with 'AQ.' (new) or 'AIza' (old)
   Got: Starts with 'xxxx'
```
This means your API key format is unexpected. Double-check you copied it correctly.

## Test 4: Run Full Backend Server

```powershell
cd bob-onboarding/backend
uvicorn main:app --reload
```

### Test the Health Endpoint:
Open browser: http://localhost:8000/health

Expected response:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### Test the Analyze Endpoint:
Use the frontend or curl:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/tiangolo/fastapi"}'
```

## Test 5: Run Frontend

```powershell
cd bob-onboarding/frontend
npm install
npm run dev
```

Open: http://localhost:5173

Try analyzing a repository!

## Common Issues & Solutions

### Issue: "GEMINI_API_KEY not set"
**Solution:** 
- Check `.env` file exists in `bob-onboarding/backend/`
- Verify the key is set: `GEMINI_API_KEY=AQ.your_key_here`
- No spaces around the `=` sign

### Issue: "Invalid API key or authentication error"
**Solution:**
- Verify your API key is correct
- Generate a new key at https://aistudio.google.com/app/apikey
- Make sure you copied the entire key (no line breaks)

### Issue: "Module not found: google"
**Solution:**
```powershell
pip install google-genai>=2.8.0
```

### Issue: Backend starts but frontend can't connect
**Solution:**
- Verify backend is running on port 8000
- Check `frontend/.env` has: `VITE_API_URL=http://127.0.0.1:8000`
- Check CORS settings in `backend/main.py`

## Verification Checklist

- [ ] API key obtained from Google AI Studio
- [ ] API key starts with `AQ.` or `AIza`
- [ ] `.env` file updated with real API key
- [ ] Backend dependencies installed
- [ ] `python gemini_client.py` runs successfully
- [ ] Backend server starts without errors
- [ ] Health endpoint returns `{"status": "ok"}`
- [ ] Frontend connects to backend
- [ ] Can analyze a test repository

## Success Criteria

✅ **System is working if:**
1. Backend starts without errors
2. Health endpoint responds
3. Can analyze a GitHub repository
4. Results display in frontend (architecture, flows, guide)

## Need Help?

1. Check `API_KEY_FORMAT_UPDATE.md` for detailed information
2. Review `DEPLOYMENT.md` for production setup
3. See `DEVELOPMENT.md` for local development guide
4. Check backend logs for specific error messages

---

**Last Updated:** 2026-06-18  
**Status:** Ready for testing with both old and new API key formats