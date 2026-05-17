# 📚 API Documentation

## Bob Onboarding Accelerator API

**Base URL:** `https://api.bob-onboarding.com`  
**Version:** 1.0.0  
**Protocol:** HTTPS  
**Format:** JSON

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Error Handling](#error-handling)
4. [Rate Limiting](#rate-limiting)
5. [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication for public endpoints. Internal Bob API authentication is handled server-side.

---

## Endpoints

### Health Check

Check the API service status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is down

**Example:**
```bash
curl https://api.bob-onboarding.com/health
```

---

### Analyze Repository

Analyze a GitHub repository and generate architecture diagram, flows, and onboarding guide.

**Endpoint:** `POST /analyze`

**Request Body:**
```json
{
  "url": "https://github.com/owner/repository"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| url | string | Yes | GitHub repository URL (must start with `https://github.com/`) |

**Response:**
```json
{
  "architecture_mermaid": "graph LR\n    A[Frontend] --> B[Backend]\n    B --> C[Database]",
  "flows": [
    {
      "name": "User Authentication Flow",
      "description": "How users log in and get authenticated",
      "steps": [
        "User submits credentials to /login endpoint",
        "Server validates credentials against database",
        "JWT token is generated and returned"
      ],
      "files": ["auth.py", "models/user.py", "routes/login.py"]
    }
  ],
  "guide": "## 1. What does this project do?\n\nThis project...",
  "repository_url": "https://github.com/owner/repository",
  "files_analyzed": 42
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| architecture_mermaid | string | Mermaid diagram code showing system architecture |
| flows | array | List of key system flows (3 flows) |
| flows[].name | string | Name of the flow |
| flows[].description | string | Description of what the flow does |
| flows[].steps | array | Step-by-step breakdown of the flow |
| flows[].files | array | Relevant files for this flow |
| guide | string | Markdown onboarding guide with 5 sections |
| repository_url | string | The analyzed repository URL |
| files_analyzed | integer | Number of files analyzed |

**Status Codes:**
- `200 OK` - Analysis completed successfully
- `400 Bad Request` - Invalid repository URL or empty repository
- `422 Unprocessable Entity` - URL validation failed
- `500 Internal Server Error` - Analysis failed (Bob API error, etc.)

**Example:**
```bash
curl -X POST https://api.bob-onboarding.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com/octocat/Hello-World"}'
```

**Processing Time:**
- Small repos (<50 files): ~30 seconds
- Medium repos (50-200 files): ~60 seconds
- Large repos (>200 files): May timeout or be truncated

---

## Error Handling

All errors follow a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Failed to read repository: Repository not found"
}
```

#### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "url"],
      "msg": "URL must be a GitHub repository (https://github.com/...)",
      "type": "value_error"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Failed to get response from Bob AI: Rate limit exceeded"
}
```

---

## Rate Limiting

**Current Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

**Rate Limit Exceeded Response:**
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

---

## CORS

The API supports CORS for the following origins:
- `http://localhost:5173` (development)
- `http://127.0.0.1:5173` (development)
- `https://bob-onboarding.com` (production)

**CORS Headers:**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Examples

### Python

```python
import requests

# Analyze repository
response = requests.post(
    'https://api.bob-onboarding.com/analyze',
    json={'url': 'https://github.com/octocat/Hello-World'}
)

if response.status_code == 200:
    data = response.json()
    print(f"Analyzed {data['files_analyzed']} files")
    print(f"Architecture:\n{data['architecture_mermaid']}")
    print(f"Found {len(data['flows'])} flows")
else:
    print(f"Error: {response.json()['detail']}")
```

### JavaScript (Fetch)

```javascript
// Analyze repository
fetch('https://api.bob-onboarding.com/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://github.com/octocat/Hello-World'
  })
})
  .then(response => response.json())
  .then(data => {
    console.log(`Analyzed ${data.files_analyzed} files`);
    console.log('Architecture:', data.architecture_mermaid);
    console.log(`Found ${data.flows.length} flows`);
  })
  .catch(error => console.error('Error:', error));
```

### cURL

```bash
# Health check
curl https://api.bob-onboarding.com/health

# Analyze repository
curl -X POST https://api.bob-onboarding.com/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/octocat/Hello-World"
  }'

# Pretty print JSON response
curl -X POST https://api.bob-onboarding.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/octocat/Hello-World"}' \
  | jq .
```

---

## Response Time Guidelines

| Repository Size | Expected Time | Timeout |
|----------------|---------------|---------|
| Small (<50 files) | 20-30s | 60s |
| Medium (50-200 files) | 40-60s | 90s |
| Large (>200 files) | 60-90s | 120s |

---

## Best Practices

1. **Timeout Handling:** Set client timeout to at least 120 seconds
2. **Error Handling:** Always check status codes and handle errors gracefully
3. **Retry Logic:** Implement exponential backoff for 5xx errors
4. **Caching:** Cache results for the same repository URL
5. **Validation:** Validate GitHub URLs client-side before sending

---

## OpenAPI Specification

The full OpenAPI (Swagger) specification is available at:
- **Interactive Docs:** https://api.bob-onboarding.com/docs
- **ReDoc:** https://api.bob-onboarding.com/redoc
- **OpenAPI JSON:** https://api.bob-onboarding.com/openapi.json

---

## Support

For API support or questions:
- **Email:** support@bob-onboarding.com
- **GitHub Issues:** https://github.com/your-org/bob-onboarding/issues
- **Slack:** #bob-onboarding-support

---

## Changelog

### v1.0.0 (2026-05-17)
- Initial API release
- `/health` endpoint
- `/analyze` endpoint with architecture, flows, and guide generation