"""
Unit tests for Bob API client.
Tests authentication, retry logic, error handling, and parallel requests.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio
import os

from backend.bob_client import ask_bob, ask_bob_batch, BobClientError


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    monkeypatch.setenv('BOB_API_ENDPOINT', 'https://api.test.com/bob/v1/chat')
    monkeypatch.setenv('BOB_API_KEY', 'test-api-key-12345')


@pytest.mark.asyncio
async def test_ask_bob_success(mock_env_vars):
    """Test successful API call to Bob."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'text': 'This is Bob\'s response'}
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        result = await ask_bob("Test prompt")
        
        assert result == 'This is Bob\'s response'
        assert mock_client.return_value.__aenter__.return_value.post.called


@pytest.mark.asyncio
async def test_ask_bob_invalid_api_key(mock_env_vars):
    """Test 401 authentication error handling."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt")
        
        assert "Invalid API key" in str(exc_info.value)
        assert "401" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_rate_limit(mock_env_vars):
    """Test 429 rate limiting error."""
    mock_response = MagicMock()
    mock_response.status_code = 429
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt", max_retries=1)
        
        assert "Rate limit exceeded" in str(exc_info.value)
        assert "429" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_timeout_with_retry(mock_env_vars):
    """Test timeout with exponential backoff retry."""
    with patch('httpx.AsyncClient') as mock_client:
        # First two attempts timeout, third succeeds
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            side_effect=[
                httpx.TimeoutException("Timeout"),
                httpx.TimeoutException("Timeout"),
                MagicMock(status_code=200, json=lambda: {'text': 'Success after retries'})
            ]
        )
        
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            result = await ask_bob("Test prompt", max_retries=3)
            
            assert result == 'Success after retries'
            # Verify exponential backoff: 1s, 2s
            assert mock_sleep.call_count == 2
            mock_sleep.assert_any_call(1)  # 2^0
            mock_sleep.assert_any_call(2)  # 2^1


@pytest.mark.asyncio
async def test_ask_bob_network_error(mock_env_vars):
    """Test network failure handling."""
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            side_effect=httpx.NetworkError("Connection failed")
        )
        
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt", max_retries=2)
        
        assert "Failed to get response from Bob" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_batch_parallel(mock_env_vars):
    """Test parallel batch request execution."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    
    # Return different responses for each prompt
    responses = [
        {'text': 'Response 1'},
        {'text': 'Response 2'},
        {'text': 'Response 3'}
    ]
    mock_response.json.side_effect = responses
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
        results = await ask_bob_batch(prompts)
        
        assert len(results) == 3
        assert results[0] == 'Response 1'
        assert results[1] == 'Response 2'
        assert results[2] == 'Response 3'


@pytest.mark.asyncio
async def test_missing_environment_variables():
    """Test validation of required environment variables."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt")
        
        assert "BOB_API_ENDPOINT" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_missing_api_key():
    """Test missing API key environment variable."""
    with patch.dict(os.environ, {'BOB_API_ENDPOINT': 'https://api.test.com'}, clear=True):
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt")
        
        assert "BOB_API_KEY" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_invalid_json_response(mock_env_vars):
    """Test handling of invalid JSON in response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt")
        
        assert "Failed to parse" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_missing_text_field(mock_env_vars):
    """Test handling of response missing 'text' field."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'error': 'No text field'}
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt")
        
        assert "missing 'text' field" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_empty_text_response(mock_env_vars):
    """Test handling of empty text in response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'text': ''}
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt")
        
        assert "empty or invalid text" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_bob_server_error_500(mock_env_vars):
    """Test handling of 500 server errors."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        with pytest.raises(BobClientError) as exc_info:
            await ask_bob("Test prompt", max_retries=1)
        
        assert "server error" in str(exc_info.value)
        assert "500" in str(exc_info.value)

# Made with Bob
