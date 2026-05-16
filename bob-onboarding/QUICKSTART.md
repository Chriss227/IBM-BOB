# 🚀 Quick Start Guide

Get Bob Onboarding Accelerator running in 5 minutes!

## Prerequisites Check

Before starting, verify you have:

```bash
# Check Python version (need 3.11+)
python --version

# Check Node.js version (need 18+)
node --version

# Check Git
git --version
```

## Step-by-Step Setup

### 1️⃣ Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your IBM Bob credentials
# You need:
# - BOB_API_ENDPOINT (e.g., https://api.ibm.com/bob/v1/chat)
# - BOB_API_KEY (your API key)
```

### 2️⃣ Install Backend Dependencies

```bash
# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3️⃣ Install Frontend Dependencies

```bash
# In a new terminal
cd frontend
npm install
```

### 4️⃣ Start Backend Server

```bash
# Terminal 1 (from project root)
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 5️⃣ Start Frontend Server

```bash
# Terminal 2 (from project root)
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 6️⃣ Test the Application

1. Open http://localhost:5173 in your browser
2. Enter a test repository: `https://github.com/tiangolo/fastapi`
3. Click "Analyze with Bob"
4. Wait 30-60 seconds for results

## 🎯 What to Expect

**During Analysis:**
- Loading indicator with progress steps
- "Bob is reading the repository..." message

**After Analysis:**
- ✅ Success banner with file count
- 🏗️ Architecture diagram (Mermaid visualization)
- 🔄 Key system flows (3 cards with steps)
- 📚 Onboarding guide (markdown with sections)

## 🐛 Common Issues

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`
- **Fix:** Make sure virtual environment is activated and dependencies are installed

**Error:** `BOB_API_ENDPOINT environment variable is not set`
- **Fix:** Create `.env` file in project root with your credentials

### Frontend won't start

**Error:** `Cannot find module 'react'`
- **Fix:** Run `npm install` in the frontend directory

**Error:** `Port 5173 is already in use`
- **Fix:** Kill the process using port 5173 or change port in `vite.config.js`

### Analysis fails

**Error:** `Cannot connect to backend server`
- **Fix:** Ensure backend is running on port 8000

**Error:** `Failed to get response from Bob`
- **Fix:** Verify your Bob API credentials are correct

## 📝 Test Repositories

Try these repositories for testing:

- **FastAPI** (Python): `https://github.com/tiangolo/fastapi`
- **Flask** (Python): `https://github.com/pallets/flask`
- **Express** (Node.js): `https://github.com/expressjs/express`
- **React** (JavaScript): `https://github.com/facebook/react`

## 🎓 Next Steps

Once everything is working:

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the codebase structure
3. Try analyzing your own repositories
4. Customize the prompts in `backend/prompt_templates.py`
5. Adjust the UI in `frontend/src/components/`

## 💡 Pro Tips

- **Faster Analysis:** Smaller repositories analyze faster
- **Better Results:** Well-documented repos get better guides
- **Copy Guide:** Use the "Copy Guide" button to save results
- **Multiple Analyses:** Click "Analyze Another Repository" to start over

## 🆘 Need Help?

Check the troubleshooting section in [README.md](README.md) or review the error messages in:
- Backend: Terminal running uvicorn
- Frontend: Browser console (F12)

---

**Happy Analyzing! 🚀**