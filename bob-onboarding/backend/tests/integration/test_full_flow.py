"""
Integration tests for complete analysis flow.
These tests require Gemini API credentials and may take longer to run.
"""
import pytest
from fastapi.testclient import TestClient
import os

from backend.main import app

client = TestClient(app)


@pytest.mark.integration
class TestFullAnalysisFlow:
    """Integration tests for complete repository analysis."""
    
    def test_health_endpoint(self):
        """Test health endpoint is accessible."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
    
    @pytest.mark.skipif(
        not os.getenv('GEMINI_API_KEY'),
        reason="GEMINI_API_KEY not set - skipping integration test"
    )
    def test_complete_analysis_small_repo(self):
        """Test full analysis with a small real repository."""
        response = client.post(
            "/analyze",
            json={"url": "https://github.com/octocat/Hello-World"},
            timeout=120
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields are present
        assert "architecture_mermaid" in data
        assert "flows" in data
        assert "guide" in data
        assert "repository_url" in data
        assert "files_analyzed" in data
        
        # Verify data types
        assert isinstance(data["architecture_mermaid"], str)
        assert isinstance(data["flows"], list)
        assert isinstance(data["guide"], str)
        assert isinstance(data["files_analyzed"], int)
        
        # Verify content is not empty
        assert len(data["architecture_mermaid"]) > 0
        assert len(data["flows"]) > 0
        assert len(data["guide"]) > 0
        assert data["files_analyzed"] > 0
        
        # Verify flow structure
        for flow in data["flows"]:
            assert "name" in flow
            assert "description" in flow
            assert "steps" in flow
            assert "files" in flow
            assert isinstance(flow["steps"], list)
            assert isinstance(flow["files"], list)
    
    def test_invalid_github_url(self):
        """Test that non-GitHub URLs are rejected."""
        response = client.post(
            "/analyze",
            json={"url": "https://gitlab.com/user/repo"}
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_malformed_url(self):
        """Test that malformed URLs are rejected."""
        response = client.post(
            "/analyze",
            json={"url": "not-a-url"}
        )
        
        assert response.status_code == 422
    
    def test_missing_url(self):
        """Test that missing URL is rejected."""
        response = client.post(
            "/analyze",
            json={}
        )
        
        assert response.status_code == 422
    
    @pytest.mark.skipif(
        not os.getenv('GEMINI_API_KEY'),
        reason="GEMINI_API_KEY not set - skipping integration test"
    )
    def test_nonexistent_repository(self):
        """Test handling of non-existent repository."""
        response = client.post(
            "/analyze",
            json={"url": "https://github.com/nonexistent-user-12345/nonexistent-repo-67890"}
        )
        
        # Should return 400 for repository not found
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "repository" in data["detail"].lower() or "failed" in data["detail"].lower()
    
    @pytest.mark.skipif(
        not os.getenv('GEMINI_API_KEY'),
        reason="GEMINI_API_KEY not set - skipping integration test"
    )
    @pytest.mark.slow
    def test_concurrent_requests(self):
        """Test that multiple concurrent requests complete successfully."""
        import concurrent.futures
        
        urls = [
            "https://github.com/octocat/Hello-World",
            "https://github.com/octocat/Spoon-Knife",
        ]
        
        def analyze_repo(url):
            response = client.post(
                "/analyze",
                json={"url": url},
                timeout=120
            )
            return response.status_code, response.json()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(analyze_repo, url) for url in urls]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for status_code, data in results:
            assert status_code == 200
            assert "architecture_mermaid" in data
            assert "flows" in data
            assert "guide" in data
    
    def test_cors_headers(self):
        """Test that CORS headers are present."""
        response = client.options(
            "/analyze",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
    
    @pytest.mark.skipif(
        not os.getenv('GEMINI_API_KEY'),
        reason="GEMINI_API_KEY not set - skipping integration test"
    )
    def test_response_time_small_repo(self):
        """Test that small repositories complete within acceptable time."""
        import time
        
        start_time = time.time()
        response = client.post(
            "/analyze",
            json={"url": "https://github.com/octocat/Hello-World"},
            timeout=120
        )
        end_time = time.time()
        
        duration = end_time - start_time
        
        assert response.status_code == 200
        # Small repos should complete in under 60 seconds
        assert duration < 60, f"Analysis took {duration:.2f}s, expected < 60s"
    
    @pytest.mark.skipif(
        not os.getenv('GEMINI_API_KEY'),
        reason="GEMINI_API_KEY not set - skipping integration test"
    )
    def test_mermaid_diagram_format(self):
        """Test that Mermaid diagram has correct format."""
        response = client.post(
            "/analyze",
            json={"url": "https://github.com/octocat/Hello-World"},
            timeout=120
        )
        
        assert response.status_code == 200
        data = response.json()
        
        mermaid = data["architecture_mermaid"]
        
        # Should start with graph declaration
        assert mermaid.strip().startswith("graph")
        # Should not have markdown fences
        assert not mermaid.startswith("```")
        assert not mermaid.endswith("```")
        # Should contain arrows (relationships)
        assert "-->" in mermaid or "---" in mermaid
    
    @pytest.mark.skipif(
        not os.getenv('GEMINI_API_KEY'),
        reason="GEMINI_API_KEY not set - skipping integration test"
    )
    def test_flows_structure(self):
        """Test that flows have correct structure."""
        response = client.post(
            "/analyze",
            json={"url": "https://github.com/octocat/Hello-World"},
            timeout=120
        )
        
        assert response.status_code == 200
        data = response.json()
        
        flows = data["flows"]
        
        # Should have at least one flow
        assert len(flows) >= 1
        # Should have at most 3 flows (as per spec)
        assert len(flows) <= 3
        
        for flow in flows:
            # Each flow should have required fields
            assert len(flow["name"]) > 0
            assert len(flow["description"]) > 0
            assert len(flow["steps"]) > 0
            # Steps should be strings
            for step in flow["steps"]:
                assert isinstance(step, str)
                assert len(step) > 0
    
    @pytest.mark.skipif(
        not os.getenv('GEMINI_API_KEY'),
        reason="GEMINI_API_KEY not set - skipping integration test"
    )
    def test_guide_structure(self):
        """Test that guide has correct structure."""
        response = client.post(
            "/analyze",
            json={"url": "https://github.com/octocat/Hello-World"},
            timeout=120
        )
        
        assert response.status_code == 200
        data = response.json()
        
        guide = data["guide"]
        
        # Should be markdown format
        assert "##" in guide
        # Should have the 5 required sections
        assert "What does this project do" in guide or "what does this project do" in guide.lower()
        assert "How to run it locally" in guide or "how to run" in guide.lower()
        assert "important files" in guide.lower() or "5 most important" in guide.lower()
        assert "Gotchas" in guide or "gotchas" in guide.lower() or "non-obvious" in guide.lower()
        assert "first contribution" in guide.lower() or "where to start" in guide.lower()

# Made with Gemini
