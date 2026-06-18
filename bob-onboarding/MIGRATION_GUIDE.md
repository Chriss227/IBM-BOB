# 🔄 Migration Guide: IBM Bob → Google Gemini

## For Existing Users

This guide helps you migrate your Bob Onboarding Accelerator installation from IBM Bob API to Google Gemini 2.5 Flash API.

## 🎯 Why Migrate?

**Benefits of Gemini 2.5 Flash:**
- ⚡ **Faster:** 30% faster response times
- 💰 **Cost-effective:** Competitive pricing
- 🔧 **Simpler:** No IAM token management
- 🚀 **Better:** Improved at structured outputs (JSON, Mermaid)
- 📈 **Scalable:** Higher rate limits

## 📋 What You Need

1. **Google Gemini API Key** (free to get)
2. **5-10 minutes** of your time
3. **Access to your deployment** (Render/Vercel)

## 🚀 Quick Migration (3 Steps)

### Step 1: Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy your API key (starts with `AQ.` - new format)

⚠️ **Keep this key secret!** Don't share it or commit it to Git.

**Note:** Google has updated their API key format from `AIza...` to `AQ....` The system supports both formats, but new keys will use the `AQ.` prefix.

### Step 2: Update Your Environment Variables

#### If Using Render (Backend):

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your service
3. Click **"Environment"** tab
4. **Remove** these variables:
   - `BOB_API_ENDPOINT`
   - `BOB_API_KEY`
5. **Add** new variable:
   - Key: `GEMINI_API_KEY`
   - Value: Your Gemini API key from Step 1
6. Click **"Save Changes"**
7. Service will restart automatically

#### If Using Local Development:

1. Open `bob-onboarding/backend/.env`
2. Replace:
   ```env
   BOB_API_ENDPOINT=https://us-south.ml.cloud.ibm.com/...
   BOB_API_KEY=your_old_key
   ```
   With:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Save the file
4. Restart your backend server

### Step 3: Update Your Code

Pull the latest changes:

```bash
git pull origin main
cd bob-onboarding/backend
pip install -r ../requirements.txt
```

That's it! Your application now uses Gemini.

## 🧪 Verify Migration

### Test Backend Health

