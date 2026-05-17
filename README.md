# 🤖 IBM Bob Onboarding Accelerator

> Understand any GitHub repository in under 5 minutes using IBM Bob AI

Built for the IBM Bob Hackathon, this tool eliminates the 2-5 day onboarding time for new developers by automatically analyzing codebases and generating comprehensive documentation.

## 🚀 Live Demo

- **Frontend**: Deployed on Vercel
- **Backend**: Deploy on Render

## ✨ Features

- 🏗️ **Architecture Diagrams** - Visual Mermaid diagrams showing system structure
- 🔄 **Key Flows** - Identification of the 3 most important system flows
- 📚 **Onboarding Guide** - Complete markdown guide with setup instructions
- ⚡ **Fast Analysis** - Results in 30-60 seconds
- 🎨 **Beautiful UI** - Modern, responsive interface built with React + Tailwind

## 📋 Quick Deploy to Render

### Option 1: Using Render Dashboard

1. **Fork this repository** to your GitHub account

2. **Go to [Render Dashboard](https://dashboard.render.com/)**

3. **Click "New +" → "Web Service"**

4. **Connect your GitHub repository**

5. **Configure the service:**
   - **Name**: `bob-onboarding-backend`
   - **Environment**: `Python 3`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements-prod.txt`
   - **Start Command**: `cd bob-onboarding/backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

6. **Add Environment Variables:**
   - `BOB_API_ENDPOINT`: Your IBM Bob API endpoint
   - `BOB_API_KEY`: Your IBM Bob API key

7. **Click "Create Web Service"**

### Option 2: Using render.yaml (Blueprint)

1. **Fork this repository**

2. **Go to [Render Dashboard](https://dashboard.render.com/)**

3. **Click "New +" → "Blueprint"**

4. **Connect your repository**

5. **Render will automatically detect `render.yaml` and configure everything**

6. **Add your environment variables when prompted:**
   - `BOB_API_ENDPOINT`
   - `BOB_API_KEY`

## 🔧 Environment Variables

You need to set these environment variables in Render:

```
BOB_API_ENDPOINT=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
BOB_API_KEY=your_actual_api_key_here
```

### How to get IBM Bob API credentials:

1. Go to [IBM Cloud Console](https://cloud.ibm.com)
2. Navigate to your watsonx.ai instance
3. Go to "Credentials" or "Service credentials"
4. Copy the API endpoint URL and API key

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

## 📖 Local Development

See the [bob-onboarding/README.md](bob-onboarding/README.md) for detailed local development instructions.

## 🏗️ Project Structure

```
.
├── bob-onboarding/          # Main application
│   ├── backend/            # FastAPI backend
│   └── frontend/           # React frontend
├── requirements.txt        # Python dependencies (root for Render)
├── Procfile               # Render/Heroku process file
├── runtime.txt            # Python version specification
└── render.yaml            # Render blueprint configuration
```

## 🐛 Troubleshooting Render Deployment

### Build fails with "requirements.txt not found"
✅ **Fixed!** The `requirements.txt` is now in the root directory.

### Environment variables not set
1. Go to your service in Render Dashboard
2. Click "Environment" tab
3. Add `BOB_API_ENDPOINT` and `BOB_API_KEY`
4. Click "Save Changes"

### Service won't start
- Check the logs in Render Dashboard
- Verify your start command is correct
- Ensure all environment variables are set

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ❤️ for the IBM Bob Hackathon**