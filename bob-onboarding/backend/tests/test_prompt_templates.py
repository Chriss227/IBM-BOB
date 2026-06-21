"""Tests for bilingual Repo Accelerate prompts."""

import pytest

from backend.prompt_templates import (
    create_architecture_prompt,
    create_flows_prompt,
    create_guide_prompt,
)


@pytest.fixture
def sample_files():
    return {
        "main.py": "from fastapi import FastAPI\napp = FastAPI()",
        "README.md": "# Example\nRun with uvicorn.",
    }


@pytest.mark.parametrize("language,name", [("en", "English"), ("es", "Spanish")])
def test_all_prompts_request_selected_language(sample_files, language, name):
    prompts = [
        create_architecture_prompt(sample_files, language),
        create_flows_prompt(sample_files, language),
        create_guide_prompt(sample_files, language),
    ]
    assert all(f"OUTPUT LANGUAGE: {name}" in prompt for prompt in prompts)
    assert all("main.py" in prompt for prompt in prompts)


def test_architecture_prompt_is_strict_and_focused(sample_files):
    prompt = create_architecture_prompt(sample_files, "en")
    assert "flowchart LR" in prompt
    assert "5 to 10" in prompt
    assert "Do not use HTML" in prompt
    assert "Do not include Markdown fences" in prompt


def test_flows_prompt_requires_json(sample_files):
    prompt = create_flows_prompt(sample_files, "es")
    assert '"flows"' in prompt
    assert '"steps"' in prompt
    assert "valid JSON" in prompt


def test_guide_uses_localized_exact_sections(sample_files):
    english = create_guide_prompt(sample_files, "en")
    spanish = create_guide_prompt(sample_files, "es")
    assert "## 1. What does this project do?" in english
    assert "## 1. ¿Qué hace este proyecto?" in spanish
    assert "## 5. Dónde comenzar tu primera contribución" in spanish


def test_prompts_bound_file_count_and_content_size():
    files = {f"file{i}.py": "x" * 5000 for i in range(60)}
    prompt = create_architecture_prompt(files)
    assert "file49.py" in prompt
    assert "file50.py" not in prompt
    assert "x" * 2000 in prompt
    assert "x" * 2001 not in prompt