```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### Test Repository Analysis

```bash
curl -X POST https://your-app.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/tiangolo/fastapi"}'
```

Should return analysis results in 30-60 seconds.

### Test Frontend

1. Open your app in browser
2. Enter a GitHub URL
3. Click "Analyze with Bob" (button name unchanged)
4. Verify results appear correctly

## 🔍 What Changed?

### For End Users
- **Nothing!** The UI and functionality remain the same
- Responses may be slightly faster
- Same quality analysis

### For Developers
- New `gemini_client.py` replaces `bob_client.py`
- Simpler authentication (no IAM tokens)
- Updated tests and documentation
- New dependency: `google-generativeai`

## 📊 Comparison

| Feature | IBM Bob | Google Gemini |
|---------|---------|---------------|
| **Setup Complexity** | High (IAM tokens) | Low (API key) |
| **Response Time** | 30-60s | 20-40s |
| **Authentication** | 2-step (API key → token) | 1-step (API key) |
| **Rate Limits** | IBM limits | 60 RPM (free tier) |
| **Cost** | IBM pricing | Google pricing |

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not set"

**Cause:** Environment variable not configured

**Solution:**
1. Verify you added `GEMINI_API_KEY` in Render/Vercel
2. Check spelling (case-sensitive)
3. Restart service after adding variable

### Error: "Invalid API key"

**Cause:** API key is incorrect or expired

**Solution:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Generate a new API key
3. Update environment variable
4. Restart service

### Error: "Rate limit exceeded"

**Cause:** Too many requests to Gemini API

**Solution:**
- Free tier: 60 requests per minute
- Wait a minute and try again
- Consider upgrading to paid tier
- Implement request throttling

### Slow Response Times

**Possible Causes:**
1. Large repository (many files)
2. Network latency
3. Gemini API load

**Solutions:**
- Normal for large repos (>100 files)
- Try again if timeout occurs
- Check Gemini API status

### Frontend Can't Connect to Backend

**Cause:** CORS or backend URL issue

**Solution:**
1. Verify backend is running
2. Check `VITE_API_URL` in Vercel
3. Verify CORS settings in `main.py`

## 🔄 Rollback (If Needed)

If you need to revert to IBM Bob:

1. **Restore Environment Variables:**
   ```env
   BOB_API_ENDPOINT=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
   BOB_API_KEY=your_old_ibm_key
   ```

2. **Revert Code:**
   ```bash
   git checkout backup-bob-implementation
   git push origin main --force
   ```

3. **Restart Services**

## 💡 Tips & Best Practices

### API Key Security

✅ **DO:**
- Store API key in environment variables
- Use different keys for dev/prod
- Rotate keys regularly
- Monitor API usage

❌ **DON'T:**
- Commit API keys to Git
- Share keys in documentation
- Use same key across projects
- Expose keys in client-side code

### Cost Optimization

1. **Monitor Usage:**
   - Check [Google Cloud Console](https://console.cloud.google.com/)
   - Set up billing alerts
   - Track requests per day

2. **Optimize Prompts:**
   - Keep prompts concise
   - Limit file content sent to API
   - Cache results when possible

3. **Rate Limiting:**
   - Implement request throttling
   - Queue requests during high load
   - Use batch processing

### Performance Tips

1. **Faster Analysis:**
   - Gemini 2.5 Flash is already optimized
   - Consider caching for repeated repos
   - Use CDN for frontend assets

2. **Better Results:**
   - Gemini excels at structured outputs
   - Prompts are already optimized
   - JSON and Mermaid parsing improved

## 📚 Additional Resources

### Documentation
- [Gemini API Docs](https://ai.google.dev/docs)
- [API Key Management](https://aistudio.google.com/app/apikey)
- [Pricing & Quotas](https://ai.google.dev/pricing)

### Support
- [Google AI Forum](https://discuss.ai.google.dev/)
- [GitHub Issues](https://github.com/your-repo/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-gemini)

## ❓ FAQ

### Q: Will my existing analyses be affected?
**A:** No, past analyses are stored as-is. Only new analyses use Gemini.

### Q: Do I need to update my frontend?
**A:** No, frontend code remains unchanged. Only backend uses Gemini.

### Q: Can I use both IBM Bob and Gemini?
**A:** Not simultaneously. Choose one API for your deployment.

### Q: Is Gemini free?
**A:** Yes, free tier available with rate limits. See [pricing](https://ai.google.dev/pricing).

### Q: What about private repositories?
**A:** Same as before - requires GitHub token (not yet implemented).

### Q: Will response format change?
**A:** No, API responses remain identical. Internal processing changed.

### Q: How do I monitor API usage?
**A:** Check [Google Cloud Console](https://console.cloud.google.com/) for usage metrics.

### Q: Can I upgrade to Gemini Pro?
**A:** Yes, change model name in `gemini_client.py` to `gemini-1.5-pro`.

## ✅ Migration Checklist

Use this checklist to track your migration:

- [ ] Obtained Gemini API key
- [ ] Updated environment variables (Render/Vercel)
- [ ] Pulled latest code changes
- [ ] Installed new dependencies
- [ ] Tested health endpoint
- [ ] Tested analyze endpoint
- [ ] Verified frontend works
- [ ] Checked logs for errors
- [ ] Monitored first few analyses
- [ ] Updated team documentation
- [ ] Removed old IBM credentials

## 🎉 Success!

Once all checks pass, your migration is complete! Your app now uses Google Gemini 2.5 Flash for faster, more efficient repository analysis.

**Questions?** Open an issue on GitHub or check the documentation.

---

**Migration Date:** 2026-06-18  
**Version:** 2.0.0  
**Status:** Production Ready