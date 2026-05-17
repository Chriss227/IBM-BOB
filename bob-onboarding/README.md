# 🤖 Bob Onboarding Accelerator

> Understand any GitHub repository in under 5 minutes using IBM Bob AI

Built for the IBM Bob Hackathon, this tool eliminates the 2-5 day onboarding time for new developers by automatically analyzing codebases and generating comprehensive documentation.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

## ✨ Features

- 🏗️ **Architecture Diagrams** - Visual Mermaid diagrams showing system structure
- 🔄 **Key Flows** - Identification of the 3 most important system flows
- 📚 **Onboarding Guide** - Complete markdown guide with setup instructions
- ⚡ **Fast Analysis** - Results in 30-60 seconds
- 🎨 **Beautiful UI** - Modern, responsive interface built with React + Tailwind
- 🐛 **Full Debugging Support** - VS Code configurations for Python and React

## 🛠️ Tech Stack

**Backend:**
- Python 3.11 + FastAPI
- IBM Bob AI
- GitPython for repository analysis

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- Mermaid.js for diagrams
- React Markdown

**Deployment:**
- Backend: Render
- Frontend: Vercel

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd bob-onboarding

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r ../requirements.txt
copy .env.example .env  # Add your Bob API credentials
uvicorn main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser!

📖 **Detailed Instructions:** See [DEVELOPMENT.md](DEVELOPMENT.md)

### Production Deployment

**Backend (Render):**
1. Push code to GitHub
2. Connect repository to Render
3. Add environment variables
4. Deploy automatically

**Frontend (Vercel):**
1. Connect repository to Vercel
2. Set `VITE_API_URL` environment variable
3. Deploy automatically

🚀 **Detailed Instructions:** See [DEPLOYMENT.md](DEPLOYMENT.md)

## 📖 Usage

1. **Enter a GitHub URL** - Paste any public repository URL
2. **Click "Analyze with Bob"** - Wait 30-60 seconds
3. **Explore Results:**
   - View architecture diagram
   - Read key system flows
   - Study onboarding guide
   - Copy guide for reference

### Example Repositories to Try

- `https://github.com/tiangolo/fastapi`
- `https://github.com/pallets/flask`
- `https://github.com/django/django`

## 🏗️ Project Structure

```
bob-onboarding/
├── backend/
│   ├── .env.example           # Environment template
│   ├── main.py                # FastAPI application
│   ├── bob_client.py          # IBM Bob AI client
│   ├── repo_reader.py         # Repository analyzer
│   ├── prompt_templates.py    # AI prompts
│   └── tests/                 # Backend tests
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── api.js             # Backend client
│   │   ├── components/        # React components
│   │   └── __tests__/         # Frontend tests
│   ├── vercel.json            # Vercel config
│   └── package.json           # Dependencies
│
├── .vscode/
│   ├── launch.json            # Debug configurations
│   ├── settings.json          # Workspace settings
│   └── extensions.json        # Recommended extensions
│
├── docs/                      # Additional documentation
├── render.yaml                # Render deployment config
├── DEVELOPMENT.md             # Local development guide
├── DEPLOYMENT.md              # Production deployment guide
└── README.md                  # This file
```

## 🐛 Debugging

This project includes complete VS Code debugging configurations:

### Python Backend
- Set breakpoints in `.py` files
- Press `F5` → Select "Python: FastAPI Backend"
- Debug with hot reload enabled

### React Frontend
- Set breakpoints in `.jsx` files
- Press `F5` → Select "Chrome: Frontend"
- Debug in browser with source maps

### Full Stack
- Press `F5` → Select "Full Stack: Backend + Frontend"
- Debug both simultaneously

📖 **More Details:** See [DEVELOPMENT.md](DEVELOPMENT.md#-debugging)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest                    # Run all tests
pytest --cov             # With coverage
pytest -v -s             # Verbose output
```

### Frontend Tests
```bash
cd frontend
npm test                 # Unit tests
npm run test:e2e        # E2E tests
npm run test:coverage   # With coverage
```

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
  "flows": [...],
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

📖 **Full API Documentation:** See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env` from `backend/.env.example`:

```env
BOB_API_ENDPOINT=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
BOB_API_KEY=your_api_key_here
PORT=8000
ENVIRONMENT=development
```

### Frontend Environment Variables

For production deployment, set in Vercel:

```env
VITE_API_URL=https://your-backend.onrender.com
```

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Verify virtual environment is activated
- Check `.env` file exists with valid credentials
- Ensure port 8000 is not in use

**Frontend can't connect:**
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify `VITE_API_URL` in production

**Mermaid diagram not rendering:**
- This is usually due to invalid syntax from Bob
- The app shows a friendly error message
- Other analysis results remain available

📖 **More Solutions:** See [DEVELOPMENT.md](DEVELOPMENT.md#-troubleshooting)

## 📚 Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Complete local development guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - API reference
- **[docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - Testing guide

## 🤝 Contributing

Contributions are welcome! This project was built for the IBM Bob Hackathon.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 🙏 Acknowledgments

- **IBM Bob AI** - The AI engine powering this tool
- **FastAPI** - Excellent Python web framework
- **React** - Powerful UI library
- **Mermaid.js** - Beautiful diagram rendering
- **Render & Vercel** - Easy deployment platforms

## 📧 Contact

Built with ❤️ for the IBM Bob Hackathon

---

## 🎯 What's Next?

- [ ] Add support for private repositories
- [ ] Cache analysis results
- [ ] Support for more diagram types
- [ ] Multi-language support
- [ ] Team collaboration features
- [ ] Integration with Slack/Teams

---

**Happy Onboarding! 🚀**

*Made with Bob*