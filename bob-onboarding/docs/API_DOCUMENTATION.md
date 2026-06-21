# Repo Accelerate API

## Health

`GET /health`

```json
{
  "status": "ok",
  "version": "3.0.0"
}
```

## Analyze repository

`POST /analyze`

Request:

```json
{
  "url": "https://github.com/owner/repository",
  "language": "en"
}
```

Fields:

| Field | Required | Values |
| --- | --- | --- |
| `url` | Yes | Public `https://github.com/{owner}/{repo}` URL |
| `language` | No | `en` or `es`; defaults to `en` |

Response:

```json
{
  "architecture_mermaid": "flowchart LR\nA[Frontend] --> B[API]",
  "flows": [
    {
      "name": "Request flow",
      "description": "How a request is processed",
      "steps": ["Receive request", "Run service", "Return response"],
      "files": ["backend/main.py"]
    }
  ],
  "guide": "## 1. What does this project do?",
  "repository_url": "https://github.com/owner/repository",
  "files_analyzed": 42,
  "language": "en"
}
```

The service returns `422` for invalid request data, `400` when the repository
cannot be read, and `500` when Gemini or internal processing fails.

Interactive OpenAPI documentation is available at `/docs`.
