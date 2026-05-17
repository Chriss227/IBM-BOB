"""
FastAPI backend for Bob Onboarding Accelerator.
Analyzes GitHub repositories using IBM Bob AI.
"""
import asyncio
import json
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl, validator
import logging

from repo_reader import clone_and_read, RepoReaderError
from bob_client import ask_bob, BobClientError
from prompt_templates import (
    create_architecture_prompt,
    create_flows_prompt,
    create_guide_prompt
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Bob Onboarding Accelerator",
    description="Analyze GitHub repositories in under 5 minutes using IBM Bob AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # Alternative port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class AnalyzeRequest(BaseModel):
    """Request model for repository analysis."""
    url: HttpUrl
    
    @validator('url')
    def validate_github_url(cls, v):
        """Ensure URL is a GitHub repository."""
        url_str = str(v)
        if not url_str.startswith('https://github.com/'):
            raise ValueError('URL must be a GitHub repository (https://github.com/...)')
        return v


class FlowItem(BaseModel):
    """Model for a single flow."""
    name: str
    description: str
    steps: list[str]
    files: list[str]


class AnalyzeResponse(BaseModel):
    """Response model for repository analysis."""
    architecture_mermaid: str
    flows: list[FlowItem]
    guide: str
    repository_url: str
    files_analyzed: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    version: str


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str
    detail: str


# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns the service status and version.
    """
    return HealthResponse(
        status="ok",
        version="1.0.0"
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze a GitHub repository and generate:
    - Architecture diagram (Mermaid)
    - Key system flows (JSON)
    - Onboarding guide (Markdown)
    
    This endpoint:
    1. Clones the repository
    2. Reads all relevant files
    3. Sends three parallel requests to Bob AI
    4. Returns the combined analysis
    
    Args:
        request: AnalyzeRequest with repository URL
        
    Returns:
        AnalyzeResponse with architecture, flows, and guide
        
    Raises:
        HTTPException: 400 for invalid URLs, 500 for processing errors
    """
    repo_url = str(request.url)
    logger.info(f"Starting analysis for repository: {repo_url}")
    
    try:
        # Step 1: Clone and read repository
        logger.info("Cloning repository...")
        file_contents = clone_and_read(repo_url)
        files_count = len(file_contents)
        logger.info(f"Successfully read {files_count} files")
        
        if files_count == 0:
            raise HTTPException(
                status_code=400,
                detail="No readable files found in repository"
            )
        
        # Step 2: Create prompts
        logger.info("Creating prompts for Bob...")
        architecture_prompt = create_architecture_prompt(file_contents)
        flows_prompt = create_flows_prompt(file_contents)
        guide_prompt = create_guide_prompt(file_contents)
        
        # Step 3: Call Bob AI in parallel
        logger.info("Calling Bob AI (3 parallel requests)...")
        architecture_raw, flows_raw, guide_raw = await asyncio.gather(
            ask_bob(architecture_prompt),
            ask_bob(flows_prompt),
            ask_bob(guide_prompt)
        )
        logger.info("Bob AI analysis complete")
        
        # Step 4: Parse and validate responses
        logger.info("Parsing Bob responses...")
        
        # Parse architecture (should be plain Mermaid)
        architecture_mermaid = architecture_raw.strip()
        
        # Clean up Mermaid if Bob added markdown fences
        if architecture_mermaid.startswith('```'):
            lines = architecture_mermaid.split('\n')
            # Remove first and last lines if they're markdown fences
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].startswith('```'):
                lines = lines[:-1]
            architecture_mermaid = '\n'.join(lines).strip()
        
        # Parse flows (should be JSON)
        try:
            # Clean up JSON if Bob added markdown fences
            flows_json = flows_raw.strip()
            if flows_json.startswith('```'):
                lines = flows_json.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].startswith('```'):
                    lines = lines[:-1]
                flows_json = '\n'.join(lines).strip()
            
            flows_data = json.loads(flows_json)
            
            if 'flows' not in flows_data:
                raise ValueError("Response missing 'flows' key")
            
            flows = [FlowItem(**flow) for flow in flows_data['flows']]
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.error(f"Failed to parse flows JSON: {str(e)}")
            logger.error(f"Raw flows response: {flows_raw[:500]}")
            # Provide fallback
            flows = [
                FlowItem(
                    name="Analysis Error",
                    description="Could not parse flow information from Bob's response",
                    steps=["Please try again or check the repository manually"],
                    files=[]
                )
            ]
        
        # Parse guide (should be Markdown)
        guide = guide_raw.strip()
        
        # Step 5: Return response
        logger.info("Analysis complete, returning results")
        return AnalyzeResponse(
            architecture_mermaid=architecture_mermaid,
            flows=flows,
            guide=guide,
            repository_url=repo_url,
            files_analyzed=files_count
        )
        
    except RepoReaderError as e:
        logger.error(f"Repository reading error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read repository: {str(e)}"
        )
    
    except BobClientError as e:
        logger.error(f"Bob AI error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get response from Bob AI: {str(e)}"
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested endpoint does not exist"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Bob Onboarding Accelerator backend...")
    logger.info("API documentation available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# Made with Bob
