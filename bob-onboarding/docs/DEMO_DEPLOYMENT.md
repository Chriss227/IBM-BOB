# 🚀 Demo Platform Deployment Guide

Complete guide for deploying the Bob Onboarding Accelerator Demo Platform to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Build Process](#build-process)
3. [Deployment Options](#deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Post-Deployment](#post-deployment)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools
- Node.js 18+ and npm
- Git
- Account on chosen hosting platform (Vercel/Netlify/AWS)

### Required Information
- Backend API URL (production endpoint)
- GitHub repository URL
- Domain name (optional)

## Build Process

### 1. Prepare the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run tests
npm test

# Build for production
npm run build
```

This creates an optimized production build in the `dist/` directory.

### 2. Verify Build

```bash
# Preview the production build locally
npm run preview
```

Visit `http://localhost:4173` to verify the build works correctly.

### 3. Build Optimization Checklist

- [ ] All routes load correctly (`/` and `/demo`)
- [ ] Navigation works between pages
- [ ] Sample repository links function
- [ ] Images and assets load
- [ ] No console errors
- [ ] Mobile responsive design works

## Deployment Options

### Option 1: Vercel (Recommended)

**Pros**: Automatic deployments, edge network, free SSL, excellent DX

#### Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? bob-onboarding-demo
# - Directory? ./
# - Override settings? No
```

#### Via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your Git repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add environment variables (see below)
6. Click "Deploy"

#### Vercel Configuration File

Create `frontend/vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Option 2: Netlify

**Pros**: Similar to Vercel, great for static sites, form handling

#### Via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod

# Follow prompts:
# - Create new site? Yes
# - Site name? bob-onboarding-demo
# - Publish directory? dist
```

#### Via Netlify Dashboard

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect to Git provider
4. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
5. Add environment variables
6. Click "Deploy site"

#### Netlify Configuration File

Create `frontend/netlify.toml`:

```toml
[build]
  base = "frontend"
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Option 3: AWS S3 + CloudFront

**Pros**: Full control, scalable, cost-effective for high traffic

#### Step 1: Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://bob-onboarding-demo

# Enable static website hosting
aws s3 website s3://bob-onboarding-demo \
  --index-document index.html \
  --error-document index.html
```

#### Step 2: Upload Build

```bash
# Build the project
cd frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://bob-onboarding-demo \
  --delete \
  --cache-control "public, max-age=31536000"

# Upload index.html with no-cache
aws s3 cp dist/index.html s3://bob-onboarding-demo/index.html \
  --cache-control "no-cache"
```

#### Step 3: Configure CloudFront

1. Create CloudFront distribution
2. Set origin to S3 bucket
3. Configure custom error responses:
   - 403 → /index.html (200)
   - 404 → /index.html (200)
4. Enable HTTPS
5. Add custom domain (optional)

#### Deployment Script

Create `scripts/deploy-aws.sh`:

```bash
#!/bin/bash
set -e

echo "Building frontend..."
cd frontend
npm run build

echo "Uploading to S3..."
aws s3 sync dist/ s3://bob-onboarding-demo \
  --delete \
  --cache-control "public, max-age=31536000"

aws s3 cp dist/index.html s3://bob-onboarding-demo/index.html \
  --cache-control "no-cache"

echo "Invalidating CloudFront cache..."
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"

echo "Deployment complete!"
```

### Option 4: GitHub Pages

**Pros**: Free, integrated with GitHub, simple setup

#### Configuration

1. Create `frontend/.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        working-directory: ./frontend
        run: npm install
        
      - name: Build
        working-directory: ./frontend
        run: npm run build
        
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/dist
```

2. Enable GitHub Pages in repository settings
3. Set source to `gh-pages` branch

## Environment Configuration

### Frontend Environment Variables

Create `.env.production` in the frontend directory:

```env
# Backend API URL (production)
VITE_API_URL=https://api.yourdomain.com

# Analytics (optional)
VITE_GA_ID=G-XXXXXXXXXX

# Feature flags (optional)
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_TRACKING=true
```

### Platform-Specific Configuration

#### Vercel
Add in Vercel dashboard under "Environment Variables":
- `VITE_API_URL` → Your backend URL

#### Netlify
Add in Netlify dashboard under "Site settings" → "Environment variables":
- `VITE_API_URL` → Your backend URL

#### AWS
Set in CloudFront or use AWS Systems Manager Parameter Store

## Post-Deployment

### 1. Verify Deployment

```bash
# Check if site is accessible
curl -I https://your-demo-url.com

# Check specific routes
curl https://your-demo-url.com/
curl https://your-demo-url.com/demo
```

### 2. Test Functionality

- [ ] Homepage loads correctly
- [ ] Demo page loads correctly
- [ ] Navigation works
- [ ] Sample repository links work
- [ ] Analyzer connects to backend
- [ ] Mobile view works
- [ ] All assets load (images, fonts)

### 3. Performance Testing

```bash
# Run Lighthouse audit
npx lighthouse https://your-demo-url.com --view

# Check Core Web Vitals
# - LCP (Largest Contentful Paint) < 2.5s
# - FID (First Input Delay) < 100ms
# - CLS (Cumulative Layout Shift) < 0.1
```

### 4. SEO Configuration

Add to `frontend/index.html`:

```html
<head>
  <!-- Primary Meta Tags -->
  <title>Bob Onboarding Accelerator - Understand Any Repo in 5 Minutes</title>
  <meta name="title" content="Bob Onboarding Accelerator">
  <meta name="description" content="Analyze GitHub repositories in under 5 minutes using IBM Bob AI. Get architecture diagrams, key flows, and onboarding guides instantly.">
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://your-demo-url.com/">
  <meta property="og:title" content="Bob Onboarding Accelerator">
  <meta property="og:description" content="Analyze GitHub repositories in under 5 minutes using IBM Bob AI.">
  <meta property="og:image" content="https://your-demo-url.com/og-image.png">
  
  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="https://your-demo-url.com/">
  <meta property="twitter:title" content="Bob Onboarding Accelerator">
  <meta property="twitter:description" content="Analyze GitHub repositories in under 5 minutes using IBM Bob AI.">
  <meta property="twitter:image" content="https://your-demo-url.com/og-image.png">
</head>
```

### 5. Analytics Setup (Optional)

#### Google Analytics

```javascript
// Add to frontend/index.html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## Monitoring

### 1. Uptime Monitoring

Use services like:
- **UptimeRobot**: Free, checks every 5 minutes
- **Pingdom**: More detailed monitoring
- **StatusCake**: Multiple check locations

### 2. Error Tracking

Integrate Sentry:

```bash
npm install @sentry/react
```

```javascript
// frontend/src/main.jsx
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  environment: "production",
  tracesSampleRate: 1.0,
});
```

### 3. Performance Monitoring

- Use Vercel Analytics (if on Vercel)
- Google PageSpeed Insights
- WebPageTest.org

## Troubleshooting

### Issue: Routes return 404

**Solution**: Configure rewrites/redirects to serve `index.html` for all routes

Vercel:
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

Netlify:
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Issue: Environment variables not working

**Solution**: 
1. Ensure variables are prefixed with `VITE_`
2. Rebuild after adding variables
3. Check platform-specific configuration

### Issue: Assets not loading

**Solution**:
1. Check base URL in `vite.config.js`
2. Verify asset paths are relative
3. Check CORS configuration

### Issue: Slow load times

**Solution**:
1. Enable compression (gzip/brotli)
2. Optimize images
3. Use CDN for assets
4. Enable caching headers

## Continuous Deployment

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Demo Platform

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      
      - name: Run tests
        working-directory: ./frontend
        run: npm test
      
      - name: Build
        working-directory: ./frontend
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
```

## Rollback Procedure

### Vercel
```bash
# List deployments
vercel ls

# Rollback to previous deployment
vercel rollback [deployment-url]
```

### Netlify
```bash
# List deployments
netlify deploy:list

# Restore previous deployment
netlify deploy:restore [deploy-id]
```

### AWS S3
```bash
# Keep backups of previous builds
aws s3 sync s3://bob-onboarding-demo s3://bob-onboarding-demo-backup

# Restore from backup
aws s3 sync s3://bob-onboarding-demo-backup s3://bob-onboarding-demo
```

## Security Checklist

- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] No sensitive data in frontend code
- [ ] API endpoints use authentication
- [ ] CORS properly configured
- [ ] Dependencies updated
- [ ] No exposed API keys

## Maintenance Schedule

### Weekly
- Check uptime status
- Review error logs
- Monitor performance metrics

### Monthly
- Update dependencies
- Review analytics
- Test all functionality
- Update sample repositories

### Quarterly
- Security audit
- Performance optimization
- Content refresh
- User feedback review

---

**Deployment Checklist**

- [ ] Frontend built successfully
- [ ] Environment variables configured
- [ ] Deployment platform chosen
- [ ] Domain configured (if applicable)
- [ ] SSL certificate active
- [ ] All routes working
- [ ] Analytics configured
- [ ] Monitoring set up
- [ ] Documentation updated
- [ ] Team notified

**Need Help?**
- Check [DEMO_PLATFORM.md](./DEMO_PLATFORM.md) for platform details
- Review [README.md](../README.md) for general setup
- Open an issue on GitHub for support

---

**Built with ❤️ for the IBM Bob Hackathon**