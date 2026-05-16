# 🤖 Bob Onboarding Accelerator

> Understand any GitHub repository in under 5 minutes using IBM Bob AI

Built for the IBM Bob Hackathon, this tool eliminates the 2-5 day onboarding time for new developers by automatically analyzing codebases and generating comprehensive documentation.

## ✨ Features

- 🏗️ **Architecture Diagrams** - Visual Mermaid diagrams showing system structure
- 🔄 **Key Flows** - Identification of the 3 most important system flows
- 📚 **Onboarding Guide** - Complete markdown guide with setup instructions
- ⚡ **Fast Analysis** - Results in 30-60 seconds
- 🎨 **Beautiful UI** - Modern, responsive interface built with React + Tailwind

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- FastAPI
- IBM Bob AI
- GitPython

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Mermaid.js
- React Markdown

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git
- IBM Bob API credentials

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd bob-onboarding
```

### 2. Set Up Backend

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

# Create .env file
cp ../.env.example .env

# Edit .env and add your IBM Bob API credentials
# BOB_API_ENDPOINT=https://api.ibm.com/bob/v1/chat
# BOB_API_KEY=your_api_key_here
```

### 3. Set Up Frontend

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
# Make sure virtual environment is activated
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Open in Browser

Navigate to `http://localhost:5173` and start analyzing repositories!

## 📖 Usage

1. **Enter a GitHub URL** - Paste any public GitHub repository URL (e.g., `https://github.com/tiangolo/fastapi`)
2. **Click "Analyze with Bob"** - Wait 30-60 seconds while Bob analyzes the code
3. **Explore the Results:**
   - View the architecture diagram
   - Read through key system flows
   - Study the onboarding guide
   - Copy the guide for future reference

## 🏗️ Project Structure

```
bob-onboarding/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── repo_reader.py       # Repository cloning and reading
│   ├── bob_client.py        # IBM Bob API client
│   └── prompt_templates.py  # AI prompts for analysis
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── api.js           # Backend API client
│   │   ├── components/      # React components
│   │   │   ├── RepoInput.jsx
│   │   │   ├── ArchDiagram.jsx
│   │   │   ├── FlowCards.jsx
│   │   │   └── GuidePanel.jsx
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Tailwind styles
│   ├── index.html
│   └── vite.config.js
├── requirements.txt         # Python dependencies
├── package.json            # Node dependencies
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the root directory:

```env
BOB_API_ENDPOINT=https://api.ibm.com/bob/v1/chat
BOB_API_KEY=your_api_key_here
```

### Frontend Configuration

The frontend is configured to connect to `http://localhost:8000` by default. To change this, edit `frontend/src/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## 🧪 Testing

### Test Backend

```bash
cd backend

# Test repository reader
python repo_reader.py

# Test Bob client (requires valid API credentials)
python bob_client.py

# Test with a sample repository
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/tiangolo/fastapi"}'
```

### Test Frontend

```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` and test with a repository like:
- `https://github.com/tiangolo/fastapi`
- `https://github.com/pallets/flask`
- `https://github.com/django/django`

## 🐛 Troubleshooting

### Backend Issues

**"BOB_API_ENDPOINT environment variable is not set"**
- Make sure you've created a `.env` file in the root directory
- Verify the file contains `BOB_API_ENDPOINT` and `BOB_API_KEY`

**"Git clone failed"**
- Ensure Git is installed and accessible from command line
- Check that the repository URL is valid and public
- Verify you have internet connectivity

**"Failed to get response from Bob"**
- Verify your Bob API credentials are correct
- Check that the API endpoint is accessible
- Ensure you haven't exceeded rate limits

### Frontend Issues

**"Cannot connect to backend server"**
- Make sure the backend is running on port 8000
- Check that CORS is properly configured
- Verify no firewall is blocking the connection

**"Mermaid diagram not rendering"**
- This is usually due to invalid Mermaid syntax from Bob
- The app will show a friendly error message
- The rest of the analysis will still be available

## 🎯 API Endpoints

### `POST /analyze`

Analyze a GitHub repository.

**Request:**
```json
{
  "url": "https://github.com/username/repository"
}
```

**Response:**
```json
{
  "architecture_mermaid": "graph LR\n  A[Module] --> B[Module]",
  "flows": [
    {
      "name": "Flow Name",
      "description": "What it does",
      "steps": ["Step 1", "Step 2"],
      "files": ["file.py"]
    }
  ],
  "guide": "# Onboarding Guide\n...",
  "repository_url": "https://github.com/username/repository",
  "files_analyzed": 42
}
```

### `GET /health`

Check backend health status.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

## 🚀 Deployment

### Backend Deployment

The backend can be deployed to any platform that supports Python:

- **Heroku**: Use the included `Procfile`
- **AWS Lambda**: Package with Mangum
- **Google Cloud Run**: Use Docker
- **Azure App Service**: Deploy directly

### Frontend Deployment

Build the frontend for production:

```bash
cd frontend
npm run build
```

Deploy the `dist/` folder to:
- **Vercel**: `vercel deploy`
- **Netlify**: Drag and drop `dist/` folder
- **GitHub Pages**: Use `gh-pages` package
- **AWS S3**: Upload to S3 bucket with static hosting

## 🤝 Contributing

This project was built for the IBM Bob Hackathon. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 🙏 Acknowledgments

- **IBM Bob AI** - The AI engine that powers this tool
- **FastAPI** - For the excellent Python web framework
- **React** - For the powerful UI library
- **Mermaid.js** - For beautiful diagram rendering

## 📧 Contact

Built with ❤️ for the IBM Bob Hackathon

---

**Happy Onboarding! 🚀**