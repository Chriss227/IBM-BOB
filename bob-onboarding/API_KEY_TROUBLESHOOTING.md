# 🔧 API Key Troubleshooting Guide

## ⚠️ Current Issue: Invalid API Key

The error message indicates:
```
API key not valid. Please pass a valid API key.
```

## Root Cause

The API key in your `backend/.env` file is **not a valid Google Gemini API key**. The current key appears to be a placeholder or example key.

**Current key in `backend/.env`:**
```
GEMINI_API_KEY=AQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## ✅ Solution: Get a Real API Key

### Step 1: Generate Your API Key

1. **Visit Google AI Studio:**
   - Go to: https://aistudio.google.com/app/apikey
   
2. **Sign in:**
   - Use your Google account
   
3. **Create API Key:**
   - Click **"Create API Key"** button
   - Choose "Create API key in new project" or select existing project
   
4. **Copy Your Key:**
   - Your new key will start with `AQ.` (e.g., `AQ.xxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - Copy the ENTIRE key (it's quite long, around 40-50 characters)

### Step 2: Update Your .env File

**Windows PowerShell:**
```powershell
# Navigate to backend directory
cd bob-onboarding/backend

# Open .env file in notepad
notepad .env
```

**Update line 3:**
```env
# BEFORE (invalid):
GEMINI_API_KEY=AQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# AFTER (your real key):
GEMINI_API_KEY=AQ.your_actual_key_from_google_ai_studio_here
```

**Save and close the file.**

### Step 3: Restart the Backend

```powershell
# Stop the current server (Ctrl+C)
# Then restart:
cd bob-onboarding/backend
uvicorn main:app --reload
```

## 🔍 How to Verify Your API Key

### Test 1: Check Key Format

Your API key should:
- ✅ Start with `AQ.` (new format) or `AIza` (old format)
- ✅ Be 40-50+ characters long
- ✅ Contain only alphanumeric characters, dots, hyphens, and underscores
- ❌ NOT be the example key shown above

### Test 2: Run the Test Script

```powershell
cd bob-onboarding/backend
python gemini_client.py
```

**Expected output if key is valid:**
```
Testing Gemini API client...

Sending test prompt: 'Explain what FastAPI is in one sentence.'

Calling Gemini API (attempt 1/3)...
Gemini API call successful (response length: XXX chars)
✅ Success! Response:
[Gemini's response about FastAPI]
```

**If you see this error:**
```
❌ Error: Invalid API key or authentication error
```
Your key is still invalid. Go back to Step 1.

## 🚨 Common Mistakes

### Mistake 1: Using Example/Placeholder Key
❌ **Wrong:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_API_KEY=AQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

✅ **Correct:**
```env
GEMINI_API_KEY=AQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
(Your actual key from Google AI Studio)

### Mistake 2: Spaces or Line Breaks
❌ **Wrong:**
```env
GEMINI_API_KEY = AQ.xxxxxxxxxx
GEMINI_API_KEY=AQ.xxxxxxxxxx
xxxxxxxxxx
```

✅ **Correct:**
```env
GEMINI_API_KEY=AQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
(No spaces, all on one line)

### Mistake 3: Wrong File Location
Make sure you're editing:
- ✅ `bob-onboarding/backend/.env` (correct)
- ❌ `bob-onboarding/.env` (wrong - this is the root file)

### Mistake 4: Not Restarting Server
After changing the `.env` file, you MUST restart the backend server:
```powershell
# Press Ctrl+C to stop
# Then run again:
uvicorn main:app --reload
```

## 📋 Complete Checklist

- [ ] Visited https://aistudio.google.com/app/apikey
- [ ] Signed in with Google account
- [ ] Created a new API key
- [ ] Copied the ENTIRE key (starts with `AQ.`)
- [ ] Opened `bob-onboarding/backend/.env` file
- [ ] Replaced the placeholder key with real key
- [ ] Saved the file
- [ ] Restarted the backend server
- [ ] Tested with `python gemini_client.py`
- [ ] Verified backend is working

## 🎯 Quick Test Commands

```powershell
# 1. Test the Gemini client directly
cd bob-onboarding/backend
python gemini_client.py

# 2. Start the backend server
uvicorn main:app --reload

# 3. Test the health endpoint (in browser)
# Open: http://localhost:8000/health

# 4. Test the frontend
cd ../frontend
npm run dev
# Open: http://localhost:5173
```

## 💡 Additional Tips

### Free Tier Limits
- Google Gemini API has a free tier
- Limits: 60 requests per minute
- If you hit limits, wait a minute and try again

### API Key Security
- ✅ DO: Keep your API key secret
- ✅ DO: Add `.env` to `.gitignore` (already done)
- ❌ DON'T: Share your API key
- ❌ DON'T: Commit `.env` to Git
- ❌ DON'T: Post your key in screenshots or documentation

### Multiple Environments
If you're deploying to production (Render):
1. Get your API key from Google AI Studio
2. Go to Render Dashboard
3. Select your service
4. Click "Environment" tab
5. Add/update `GEMINI_API_KEY` with your real key
6. Save changes (auto-deploys)

## 🆘 Still Having Issues?

### Error: "GEMINI_API_KEY not set"
**Solution:** The `.env` file doesn't exist or is in the wrong location
```powershell
# Create from example:
cd bob-onboarding/backend
copy .env.example .env
# Then edit .env with your real key
```

### Error: "Module not found: google"
**Solution:** Dependencies not installed
```powershell
pip install -r bob-onboarding/requirements.txt
```

### Error: "Port 8000 already in use"
**Solution:** Another process is using port 8000
```powershell
# Find and kill the process, or use a different port:
uvicorn main:app --reload --port 8001
```

## 📚 Related Documentation

- **`API_KEY_FORMAT_UPDATE.md`** - Information about new API key format
- **`QUICK_TEST_GUIDE.md`** - Complete testing guide
- **`DEPLOYMENT.md`** - Production deployment guide

---

**Remember:** The key in your `.env` file MUST be a real API key from Google AI Studio. The example keys in documentation are just placeholders and will not work!