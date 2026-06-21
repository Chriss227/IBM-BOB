"""
Google Gemini API client with retry logic and error handling.
Uses the new google-genai library that supports both old (AIza...) and new (AQ....) API key formats.

Note: Google has updated their API key format:
- New keys: Start with "AQ." (e.g., AQ.Ab8RN6IxkvazkDr16g5K...)
- Old keys: Start with "AIza" (still supported for backward compatibility)

Get your API key from: https://aistudio.google.com/app/apikey
"""
import os
import asyncio
from google import genai  # pyright: ignore[reportAttributeAccessIssue]
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)


class GeminiClientError(Exception):
    """Custom exception for Gemini API client errors."""
    pass


async def ask_gemini(
    prompt: str,
    model: str = "gemini-2.5-flash",
    timeout: int = 60,
    max_retries: int = 3
) -> str:
    """
    Send a prompt to Google Gemini API and get the response.
    
    This function implements:
    - Direct API key authentication (supports new AQ. format)
    - Exponential backoff retry logic (3 attempts)
    - 60 second timeout per request
    - Proper error handling and logging
    - Environment variable configuration
    
    Args:
        prompt: The prompt to send to Gemini
        model: The Gemini model to use (default: "gemini-2.5-flash")
        timeout: Request timeout in seconds (default: 60)
        max_retries: Maximum number of retry attempts (default: 3)
        
    Returns:
        The text response from Gemini
        
    Raises:
        GeminiClientError: If the API call fails after all retries
    """
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise GeminiClientError("GEMINI_API_KEY environment variable is not set")
    
    # Create client with new library
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        raise GeminiClientError(f"Failed to initialize Gemini client: {str(e)}")
    
    # Retry logic with exponential backoff
    last_error: Optional[Exception] = None
    
    for attempt in range(max_retries):
        try:
            print(f"Calling Gemini API (attempt {attempt + 1}/{max_retries})...")
            
            # Make API call with timeout
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    client.models.generate_content,
                    model=model,
                    contents=prompt
                ),
                timeout=timeout
            )
            
            # Check if response has text
            if not response.text:
                raise GeminiClientError("Gemini API returned empty response")
            
            print(f"Gemini API call successful (response length: {len(response.text)} chars)")
            return response.text
            
        except asyncio.TimeoutError:
            last_error = GeminiClientError(f"Request timed out after {timeout} seconds")
            print(f"Attempt {attempt + 1} failed: Timeout")
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Don't retry on authentication errors
            if "api key" in error_msg or "authentication" in error_msg or "unauthorized" in error_msg:
                raise GeminiClientError(f"Invalid API key or authentication error: {str(e)}")
            
            # Don't retry on quota/rate limit errors
            if "quota" in error_msg or "rate limit" in error_msg or "429" in error_msg:
                raise GeminiClientError(f"Rate limit or quota exceeded: {str(e)}")
            
            # Handle safety filter blocks
            if "safety" in error_msg or "blocked" in error_msg:
                raise GeminiClientError(f"Content blocked by safety filters: {str(e)}")
            
            last_error = GeminiClientError(f"Unexpected error: {str(e)}")
            print(f"Attempt {attempt + 1} failed: {str(e)}")
        
        # Wait before retrying (exponential backoff)
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"Waiting {wait_time}s before retry...")
            await asyncio.sleep(wait_time)
    
    # All retries failed
    raise GeminiClientError(
        f"Failed to get response from Gemini after {max_retries} attempts. "
        f"Last error: {str(last_error)}"
    )


async def ask_gemini_batch(prompts: list[str], model: str = "gemini-2.5-flash") -> list[str]:
    """
    Send multiple prompts to Gemini in parallel.
    
    Args:
        prompts: List of prompts to send
        model: The Gemini model to use
        
    Returns:
        List of responses in the same order as prompts
        
    Raises:
        GeminiClientError: If any API call fails
    """
    tasks = [ask_gemini(prompt, model=model) for prompt in prompts]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Test the Gemini client
    async def test_gemini_client():
        """Test function for Gemini API client."""
        print("Testing Gemini API client...\n")
        
        # Check environment variables
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  GEMINI_API_KEY not set. Please set it in .env file")
            print("   Get your API key from: https://aistudio.google.com/app/apikey")
            print("   New keys start with 'AQ.' (e.g., AQ.Ab8RN6IxkvazkDr16g5K...)")
            print("   Old keys start with 'AIza' (both formats are supported)")
            return
        
        # Validate API key format
        if not (api_key.startswith('AQ.') or api_key.startswith('AIza')):
            print("⚠️  Warning: API key doesn't match expected format")
            print("   Expected: Starts with 'AQ.' (new) or 'AIza' (old)")
            print("   Got: Starts with '{}'".format(api_key[:4]))
            print("   Proceeding anyway, but this may cause authentication errors...")
        
        # Test single prompt
        test_prompt = "Explain what FastAPI is in one sentence."
        
        try:
            print(f"Sending test prompt: '{test_prompt}'\n")
            response = await ask_gemini(test_prompt)
            print(f"✅ Success! Response:\n{response}\n")
            
        except GeminiClientError as e:
            print(f"❌ Error: {e}\n")
        
        # Test batch prompts
        batch_prompts = [
            "What is Python?",
            "What is JavaScript?",
            "What is TypeScript?"
        ]
        
        try:
            print(f"Sending {len(batch_prompts)} prompts in parallel...\n")
            responses = await ask_gemini_batch(batch_prompts)
            print(f"✅ Success! Got {len(responses)} responses\n")
            for i, (prompt, response) in enumerate(zip(batch_prompts, responses)):
                print(f"{i+1}. {prompt}")
                print(f"   Response: {response[:100]}...\n")
                
        except GeminiClientError as e:
            print(f"❌ Error: {e}\n")
    
    # Run test
    asyncio.run(test_gemini_client())

# Made with Gemini
