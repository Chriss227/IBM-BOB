# 🛠️ Gemini Migration Implementation Guide

## Overview

This guide provides detailed, step-by-step instructions for implementing the migration from IBM Bob API to Google Gemini 2.5 Flash API.

## 📋 Prerequisites

Before starting the migration:

1. **Obtain Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy and securely store your API key

2. **Backup Current Implementation**
   ```bash
   git checkout -b backup-bob-implementation
   git push origin backup-bob-implementation
   git checkout main
   git checkout -b feature/gemini-migration
   ```

3. **Install Required Tools**
   ```bash
   pip install google-generativeai
   ```

## 🔧 Step-by-Step Implementation

### Step 1: Create Gemini Client Module

**File:** `bob-onboarding/backend/gemini_client.py`

**Key Features:**
- Direct API key authentication (no IAM token needed)
- Async/await support
- Retry logic with exponential backoff
- Error handling for rate limits and timeouts
- Batch processing support

**Implementation Notes:**
```python
import google.generativeai as genai
import asyncio
from typing import Optional

class GeminiClientError(Exception):
    """Custom exception for Gemini API errors"""
    pass

async def ask_gemini(
    prompt: str,
    model: str = "gemini-2.5-flash",
    timeout: int = 60,
    max_retries: int = 3
) -> str:
    """
    Send prompt to Gemini API with retry logic
    
    Key differences from Bob:
    1. No IAM token - direct API key
    2. Use genai.GenerativeModel
    3. Different response structure
    4. Built-in safety settings
    """
    # Configure API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise GeminiClientError("GEMINI_API_KEY not set")
    
    genai.configure(api_key=api_key)
    
    # Create model instance
    model_instance = genai.GenerativeModel(model)
    
    # Generation config
    generation_config = {
        'temperature': 0.7,
        'max_output_tokens': 2000,
    }
    
    # Retry logic
    for attempt in range(max_retries):
        try:
            response = await model_instance.generate_content_async(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            # Handle errors with exponential backoff
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            else:
                raise GeminiClientError(f"Failed after {max_retries} attempts: {e}")
```

### Step 2: Update Environment Configuration

**File:** `bob-onboarding/backend/.env.example`

**Changes:**
```diff
- # IBM Bob API Configuration
- BOB_API_ENDPOINT=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
- BOB_API_KEY=your_bob_api_key_here
+ # Google Gemini API Configuration
+ GEMINI_API_KEY=your_gemini_api_key_here

  # Server Configuration
  PORT=8000
  HOST=0.0.0.0

  # Environment
  ENVIRONMENT=development
```

### Step 3: Update Main Application

**File:** `bob-onboarding/backend/main.py`

**Changes:**
```diff
- from bob_client import ask_bob, BobClientError
+ from gemini_client import ask_gemini, GeminiClientError

  # In analyze_repository function:
- architecture_raw, flows_raw, guide_raw = await asyncio.gather(
-     ask_bob(architecture_prompt),
-     ask_bob(flows_prompt),
-     ask_bob(guide_prompt)
- )
+ architecture_raw, flows_raw, guide_raw = await asyncio.gather(
+     ask_gemini(architecture_prompt),
+     ask_gemini(flows_prompt),
+     ask_gemini(guide_prompt)
+ )

  # Update error handling:
- except BobClientError as e:
-     logger.error(f"Bob AI error: {str(e)}")
+ except GeminiClientError as e:
+     logger.error(f"Gemini AI error: {str(e)}")
      raise HTTPException(
          status_code=500,
-         detail=f"Failed to get response from Bob AI: {str(e)}"
+         detail=f"Failed to get response from Gemini AI: {str(e)}"
      )
```

### Step 4: Update Dependencies

**File:** `bob-onboarding/requirements.txt`

**Changes:**
```diff
  fastapi==0.109.0
  uvicorn[standard]==0.27.0
  gitpython==3.1.41
  httpx==0.26.0
  python-dotenv==1.0.0
  pydantic==2.5.3
+ google-generativeai==0.3.2

  # Testing dependencies
  pytest==7.4.3
  pytest-asyncio==0.21.1
  pytest-cov==4.1.0
  pytest-mock==3.12.0
  pytest-timeout==2.2.0
  httpx==0.26.0

  # Security testing
  safety==2.3.5
  bandit==1.7.5

  # Performance testing
  locust==2.20.0
```

### Step 5: Update Tests

**File:** `bob-onboarding/backend/tests/test_gemini_client.py` (renamed from test_bob_client.py)

**Key Changes:**
1. Rename all `test_ask_bob_*` to `test_ask_gemini_*`
2. Update mock responses to match Gemini format
3. Remove IAM token tests
4. Add Gemini-specific error tests

**Example:**
```python
@pytest.mark.asyncio
async def test_ask_gemini_success(mock_env_vars):
    """Test successful Gemini API call."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_model.return_value.generate_content_async.return_value = mock_response
        
        result = await ask_gemini("Test prompt")
        assert result == "Test response"
```

### Step 6: Update Documentation

