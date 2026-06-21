"""API contract tests for Repo Accelerate."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from backend.gemini_client import GeminiClientError
from backend.main import app
from backend.repo_reader import RepoReaderError


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def repository_files():
    return {
        "main.py": "from fastapi import FastAPI",
        "README.md": "# Test",
    }


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "3.0.0"}


@patch("backend.main.clone_and_read")
@patch("backend.main.ask_gemini")
def test_analyze_defaults_to_english(mock_gemini, mock_clone, client, repository_files):
    mock_clone.return_value = repository_files
    mock_gemini.side_effect = [
        "flowchart LR\nA[Frontend] --> B[API]",
        '{"flows":[{"name":"Request","description":"A request","steps":["Send"],"files":["main.py"]}]}',
        "## 1. What does this project do?\nA test.",
    ]

    response = client.post("/analyze", json={"url": "https://github.com/test/repo"})
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "en"
    assert data["files_analyzed"] == 2
    assert data["architecture_mermaid"].startswith("flowchart LR")
    assert all("OUTPUT LANGUAGE: English" in call.args[0] for call in mock_gemini.call_args_list)


@patch("backend.main.clone_and_read")
@patch("backend.main.ask_gemini")
def test_analyze_propagates_spanish(mock_gemini, mock_clone, client, repository_files):
    mock_clone.return_value = repository_files
    mock_gemini.side_effect = [
        "```mermaid\nflowchart LR\nA[Interfaz] --> B[API]\n```",
        '```json\n{"flows":[{"name":"Solicitud","description":"Procesa datos","steps":["Enviar"],"files":["main.py"]}]}\n```',
        "## 1. ¿Qué hace este proyecto?\nUna prueba.",
    ]

    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo", "language": "es"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "es"
    assert data["flows"][0]["name"] == "Solicitud"
    assert not data["architecture_mermaid"].startswith("```")
    assert all("OUTPUT LANGUAGE: Spanish" in call.args[0] for call in mock_gemini.call_args_list)


@patch("backend.main.clone_and_read")
@patch("backend.main.ask_gemini")
def test_invalid_flow_json_uses_localized_fallback(mock_gemini, mock_clone, client, repository_files):
    mock_clone.return_value = repository_files
    mock_gemini.side_effect = [
        "flowchart LR\nA --> B",
        "not-json",
        "## Guía",
    ]
    response = client.post(
        "/analyze",
        json={"url": "https://github.com/test/repo", "language": "es"},
    )
    assert response.status_code == 200
    assert response.json()["flows"][0]["name"] == "Análisis de flujos no disponible"


@pytest.mark.parametrize("payload", [
    {"url": "https://gitlab.com/test/repo"},
    {"url": "https://github.com/test/repo", "language": "fr"},
    {},
])
def test_invalid_requests_return_422(client, payload):
    assert client.post("/analyze", json=payload).status_code == 422


@patch("backend.main.clone_and_read")
def test_repository_errors_return_400(mock_clone, client):
    mock_clone.side_effect = RepoReaderError("Repository not found")
    response = client.post("/analyze", json={"url": "https://github.com/test/repo"})
    assert response.status_code == 400
    assert "Failed to read repository" in response.json()["detail"]


@patch("backend.main.clone_and_read")
@patch("backend.main.ask_gemini")
def test_gemini_errors_return_500(mock_gemini, mock_clone, client, repository_files):
    mock_clone.return_value = repository_files
    mock_gemini.side_effect = GeminiClientError("API unavailable")
    response = client.post("/analyze", json={"url": "https://github.com/test/repo"})
    assert response.status_code == 500
    assert "Failed to get response from Gemini AI" in response.json()["detail"]


def test_cors_allows_local_frontend(client):
    response = client.options(
        "/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
