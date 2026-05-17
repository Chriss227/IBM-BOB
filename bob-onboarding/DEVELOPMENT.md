# 🛠️ Development Guide

Complete guide for setting up and developing the Bob Onboarding Accelerator locally.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **VS Code** (recommended) - [Download](https://code.visualstudio.com/)

## 🚀 Initial Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd IBM-BOB/bob-onboarding
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Copy environment template
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env and add your IBM Bob API credentials
# BOB_API_ENDPOINT=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
# BOB_API_KEY=your_actual_api_key_here
```

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install
```

## 🏃 Running the Application

### Option 1: Run Separately (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
# Activate venv if not already active
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Run with hot reload
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open your browser at `http://localhost:5173`

### Option 2: Use VS Code Debugging (Best Experience)

1. Open the project in VS Code
2. Install recommended extensions (VS Code will prompt you)
3. Press `F5` or go to Run & Debug panel
4. Select **"Full Stack: Backend + Frontend"**
5. This will start both backend and frontend with debugging enabled

## 🐛 Debugging

### Python Backend Debugging

**Using VS Code:**
1. Set breakpoints in Python files by clicking left of line numbers
2. Press `F5` and select **"Python: FastAPI Backend"**
3. Make API requests - execution will pause at breakpoints
4. Use Debug Console to inspect variables

**Available Debug Configurations:**
- **Python: FastAPI Backend** - Debug the main API server
- **Python: Current File** - Debug any Python file
- **Python: Backend Tests** - Debug pytest tests

### React Frontend Debugging

**Using VS Code:**
1. Set breakpoints in `.jsx` files
2. Press `F5` and select **"Chrome: Frontend"** or **"Edge: Frontend"**
3. Browser will open with debugging enabled
4. Interact with the app - execution pauses at breakpoints

**Browser DevTools:**
- Press `F12` in browser
- Go to Sources tab
- Find your files under `webpack://` or `src/`
- Set breakpoints and inspect state

## 🧪 Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v -s
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## 📁 Project Structure

```
bob-onboarding/
├── backend/
│   ├── .env                    # Environment variables (create from .env.example)
│   ├── .env.example           # Template for environment variables
│   ├── main.py                # FastAPI application entry point
│   ├── bob_client.py          # IBM Bob AI client
│   ├── repo_reader.py         # GitHub repository reader
│   ├── prompt_templates.py    # AI prompt templates
│   └── tests/                 # Backend tests
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── api.js            # Backend API client
│   │   ├── components/       # React components
│   │   └── __tests__/        # Frontend tests
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
│
├── .vscode/
│   ├── launch.json           # Debug configurations
│   ├── settings.json         # Workspace settings
│   └── extensions.json       # Recommended extensions
│
├── docs/                      # Documentation
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview
```

## 🔧 Common Development Tasks

### Adding a New API Endpoint

1. Add endpoint in `backend/main.py`:
```python
@app.get("/my-endpoint")
async def my_endpoint():
    return {"message": "Hello"}
```

2. Add client function in `frontend/src/api.js`:
```javascript
export async function myEndpoint() {
  const response = await fetch(`${API_BASE_URL}/my-endpoint`);
  return await response.json();
}
```

3. Use in React component:
```javascript
import { myEndpoint } from './api';

const data = await myEndpoint();
```

### Adding a New React Component

1. Create file in `frontend/src/components/MyComponent.jsx`
2. Import and use in `App.jsx` or other components
3. Add tests in `frontend/src/__tests__/MyComponent.test.jsx`

### Updating Dependencies

**Backend:**
```bash
pip install <package>
pip freeze > requirements.txt
```

**Frontend:**
```bash
npm install <package>
# package.json is automatically updated
```

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
# Make sure virtual environment is activated
cd backend
venv\Scripts\activate  # Windows
pip install -r ../requirements.txt
```

**"BOB_API_ENDPOINT not set":**
- Check that `backend/.env` file exists
- Verify it contains `BOB_API_ENDPOINT` and `BOB_API_KEY`
- Restart the backend server

**Port 8000 already in use:**
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**"Cannot connect to backend":**
- Ensure backend is running on port 8000
- Check `frontend/src/api.js` has correct `API_BASE_URL`
- Verify CORS is enabled in backend

**npm install fails:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Hot reload not working:**
```bash
# Restart Vite dev server
npm run dev
```

## 💡 Tips & Best Practices

### Python Development

- Always activate virtual environment before working
- Use type hints for better IDE support
- Run `pytest` before committing changes
- Use `black` for code formatting: `black .`

### React Development

- Use React DevTools browser extension
- Keep components small and focused
- Use `console.log()` for quick debugging
- Run `npm run lint` before committing

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "Add my feature"

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [IBM Bob AI Documentation](https://www.ibm.com/docs/bob)
- [VS Code Python Debugging](https://code.visualstudio.com/docs/python/debugging)
- [VS Code JavaScript Debugging](https://code.visualstudio.com/docs/nodejs/browser-debugging)

## 🆘 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review error messages carefully
3. Check the logs in terminal/console
4. Search for similar issues on GitHub
5. Ask for help in team chat

---

Happy coding! 🚀