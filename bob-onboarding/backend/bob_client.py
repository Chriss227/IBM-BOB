"""
IBM Bob API client with retry logic and error handling.
"""
import os
import asyncio
import httpx
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables from project root
# Get the project root directory (2 levels up from this file)
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)


async def get_iam_token(api_key: str) -> str:
    """
    Get IBM Cloud IAM access token from API key.
    
    Args:
        api_key: IBM Cloud API key
        
    Returns:
        IAM access token
        
    Raises:
        BobClientError: If token generation fails
    """
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(iam_url, headers=headers, data=data)
            
            if response.status_code != 200:
                raise Exception(f"IAM token request failed: {response.status_code} - {response.text}")
            
            token_data = response.json()
            return token_data["access_token"]
    except Exception as e:
        from bob_client import BobClientError
        raise BobClientError(f"Failed to get IAM token: {str(e)}")


class BobClientError(Exception):
    """Custom exception for Bob API client errors."""
    pass


async def ask_bob(
    prompt: str,
    model: str = "bob-v1",
    timeout: int = 60,
    max_retries: int = 3
) -> str:
    """
    Send a prompt to IBM Bob API and get the response.
    
    This function implements:
    - Exponential backoff retry logic (3 attempts)
    - 60 second timeout per request
    - Proper error handling and logging
    - Environment variable configuration
    
    Args:
        prompt: The prompt to send to Bob
        model: The Bob model to use (default: "bob-v1")
        timeout: Request timeout in seconds (default: 60)
        max_retries: Maximum number of retry attempts (default: 3)
        
    Returns:
        The text response from Bob
        
    Raises:
        BobClientError: If the API call fails after all retries
    """
    # Get configuration from environment variables
    api_endpoint = os.getenv('BOB_API_ENDPOINT')
    api_key = os.getenv('BOB_API_KEY')
    
    if not api_endpoint:
        raise BobClientError("BOB_API_ENDPOINT environment variable is not set")
    
    if not api_key:
        raise BobClientError("BOB_API_KEY environment variable is not set")
    
    # Get IAM token from API key
    try:
        iam_token = await get_iam_token(api_key)
    except Exception as e:
        raise BobClientError(f"Failed to authenticate with IBM Cloud: {str(e)}")
    
    # Prepare request with IBM Cloud IAM authentication
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    payload = {
        'input': prompt,
        'parameters': {
            'max_new_tokens': 2000,
            'temperature': 0.7
        }
    }
    
    # Retry logic with exponential backoff
    last_error: Optional[Exception] = None
    
    for attempt in range(max_retries):
        try:
            print(f"Calling Bob API (attempt {attempt + 1}/{max_retries})...")
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    api_endpoint,
                    json=payload,
                    headers=headers
                )
                
                # Check for HTTP errors
                if response.status_code == 401:
                    raise BobClientError("Invalid API key (401 Unauthorized)")
                elif response.status_code == 429:
                    raise BobClientError("Rate limit exceeded (429 Too Many Requests)")
                elif response.status_code >= 500:
                    raise BobClientError(f"Bob API server error ({response.status_code})")
                elif response.status_code != 200:
                    raise BobClientError(
                        f"Bob API returned status {response.status_code}: {response.text}"
                    )
                
                # Parse response
                try:
                    response_data = response.json()
                except Exception as e:
                    raise BobClientError(f"Failed to parse Bob API response as JSON: {str(e)}")
                
                # Extract text from response (Watson Orchestrate format)
                # Try different response formats
                text = None
                
                if 'results' in response_data and len(response_data['results']) > 0:
                    # watsonx.ai format
                    text = response_data['results'][0].get('generated_text', '')
                elif 'generated_text' in response_data:
                    # Alternative format
                    text = response_data['generated_text']
                elif 'text' in response_data:
                    # Original format
                    text = response_data['text']
                elif 'output' in response_data:
                    # Watson Orchestrate format
                    text = response_data['output']
                else:
                    raise BobClientError(
                        f"Bob API response missing expected fields. Response: {response_data}"
                    )
                
                if not text or not isinstance(text, str):
                    raise BobClientError("Bob API returned empty or invalid text response")
                
                print(f"Bob API call successful (response length: {len(text)} chars)")
                return text
                
        except httpx.TimeoutException as e:
            last_error = BobClientError(f"Request timed out after {timeout} seconds")
            print(f"Attempt {attempt + 1} failed: Timeout")
            
        except httpx.NetworkError as e:
            last_error = BobClientError(f"Network error: {str(e)}")
            print(f"Attempt {attempt + 1} failed: Network error")
            
        except BobClientError as e:
            # Don't retry on authentication or client errors
            if "401" in str(e) or "Invalid API key" in str(e):
                raise
            last_error = e
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            
        except Exception as e:
            last_error = BobClientError(f"Unexpected error: {str(e)}")
            print(f"Attempt {attempt + 1} failed: Unexpected error")
        
        # Wait before retrying (exponential backoff)
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"Waiting {wait_time}s before retry...")
            await asyncio.sleep(wait_time)
    
    # All retries failed
    raise BobClientError(
        f"Failed to get response from Bob after {max_retries} attempts. "
        f"Last error: {str(last_error)}"
    )


async def ask_bob_batch(prompts: list[str], model: str = "bob-v1") -> list[str]:
    """
    Send multiple prompts to Bob in parallel.
    
    Args:
        prompts: List of prompts to send
        model: The Bob model to use
        
    Returns:
        List of responses in the same order as prompts
        
    Raises:
        BobClientError: If any API call fails
    """
    tasks = [ask_bob(prompt, model=model) for prompt in prompts]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Test the Bob client
    async def test_bob_client():
        """Test function for Bob API client."""
        print("Testing Bob API client...\n")
        
        # Check environment variables
        if not os.getenv('BOB_API_ENDPOINT'):
            print("⚠️  BOB_API_ENDPOINT not set. Please set it in .env file")
            return
        
        if not os.getenv('BOB_API_KEY'):
            print("⚠️  BOB_API_KEY not set. Please set it in .env file")
            return
        
        # Test single prompt
        test_prompt = "Explain what FastAPI is in one sentence."
        
        try:
            print(f"Sending test prompt: '{test_prompt}'\n")
            response = await ask_bob(test_prompt)
            print(f"✅ Success! Response:\n{response}\n")
            
        except BobClientError as e:
            print(f"❌ Error: {e}\n")
        
        # Test batch prompts
        batch_prompts = [
            "What is Python?",
            "What is JavaScript?",
            "What is TypeScript?"
        ]
        
        try:
            print(f"Sending {len(batch_prompts)} prompts in parallel...\n")
            responses = await ask_bob_batch(batch_prompts)
            print(f"✅ Success! Got {len(responses)} responses\n")
            for i, (prompt, response) in enumerate(zip(batch_prompts, responses)):
                print(f"{i+1}. {prompt}")
                print(f"   Response: {response[:100]}...\n")
                
        except BobClientError as e:
            print(f"❌ Error: {e}\n")
    
    # Run test
    asyncio.run(test_bob_client())

# Made with Bob
