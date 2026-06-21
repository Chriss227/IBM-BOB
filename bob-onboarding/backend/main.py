"""FastAPI backend for Repo Accelerate."""
import asyncio
import json
from typing import Literal
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl, field_validator
import logging

try:
    from .repo_reader import clone_and_read, RepoReaderError
    from .gemini_client import ask_gemini, GeminiClientError
    from .prompt_templates import (
        create_architecture_prompt,
        create_flows_prompt,
        create_guide_prompt,
    )
except ImportError:  # Support `uvicorn main:app` from the backend directory.
    from repo_reader import clone_and_read, RepoReaderError
    from gemini_client import ask_gemini, GeminiClientError
    from prompt_templates import (
        create_architecture_prompt,
        create_flows_prompt,
        create_guide_prompt,
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Repo Accelerate API",
    description="Generate architecture maps, system flows, and onboarding guides for public GitHub repositories.",
    version="3.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # Alternative port
        "https://ibm-bob-zeta.vercel.app",  # Vercel production
        "https://*.vercel.app",  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class AnalyzeRequest(BaseModel):
    """Request model for repository analysis."""
    url: HttpUrl
    language: Literal["en", "es"] = "en"

    @field_validator("url")
    @classmethod
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
    language: Literal["en", "es"]


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
        version="3.0.0"
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
    3. Sends three parallel requests to Gemini AI
    4. Returns the combined analysis
    
    Args:
        request: AnalyzeRequest with repository URL
        
    Returns:
        AnalyzeResponse with architecture, flows, and guide
        
    Raises:
        HTTPException: 400 for invalid URLs, 500 for processing errors
    """
    repo_url = str(request.url)
    language = request.language
    logger.info("Starting analysis for repository: %s (language=%s)", repo_url, language)
    
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
        logger.info("Creating analysis prompts...")
        architecture_prompt = create_architecture_prompt(file_contents, language)
        flows_prompt = create_flows_prompt(file_contents, language)
        guide_prompt = create_guide_prompt(file_contents, language)
        
        # Step 3: Call Gemini AI in parallel
        logger.info("Calling Gemini AI (3 parallel requests)...")
        architecture_raw, flows_raw, guide_raw = await asyncio.gather(
            ask_gemini(architecture_prompt),
            ask_gemini(flows_prompt),
            ask_gemini(guide_prompt)
        )
        logger.info("Gemini AI analysis complete")
        
        # Step 4: Parse and validate responses
        logger.info("Parsing Gemini responses...")
        
        # Parse architecture (should be plain Mermaid)
        architecture_mermaid = architecture_raw.strip()
        
        # Clean up Mermaid if Gemini added markdown fences
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
            # Clean up JSON if Gemini added markdown fences
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
            fallback = {
                "en": {
                    "name": "Flow analysis unavailable",
                    "description": "The structured flow response could not be parsed.",
                    "step": "Run the analysis again or review the repository manually.",
                },
                "es": {
                    "name": "Análisis de flujos no disponible",
                    "description": "No se pudo interpretar la respuesta estructurada de flujos.",
                    "step": "Ejecuta el análisis nuevamente o revisa el repositorio manualmente.",
                },
            }[language]
            flows = [
                FlowItem(
                    name=fallback["name"],
                    description=fallback["description"],
                    steps=[fallback["step"]],
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
            files_analyzed=files_count,
            language=language
        )
        
    except RepoReaderError as e:
        logger.error(f"Repository reading error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read repository: {str(e)}"
        )
    
    except GeminiClientError as e:
        logger.error(f"Gemini AI error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get response from Gemini AI: {str(e)}"
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
    
    logger.info("Starting Repo Accelerate backend...")
    logger.info("API documentation available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
