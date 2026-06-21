# 🚀 Deployment Guide

Complete guide for deploying Repo Accelerate to production using Render (Backend) and Vercel (Frontend).

## 📋 Prerequisites

- GitHub account with your repository
- [Render account](https://render.com/) (free tier available)
- [Vercel account](https://vercel.com/) (free tier available)
- Google Gemini API key

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Your Repository

Ensure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Create Render Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `bob-onboarding` repository

### Step 3: Configure Service

**Basic Settings:**
- **Name:** `bob-onboarding-api` (or your preferred name)
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Root Directory:** `bob-onboarding`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select **Free** tier (or paid for better performance)

### Step 4: Set Environment Variables

In Render dashboard, add these environment variables:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
ENVIRONMENT=production
PYTHON_VERSION=3.11.0
```

⚠️ **Important:** Keep your `GEMINI_API_KEY` secret!

**Get your Gemini API key:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (new keys start with `AQ.`, old keys start with `AIza` - both work)
5. Add it to Render as `GEMINI_API_KEY`

**Note:** Google updated their API key format. New keys use the `AQ.` prefix (e.g., `AQ.Ab8RN6IxkvazkDr16g5K...`), but the system supports both old (`AIza`) and new (`AQ.`) formats.

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will automatically build and deploy
3. Wait for deployment to complete (5-10 minutes)
4. Note your backend URL: `https://bob-onboarding-api.onrender.com`

### Step 6: Test Backend

```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Should return:
# {"status":"ok","version":"1.0.0"}
```

## 🎨 Frontend Deployment (Vercel)

### Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### Step 2: Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Select the repository

### Step 3: Configure Project

**Framework Preset:** Vite

**Root Directory:** `bob-onboarding/frontend`

**Build Settings:**
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`

### Step 4: Set Environment Variables

Add this environment variable in Vercel:

```
VITE_API_URL=https://your-backend-url.onrender.com
```

Replace `your-backend-url` with your actual Render backend URL.

### Step 5: Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy automatically
3. Wait for deployment (2-5 minutes)
4. Your app will be live at: `https://your-app.vercel.app`

### Step 6: Test Frontend

1. Open your Vercel URL in browser
2. Try analyzing a repository
3. Verify it connects to your Render backend

## 🔄 Alternative: Deploy via CLI

### Backend (Render)

Render uses `render.yaml` for configuration:

```bash
# Push your code
git push origin main

# Render will auto-deploy if connected to GitHub
```

### Frontend (Vercel)

```bash
cd bob-onboarding/frontend

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Set environment variable
vercel env add VITE_API_URL production
# Enter your Render backend URL when prompted
```

## 🔐 Security Best Practices

### Environment Variables

✅ **DO:**
- Store API keys in environment variables
- Use different keys for development and production
- Rotate API keys regularly
- Use Render/Vercel's secret management

❌ **DON'T:**
- Commit `.env` files to Git
- Share API keys in code or documentation
- Use development keys in production

### CORS Configuration

Update `backend/main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Your Vercel domain
        "http://localhost:5173",         # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring & Logs

### Render Logs

1. Go to Render Dashboard
2. Select your service
3. Click **"Logs"** tab
4. View real-time logs and errors

### Vercel Logs

1. Go to Vercel Dashboard
2. Select your project
3. Click on a deployment
4. View **"Functions"** and **"Build Logs"**

## 🔄 Continuous Deployment

### Automatic Deployments

Both Render and Vercel support automatic deployments:

**Render:**
- Automatically deploys when you push to `main` branch
- Configure in Settings → Build & Deploy

**Vercel:**
- Automatically deploys on every push
- Preview deployments for pull requests
- Production deployment for `main` branch

### Manual Deployments

**Render:**
```bash
# Trigger manual deploy from dashboard
# Or push to GitHub to trigger auto-deploy
git push origin main
```

**Vercel:**
```bash
cd bob-onboarding/frontend
vercel --prod
```

## 🐛 Troubleshooting

### Backend Issues

**Build fails on Render:**
- Check Python version in `render.yaml`
- Verify all dependencies in `requirements.txt`
- Check build logs for specific errors

**API returns 500 errors:**
- Check environment variables are set correctly
- View logs in Render dashboard
- Verify Gemini API key is valid
- Check API quota at [Google Cloud Console](https://console.cloud.google.com/)

**Slow cold starts:**
- Free tier services sleep after inactivity
- Upgrade to paid tier for always-on service
- Or use a cron job to keep service warm

### Frontend Issues

**Build fails on Vercel:**
- Check Node.js version compatibility
- Verify all dependencies in `package.json`
- Check build logs for errors

**Cannot connect to backend:**
- Verify `VITE_API_URL` environment variable
- Check CORS settings in backend
- Ensure backend is running (not sleeping)

**Environment variables not working:**
- Vercel requires `VITE_` prefix for client-side variables
- Redeploy after adding environment variables
- Clear cache and redeploy if needed

## 📈 Performance Optimization

### Backend (Render)

1. **Upgrade Instance Type:**
   - Free tier: 512 MB RAM, shared CPU
   - Starter: 1 GB RAM, dedicated CPU
   - Standard: 2 GB RAM, faster

2. **Enable Caching:**
   - Cache repository clones
   - Cache Google Gemini responses (if appropriate)

3. **Add Health Checks:**
   - Already configured in `render.yaml`
   - Monitors `/health` endpoint

### Frontend (Vercel)

1. **Enable Edge Network:**
   - Automatic with Vercel
   - CDN for static assets

2. **Optimize Build:**
   - Already using Vite for fast builds
   - Tree-shaking enabled by default

3. **Add Analytics:**
   - Enable Vercel Analytics in dashboard
   - Monitor performance metrics

## 💰 Cost Estimation

### Free Tier Limits

**Render (Free):**
- 750 hours/month
- Service sleeps after 15 min inactivity
- 512 MB RAM
- Shared CPU

**Vercel (Free):**
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic SSL
- Edge network included

### Paid Tiers

**Render Starter ($7/month):**
- Always-on service
- 1 GB RAM
- Dedicated CPU

**Vercel Pro ($20/month):**
- 1 TB bandwidth
- Advanced analytics
- Team collaboration

## 🔄 Updating Your Deployment

### Update Backend

```bash
# Make changes to backend code
git add backend/
git commit -m "Update backend with Gemini"
git push origin main

# Render auto-deploys
```

### Update Frontend

```bash
# Make changes to frontend code
git add frontend/
git commit -m "Update frontend"
git push origin main

# Vercel auto-deploys
```

### Update Environment Variables

**Render:**
1. Dashboard → Service → Environment
2. Update `GEMINI_API_KEY` if needed
3. Click "Save Changes"
4. Service will restart automatically

**Vercel:**
1. Dashboard → Project → Settings → Environment Variables
2. Update variables
3. Redeploy for changes to take effect

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

## 🆘 Getting Help

If you encounter deployment issues:

1. Check service logs (Render/Vercel dashboards)
2. Verify environment variables are set correctly
3. Test locally first with production settings
4. Check Render/Vercel status pages
5. Contact support if needed

---

🎉 **Congratulations!** Your app is now live in production!

**Backend:** `https://your-app.onrender.com`  
**Frontend:** `https://your-app.vercel.app`