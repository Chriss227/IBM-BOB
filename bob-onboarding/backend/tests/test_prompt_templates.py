"""
Unit tests for prompt template generation.
Tests architecture, flows, and guide prompt creation.
"""
import pytest
from backend.prompt_templates import (
    create_architecture_prompt,
    create_flows_prompt,
    create_guide_prompt
)


@pytest.fixture
def sample_file_contents():
    """Sample file contents for testing."""
    return {
        "main.py": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}",
        "models.py": "from pydantic import BaseModel\nclass User(BaseModel):\n    name: str\n    email: str",
        "README.md": "# My Project\nThis is a sample project for testing.",
        "config.py": "DATABASE_URL = 'postgresql://localhost/db'\nSECRET_KEY = 'secret'"
    }


def test_create_architecture_prompt_contains_mermaid_instructions(sample_file_contents):
    """Test that architecture prompt includes Mermaid diagram instructions."""
    prompt = create_architecture_prompt(sample_file_contents)
    
    assert "Mermaid" in prompt
    assert "graph LR" in prompt
    assert "architecture diagram" in prompt.lower()
    assert "modules" in prompt.lower()


def test_create_architecture_prompt_includes_file_contents(sample_file_contents):
    """Test that architecture prompt includes file contents."""
    prompt = create_architecture_prompt(sample_file_contents)
    
    assert "main.py" in prompt
    assert "FastAPI" in prompt
    assert "models.py" in prompt


def test_create_architecture_prompt_file_truncation():
    """Test that files are truncated to 2000 chars in prompt."""
    large_content = "x" * 5000
    files = {"large.py": large_content}
    
    prompt = create_architecture_prompt(files)
    
    # The prompt should contain truncated content (2000 chars max per file)
    assert large_content[:2000] in prompt
    assert large_content[2001:] not in prompt


def test_create_architecture_prompt_max_50_files():
    """Test that prompt limits to first 50 files."""
    # Create 60 files
    files = {f"file{i}.py": f"content{i}" for i in range(60)}
    
    prompt = create_architecture_prompt(files)
    
    # Should include first 50 files
    assert "file0.py" in prompt
    assert "file49.py" in prompt
    # Should not include files beyond 50
    assert "file50.py" not in prompt
    assert "file59.py" not in prompt


def test_create_architecture_prompt_no_markdown_fences(sample_file_contents):
    """Test that prompt instructs not to use markdown code fences."""
    prompt = create_architecture_prompt(sample_file_contents)
    
    assert "Do NOT include any markdown code fences" in prompt
    assert "no ```mermaid" in prompt.lower()


def test_create_flows_prompt_contains_json_format(sample_file_contents):
    """Test that flows prompt specifies JSON format."""
    prompt = create_flows_prompt(sample_file_contents)
    
    assert "JSON" in prompt
    assert '"flows"' in prompt
    assert '"name"' in prompt
    assert '"description"' in prompt
    assert '"steps"' in prompt
    assert '"files"' in prompt


def test_create_flows_prompt_requests_three_flows(sample_file_contents):
    """Test that flows prompt requests 3 flows."""
    prompt = create_flows_prompt(sample_file_contents)
    
    assert "3 most important" in prompt or "3 most critical" in prompt


def test_create_flows_prompt_includes_file_contents(sample_file_contents):
    """Test that flows prompt includes file contents."""
    prompt = create_flows_prompt(sample_file_contents)
    
    assert "main.py" in prompt
    assert "models.py" in prompt


def test_create_flows_prompt_example_format(sample_file_contents):
    """Test that flows prompt includes example format."""
    prompt = create_flows_prompt(sample_file_contents)
    
    assert "User Authentication Flow" in prompt or "authentication" in prompt.lower()
    assert "REQUIRED JSON FORMAT" in prompt or "JSON FORMAT" in prompt


def test_create_guide_prompt_contains_five_sections(sample_file_contents):
    """Test that guide prompt specifies 5 sections."""
    prompt = create_guide_prompt(sample_file_contents)
    
    assert "## 1. What does this project do?" in prompt
    assert "## 2. How to run it locally" in prompt
    assert "## 3. The 5 most important files" in prompt
    assert "## 4. Gotchas and non-obvious things" in prompt
    assert "## 5. Where to start for your first contribution" in prompt


def test_create_guide_prompt_markdown_format(sample_file_contents):
    """Test that guide prompt requests markdown format."""
    prompt = create_guide_prompt(sample_file_contents)
    
    assert "markdown" in prompt.lower()
    assert "##" in prompt  # Markdown headers


def test_create_guide_prompt_includes_file_contents(sample_file_contents):
    """Test that guide prompt includes file contents."""
    prompt = create_guide_prompt(sample_file_contents)
    
    assert "main.py" in prompt
    assert "README.md" in prompt


def test_create_guide_prompt_actionable_instructions(sample_file_contents):
    """Test that guide prompt requests actionable content."""
    prompt = create_guide_prompt(sample_file_contents)
    
    assert "specific" in prompt.lower() or "actionable" in prompt.lower()
    assert "step-by-step" in prompt.lower() or "exact commands" in prompt.lower()


def test_all_prompts_handle_empty_files():
    """Test that all prompts handle empty file dictionary."""
    empty_files = {}
    
    # Should not raise exceptions
    arch_prompt = create_architecture_prompt(empty_files)
    flows_prompt = create_flows_prompt(empty_files)
    guide_prompt = create_guide_prompt(empty_files)
    
    assert isinstance(arch_prompt, str)
    assert isinstance(flows_prompt, str)
    assert isinstance(guide_prompt, str)
    assert len(arch_prompt) > 0
    assert len(flows_prompt) > 0
    assert len(guide_prompt) > 0


def test_prompts_handle_special_characters():
    """Test that prompts handle special characters in file contents."""
    files = {
        "test.py": "# Special chars: <>&\"'\n{\"key\": \"value\"}\nprint('test')"
    }
    
    arch_prompt = create_architecture_prompt(files)
    flows_prompt = create_flows_prompt(files)
    guide_prompt = create_guide_prompt(files)
    
    # Should include the content without errors
    assert "Special chars" in arch_prompt
    assert "Special chars" in flows_prompt
    assert "Special chars" in guide_prompt


def test_architecture_prompt_structure():
    """Test the overall structure of architecture prompt."""
    files = {"test.py": "content"}
    prompt = create_architecture_prompt(files)
    
    # Should have clear sections
    assert "CODEBASE:" in prompt
    assert "INSTRUCTIONS:" in prompt
    assert "EXAMPLE FORMAT:" in prompt


def test_flows_prompt_structure():
    """Test the overall structure of flows prompt."""
    files = {"test.py": "content"}
    prompt = create_flows_prompt(files)
    
    # Should have clear sections
    assert "CODEBASE:" in prompt
    assert "INSTRUCTIONS:" in prompt
    assert "REQUIRED JSON FORMAT:" in prompt or "JSON FORMAT:" in prompt


def test_guide_prompt_structure():
    """Test the overall structure of guide prompt."""
    files = {"test.py": "content"}
    prompt = create_guide_prompt(files)
    
    # Should have clear sections
    assert "CODEBASE:" in prompt
    assert "INSTRUCTIONS:" in prompt
    assert "REQUIREMENTS:" in prompt

# Made with Bob
