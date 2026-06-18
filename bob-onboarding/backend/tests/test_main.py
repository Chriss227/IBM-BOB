"""
Unit tests for FastAPI endpoints.
Tests health check, analyze endpoint, error handling, and CORS.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import json

from backend.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_repo_contents():
    """Mock repository contents."""
    return {
        "main.py": "from fastapi import FastAPI\napp = FastAPI()",
        "README.md": "# Test Project"
    }


def test_health_endpoint(client):
    """Test /health endpoint returns 200."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


@patch('backend.main.clone_and_read')
@patch('backend.main.ask_bob')
def test_analyze_valid_repo(mock_ask_bob, mock_clone, client, mock_repo_contents):
    """Test successful analysis flow."""
    # Mock repository cloning
    mock_clone.return_value = mock_repo_contents
    
    # Mock Bob AI responses
    mock_ask_bob.side_effect = [
        "graph LR\n    A[Frontend] --> B[Backend]",  # Architecture
        '{"flows": [{"name": "Test Flow", "description": "Test", "steps": ["Step 1"], "files": ["main.py"]}]}',  # Flows
        "## 1. What does this project do?\nTest project"  # Guide
    ]
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "architecture_mermaid" in data
    assert "flows" in data
    assert "guide" in data
    assert "repository_url" in data
    assert "files_analyzed" in data
    assert data["files_analyzed"] == 2
    assert len(data["flows"]) == 1


def test_analyze_invalid_url(client):
    """Test URL validation returns 422."""
    response = client.post(
        "/analyze",
        json={"url": "https://gitlab.com/test/repo"}
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_analyze_invalid_url_format(client):
    """Test invalid URL format."""
    response = client.post(
        "/analyze",
        json={"url": "not-a-url"}
    )
    
    assert response.status_code == 422


@patch('backend.main.clone_and_read')
def test_analyze_empty_repo(mock_clone, client):
    """Test empty repository returns 400."""
    mock_clone.return_value = {}
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/empty-repo"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "No readable files found" in data["detail"]


@patch('backend.main.clone_and_read')
@patch('backend.main.ask_bob')
def test_analyze_bob_api_failure(mock_ask_bob, mock_clone, client, mock_repo_contents):
    """Test Bob API error handling returns 500."""
    mock_clone.return_value = mock_repo_contents
    
    # Mock Bob API failure
    from backend.bob_client import BobClientError
    mock_ask_bob.side_effect = BobClientError("API key invalid")
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo"}
    )
    
    assert response.status_code == 500
    data = response.json()
    assert "Failed to get response from Gemini AI" in data["detail"]


@patch('backend.main.clone_and_read')
@patch('backend.main.ask_bob')
def test_analyze_invalid_flows_json(mock_ask_bob, mock_clone, client, mock_repo_contents):
    """Test fallback for malformed JSON in flows."""
    mock_clone.return_value = mock_repo_contents
    
    # Mock responses with invalid JSON for flows
    mock_ask_bob.side_effect = [
        "graph LR\n    A[Frontend] --> B[Backend]",  # Architecture
        "This is not valid JSON",  # Invalid flows
        "## 1. What does this project do?\nTest project"  # Guide
    ]
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo"}
    )
    
    assert response.status_code == 200
    data = response.json()
    # Should have fallback flow
    assert len(data["flows"]) == 1
    assert "Analysis Error" in data["flows"][0]["name"]


def test_cors_headers(client):
    """Test CORS configuration."""
    response = client.options(
        "/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        }
    )
    
    # CORS should allow the request
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


@patch('backend.main.clone_and_read')
@patch('backend.main.ask_bob')
def test_analyze_cleans_mermaid_fences(mock_ask_bob, mock_clone, client, mock_repo_contents):
    """Test that markdown fences are removed from Mermaid."""
    mock_clone.return_value = mock_repo_contents
    
    # Mock Bob returning Mermaid with markdown fences
    mock_ask_bob.side_effect = [
        "```mermaid\ngraph LR\n    A[Frontend] --> B[Backend]\n```",  # Architecture with fences
        '{"flows": [{"name": "Test", "description": "Test", "steps": ["Step 1"], "files": ["main.py"]}]}',
        "## Guide"
    ]
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo"}
    )
    
    assert response.status_code == 200
    data = response.json()
    # Fences should be removed
    assert not data["architecture_mermaid"].startswith("```")
    assert not data["architecture_mermaid"].endswith("```")
    assert "graph LR" in data["architecture_mermaid"]


@patch('backend.main.clone_and_read')
@patch('backend.main.ask_bob')
def test_analyze_cleans_json_fences(mock_ask_bob, mock_clone, client, mock_repo_contents):
    """Test that markdown fences are removed from JSON."""
    mock_clone.return_value = mock_repo_contents
    
    # Mock Bob returning JSON with markdown fences
    mock_ask_bob.side_effect = [
        "graph LR\n    A --> B",
        '```json\n{"flows": [{"name": "Test", "description": "Test", "steps": ["Step 1"], "files": ["main.py"]}]}\n```',
        "## Guide"
    ]
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["flows"]) == 1


@patch('backend.main.clone_and_read')
def test_analyze_repo_reader_error(mock_clone, client):
    """Test handling of repository reading errors."""
    from backend.repo_reader import RepoReaderError
    mock_clone.side_effect = RepoReaderError("Repository not found")
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "Failed to read repository" in data["detail"]


def test_analyze_missing_url(client):
    """Test request without URL."""
    response = client.post("/analyze", json={})
    
    assert response.status_code == 422


def test_analyze_null_url(client):
    """Test request with null URL."""
    response = client.post("/analyze", json={"url": None})
    
    assert response.status_code == 422


@patch('backend.main.clone_and_read')
@patch('backend.main.ask_bob')
def test_analyze_returns_correct_structure(mock_ask_bob, mock_clone, client, mock_repo_contents):
    """Test that response has correct structure."""
    mock_clone.return_value = mock_repo_contents
    
    mock_ask_bob.side_effect = [
        "graph LR\n    A --> B",
        '{"flows": [{"name": "Flow1", "description": "Desc", "steps": ["S1", "S2"], "files": ["f1.py", "f2.py"]}]}',
        "## Guide\nContent"
    ]
    
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert isinstance(data["architecture_mermaid"], str)
    assert isinstance(data["flows"], list)
    assert isinstance(data["guide"], str)
    assert isinstance(data["repository_url"], str)
    assert isinstance(data["files_analyzed"], int)
    
    # Verify flow structure
    flow = data["flows"][0]
    assert "name" in flow
    assert "description" in flow
    assert "steps" in flow
    assert "files" in flow
    assert isinstance(flow["steps"], list)
    assert isinstance(flow["files"], list)


def test_404_handler(client):
    """Test 404 error handler."""
    response = client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data or "detail" in data

# Made with Bob