**Files to Update:**
1. `README.md` - Update API references
2. `DEPLOYMENT.md` - Update environment variables
3. `docs/API_DOCUMENTATION.md` - Update API details
4. `DEVELOPMENT.md` - Update setup instructions

**Key Changes:**
- Replace "IBM Bob" with "Google Gemini"
- Update API key setup instructions
- Update environment variable names
- Update troubleshooting sections

### Step 7: Fix Existing Bugs

**Bug 1: Circular Import in bob_client.py**

**Location:** Line 54 in `bob-onboarding/backend/bob_client.py`

**Current Code:**
```python
except Exception as e:
    from bob_client import BobClientError  # ❌ Circular import!
    raise BobClientError(f"Failed to get IAM token: {str(e)}")
```

**Fixed Code:**
```python
except Exception as e:
    raise BobClientError(f"Failed to get IAM token: {str(e)}")
```

**Note:** This bug won't exist in the new `gemini_client.py` as we're creating it from scratch.

## 🧪 Testing Strategy

### Local Testing

1. **Set up environment:**
   ```bash
   cd bob-onboarding/backend
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

2. **Test Gemini client directly:**
   ```bash
   python gemini_client.py
   ```

3. **Run unit tests:**
   ```bash
   pytest tests/test_gemini_client.py -v
   ```

4. **Run integration tests:**
   ```bash
   pytest tests/integration/ -v
   ```

5. **Test full application:**
   ```bash
   uvicorn main:app --reload
   # In another terminal:
   curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"url": "https://github.com/tiangolo/fastapi"}'
   ```

### Validation Checklist

- [ ] Gemini client initializes correctly
- [ ] API calls return valid responses
- [ ] Error handling works (invalid key, rate limits)
- [ ] Retry logic functions properly
- [ ] Batch processing works
- [ ] All tests pass
- [ ] No circular imports
- [ ] Documentation is accurate

## 🚀 Deployment Steps

### 1. Update Render Environment Variables

1. Go to Render Dashboard
2. Select your service
3. Navigate to Environment tab
4. Remove old variables:
   - `BOB_API_ENDPOINT`
   - `BOB_API_KEY`
5. Add new variable:
   - `GEMINI_API_KEY` = your_gemini_api_key

### 2. Deploy to Render

```bash
git add .
git commit -m "Migrate from IBM Bob to Google Gemini 2.5 Flash"
git push origin feature/gemini-migration
```

Create pull request and merge to main. Render will auto-deploy.

### 3. Verify Deployment

```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Test analyze endpoint
curl -X POST https://your-app.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/tiangolo/fastapi"}'
```

## 🔄 Rollback Procedure

If issues occur:

1. **Immediate Rollback:**
   ```bash
   git revert HEAD
   git push origin main
   ```

2. **Restore Environment Variables:**
   - Re-add `BOB_API_ENDPOINT` and `BOB_API_KEY` in Render
   - Remove `GEMINI_API_KEY`

3. **Verify Rollback:**
   - Test health endpoint
   - Test analyze endpoint
   - Check logs for errors

## 📊 Performance Monitoring

### Metrics to Track

1. **Response Time:**
   - Target: < 60 seconds per analysis
   - Monitor: Render logs and metrics

2. **Error Rate:**
   - Target: < 1% error rate
   - Monitor: Application logs

3. **API Usage:**
   - Track Gemini API quota usage
   - Monitor rate limit errors

4. **Cost:**
   - Compare Gemini costs vs IBM Bob
   - Optimize token usage if needed

## 🐛 Troubleshooting

### Common Issues

**Issue: "GEMINI_API_KEY not set"**
- **Solution:** Verify environment variable is set in Render
- **Check:** `echo $GEMINI_API_KEY` in Render shell

**Issue: "Rate limit exceeded"**
- **Solution:** Implement request throttling
- **Check:** Gemini API quota in Google Cloud Console

**Issue: "Invalid API key"**
- **Solution:** Regenerate API key in Google AI Studio
- **Update:** Environment variable in Render

**Issue: Response format errors**
- **Solution:** Check Gemini response structure
- **Debug:** Log raw responses before parsing

## ✅ Success Criteria

Migration is successful when:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] API responds in < 60 seconds
- [ ] Error rate < 1%
- [ ] Documentation is updated
- [ ] Deployment is stable
- [ ] No breaking changes for users

## 📚 Additional Resources

- [Gemini API Quickstart](https://ai.google.dev/tutorials/python_quickstart)
- [google-generativeai SDK Docs](https://ai.google.dev/api/python/google/generativeai)
- [Gemini Model Parameters](https://ai.google.dev/api/generate-content#method:-models.generatecontent)
- [Rate Limits & Quotas](https://ai.google.dev/pricing)

## 🎯 Next Steps

After successful migration:

1. Monitor performance for 1 week
2. Gather user feedback
3. Optimize prompts for Gemini
4. Consider upgrading to Gemini Pro if needed
5. Implement caching for repeated queries

---

**Last Updated:** 2026-06-18  
**Status:** Ready for Implementation  
**Estimated Time:** 4-6 hours