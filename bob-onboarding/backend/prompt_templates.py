"""
Prompt templates for IBM Bob AI to analyze repository structure and generate documentation.
"""


def create_architecture_prompt(file_contents: dict) -> str:
    """
    Create a prompt for Bob to generate a Mermaid architecture diagram.
    
    Args:
        file_contents: Dictionary mapping file paths to their contents
        
    Returns:
        Formatted prompt string for architecture analysis
    """
    # Format file contents for the prompt
    files_text = "\n\n".join([
        f"FILE: {path}\n{content[:2000]}"  # Limit each file to 2000 chars in prompt
        for path, content in list(file_contents.items())[:50]  # Limit to first 50 files
    ])
    
    prompt = f"""Analyze this codebase and create a Mermaid architecture diagram showing the main modules and their relationships.

CODEBASE:
{files_text}

INSTRUCTIONS:
- Return ONLY a valid Mermaid diagram using 'graph LR' syntax
- Show the main modules/components (5-10 maximum)
- Show key relationships between modules with arrows
- Use clear, concise labels
- Do NOT include any markdown code fences (no ```mermaid)
- Do NOT include any explanatory text
- Start directly with 'graph LR'

EXAMPLE FORMAT:
graph LR
    A[Frontend] --> B[API Gateway]
    B --> C[Database]
    B --> D[Auth Service]
    D --> C

Return only the Mermaid diagram code, nothing else."""
    
    return prompt


def create_flows_prompt(file_contents: dict) -> str:
    """
    Create a prompt for Bob to identify key system flows.
    
    Args:
        file_contents: Dictionary mapping file paths to their contents
        
    Returns:
        Formatted prompt string for flow analysis
    """
    # Format file contents for the prompt
    files_text = "\n\n".join([
        f"FILE: {path}\n{content[:2000]}"
        for path, content in list(file_contents.items())[:50]
    ])
    
    prompt = f"""Analyze this codebase and identify the 3 most important user/system flows.

CODEBASE:
{files_text}

INSTRUCTIONS:
- Identify the 3 most critical flows (e.g., user authentication, data processing, API request handling)
- For each flow, provide: name, description, steps, and relevant files
- Return ONLY valid JSON in this exact format
- Do NOT include markdown code fences
- Do NOT include any explanatory text
- Each flow should have 3-5 steps maximum

REQUIRED JSON FORMAT:
{{
  "flows": [
    {{
      "name": "User Authentication Flow",
      "description": "How users log in and get authenticated",
      "steps": [
        "User submits credentials to /login endpoint",
        "Server validates credentials against database",
        "JWT token is generated and returned"
      ],
      "files": ["auth.py", "models/user.py", "routes/login.py"]
    }}
  ]
}}

Return only the JSON object, nothing else."""
    
    return prompt


def create_guide_prompt(file_contents: dict) -> str:
    """
    Create a prompt for Bob to generate an onboarding guide.
    
    Args:
        file_contents: Dictionary mapping file paths to their contents
        
    Returns:
        Formatted prompt string for guide generation
    """
    # Format file contents for the prompt
    files_text = "\n\n".join([
        f"FILE: {path}\n{content[:2000]}"
        for path, content in list(file_contents.items())[:50]
    ])
    
    prompt = f"""Analyze this codebase and create a comprehensive onboarding guide for new developers.

CODEBASE:
{files_text}

INSTRUCTIONS:
Create a guide with these EXACT sections in markdown format:

## 1. What does this project do?
(Maximum 3 sentences explaining the project's purpose)

## 2. How to run it locally
(Step-by-step instructions with exact commands)

## 3. The 5 most important files
(List each file with its path and explain why it matters)

## 4. Gotchas and non-obvious things
(Things a new developer should know that aren't obvious from the code)

## 5. Where to start for your first contribution
(Concrete suggestions for making a first code contribution)

REQUIREMENTS:
- Use markdown formatting
- Be specific and actionable
- Include actual file paths and command examples
- Keep it concise but informative
- Focus on practical information

Return the complete markdown guide."""
    
    return prompt


# Template constants for easy access
PROMPT_ARCHITECTURE = create_architecture_prompt
PROMPT_FLOWS = create_flows_prompt
PROMPT_GUIDE = create_guide_prompt


if __name__ == "__main__":
    # Test prompt generation
    sample_files = {
        "main.py": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}",
        "models.py": "from pydantic import BaseModel\nclass User(BaseModel):\n    name: str\n    email: str",
        "README.md": "# My Project\nThis is a sample project."
    }
    
    print("=" * 80)
    print("ARCHITECTURE PROMPT")
    print("=" * 80)
    print(create_architecture_prompt(sample_files))
    
    print("\n" + "=" * 80)
    print("FLOWS PROMPT")
    print("=" * 80)
    print(create_flows_prompt(sample_files))
    
    print("\n" + "=" * 80)
    print("GUIDE PROMPT")
    print("=" * 80)
    print(create_guide_prompt(sample_files))

# Made with Bob
