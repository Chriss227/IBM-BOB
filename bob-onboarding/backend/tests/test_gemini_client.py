"""
Unit tests for Gemini API client.
Tests authentication, retry logic, error handling, and parallel requests.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio
import os

from backend.gemini_client import ask_gemini, ask_gemini_batch, GeminiClientError


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    monkeypatch.setenv('GEMINI_API_KEY', 'test-gemini-api-key-12345')


@pytest.mark.asyncio
async def test_ask_gemini_success(mock_env_vars):
    """Test successful API call to Gemini."""
    mock_response = MagicMock()
    mock_response.text = 'This is Gemini\'s response'
    
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(return_value=mock_response)
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            result = await ask_gemini("Test prompt")
            
            assert result == 'This is Gemini\'s response'
            assert mock_instance.generate_content_async.called


@pytest.mark.asyncio
async def test_ask_gemini_invalid_api_key(mock_env_vars):
    """Test authentication error handling."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(
            side_effect=Exception("API key not valid")
        )
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            with pytest.raises(GeminiClientError) as exc_info:
                await ask_gemini("Test prompt")
            
            assert "Invalid API key" in str(exc_info.value) or "authentication" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_gemini_rate_limit(mock_env_vars):
    """Test rate limiting error."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(
            side_effect=Exception("429 Rate limit exceeded")
        )
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            with pytest.raises(GeminiClientError) as exc_info:
                await ask_gemini("Test prompt", max_retries=1)
            
            assert "Rate limit" in str(exc_info.value) or "quota" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_gemini_timeout_with_retry(mock_env_vars):
    """Test timeout with exponential backoff retry."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        
        # First two attempts timeout, third succeeds
        mock_response = MagicMock()
        mock_response.text = 'Success after retries'
        
        mock_instance.generate_content_async = AsyncMock(
            side_effect=[
                asyncio.TimeoutError("Timeout"),
                asyncio.TimeoutError("Timeout"),
                mock_response
            ]
        )
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
                result = await ask_gemini("Test prompt", max_retries=3)
                
                assert result == 'Success after retries'
                # Verify exponential backoff: 1s, 2s
                assert mock_sleep.call_count == 2
                mock_sleep.assert_any_call(1)  # 2^0
                mock_sleep.assert_any_call(2)  # 2^1


@pytest.mark.asyncio
async def test_ask_gemini_network_error(mock_env_vars):
    """Test network failure handling."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(
            side_effect=Exception("Connection failed")
        )
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            with pytest.raises(GeminiClientError) as exc_info:
                await ask_gemini("Test prompt", max_retries=2)
            
            assert "Failed to get response from Gemini" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_gemini_batch_parallel(mock_env_vars):
    """Test parallel batch request execution."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        
        # Return different responses for each prompt
        responses = [
            MagicMock(text='Response 1'),
            MagicMock(text='Response 2'),
            MagicMock(text='Response 3')
        ]
        
        mock_instance.generate_content_async = AsyncMock(side_effect=responses)
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
            results = await ask_gemini_batch(prompts)
            
            assert len(results) == 3
            assert results[0] == 'Response 1'
            assert results[1] == 'Response 2'
            assert results[2] == 'Response 3'


@pytest.mark.asyncio
async def test_missing_environment_variables():
    """Test validation of required environment variables."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(GeminiClientError) as exc_info:
            await ask_gemini("Test prompt")
        
        assert "GEMINI_API_KEY" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_gemini_empty_response(mock_env_vars):
    """Test handling of empty response."""
    mock_response = MagicMock()
    mock_response.text = ''
    
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(return_value=mock_response)
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            with pytest.raises(GeminiClientError) as exc_info:
                await ask_gemini("Test prompt")
            
            assert "empty response" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_gemini_safety_filter_block(mock_env_vars):
    """Test handling of safety filter blocks."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(
            side_effect=Exception("Content blocked by safety filters")
        )
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            with pytest.raises(GeminiClientError) as exc_info:
                await ask_gemini("Test prompt", max_retries=1)
            
            assert "safety" in str(exc_info.value).lower() or "blocked" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_ask_gemini_model_initialization_error(mock_env_vars):
    """Test handling of model initialization errors."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_model.side_effect = Exception("Invalid model name")
        
        with patch('google.generativeai.configure'):
            with pytest.raises(GeminiClientError) as exc_info:
                await ask_gemini("Test prompt")
            
            assert "Failed to initialize" in str(exc_info.value)


@pytest.mark.asyncio
async def test_ask_gemini_custom_model(mock_env_vars):
    """Test using a custom model name."""
    mock_response = MagicMock()
    mock_response.text = 'Custom model response'
    
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(return_value=mock_response)
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            result = await ask_gemini("Test prompt", model="gemini-1.5-pro")
            
            assert result == 'Custom model response'
            mock_model.assert_called_with("gemini-1.5-pro")


@pytest.mark.asyncio
async def test_ask_gemini_timeout_parameter(mock_env_vars):
    """Test custom timeout parameter."""
    mock_response = MagicMock()
    mock_response.text = 'Response'
    
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = MagicMock()
        mock_instance.generate_content_async = AsyncMock(return_value=mock_response)
        mock_model.return_value = mock_instance
        
        with patch('google.generativeai.configure'):
            with patch('asyncio.wait_for', new_callable=AsyncMock) as mock_wait:
                mock_wait.return_value = mock_response
                
                await ask_gemini("Test prompt", timeout=30)
                
                # Verify timeout was passed to wait_for
                assert mock_wait.called
                call_args = mock_wait.call_args
                assert call_args[1]['timeout'] == 30


# Made with Gemini
