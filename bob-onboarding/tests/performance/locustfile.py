"""
Performance tests using Locust for Repo Accelerate.
Run with: locust -f tests/performance/locustfile.py --host=http://localhost:8000
"""
from locust import HttpUser, task, between
import random


class RepoAccelerateUser(HttpUser):
    """Simulated user for load testing."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    # Sample repository URLs for testing
    test_repos = [
        "https://github.com/octocat/Hello-World",
        "https://github.com/octocat/Spoon-Knife",
        "https://github.com/github/gitignore",
    ]
    
    @task(10)
    def health_check(self):
        """Test health endpoint (most frequent)."""
        self.client.get("/health")
    
    @task(1)
    def analyze_repository(self):
        """Test repository analysis (less frequent, more expensive)."""
        repo_url = random.choice(self.test_repos)
        
        with self.client.post(
            "/analyze",
            json={"url": repo_url},
            catch_response=True,
            timeout=120
        ) as response:
            if response.status_code == 200:
                data = response.json()
                # Verify response structure
                if all(key in data for key in ["architecture_mermaid", "flows", "guide"]):
                    response.success()
                else:
                    response.failure("Missing required fields in response")
            elif response.status_code == 400:
                # Expected for some test cases
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(2)
    def analyze_invalid_url(self):
        """Test error handling with invalid URLs."""
        invalid_urls = [
            "https://gitlab.com/user/repo",
            "not-a-url",
            "https://github.com/nonexistent/repo"
        ]
        
        url = random.choice(invalid_urls)
        
        with self.client.post(
            "/analyze",
            json={"url": url},
            catch_response=True
        ) as response:
            if response.status_code in [400, 422]:
                response.success()
            else:
                response.failure(f"Expected 400 or 422, got {response.status_code}")


class StressTestUser(HttpUser):
    """User for stress testing with higher load."""
    
    wait_time = between(0.5, 1)  # Shorter wait time for stress testing
    
    @task
    def rapid_health_checks(self):
        """Rapid health check requests."""
        self.client.get("/health")


class SpikeTestUser(HttpUser):
    """User for spike testing with sudden load increases."""
    
    wait_time = between(0.1, 0.5)  # Very short wait time
    
    @task
    def burst_requests(self):
        """Burst of rapid requests."""
        for _ in range(5):
            self.client.get("/health")

# Made with Repo Accelerate
