"""Prompt templates for Repo Accelerate repository analysis."""

from typing import Literal

Language = Literal["en", "es"]

LANGUAGE_NAMES = {"en": "English", "es": "Spanish"}


def _format_files(file_contents: dict) -> str:
    return "\n\n".join(
        f"FILE: {path}\n{content[:2000]}"
        for path, content in list(file_contents.items())[:50]
    )


def create_architecture_prompt(file_contents: dict, language: Language = "en") -> str:
    files_text = _format_files(file_contents)
    output_language = LANGUAGE_NAMES[language]
    return f"""Analyze this codebase and create a focused Mermaid architecture diagram.

CODEBASE:
{files_text}

OUTPUT LANGUAGE: {output_language}

INSTRUCTIONS:
- Return ONLY valid Mermaid syntax starting with `flowchart LR`
- Use 5 to 10 main modules or components
- Use short, meaningful node labels written in {output_language}
- Keep technical product names, file names, framework names, and protocols unchanged
- Show only important dependencies with arrows
- Use simple rectangular nodes: A[Short label]
- Do not use HTML, Markdown, icons, emojis, comments, frontmatter, styles, or click handlers
- Do not use subgraphs, custom classes, braces, quotes, or multiline labels
- Do not include Markdown fences or explanatory text

EXAMPLE:
flowchart LR
    A[Frontend] --> B[API]
    B --> C[Services]
    C --> D[Database]

Return only the Mermaid diagram."""


def create_flows_prompt(file_contents: dict, language: Language = "en") -> str:
    files_text = _format_files(file_contents)
    output_language = LANGUAGE_NAMES[language]
    return f"""Analyze this codebase and identify the three most important user or system flows.

CODEBASE:
{files_text}

OUTPUT LANGUAGE: {output_language}

INSTRUCTIONS:
- Write every user-facing name, description, and step in {output_language}
- Keep file paths, API routes, identifiers, and technical names unchanged
- Return ONLY valid JSON using the exact schema below
- Include exactly three flows when the repository contains enough information
- Keep each flow to three to five concise steps
- Do not include Markdown fences or explanatory text

REQUIRED JSON FORMAT:
{{
  "flows": [
    {{
      "name": "Flow name",
      "description": "What this flow accomplishes",
      "steps": ["First concrete step", "Second concrete step", "Third concrete step"],
      "files": ["path/to/file.py"]
    }}
  ]
}}

Return only the JSON object."""


def create_guide_prompt(file_contents: dict, language: Language = "en") -> str:
    files_text = _format_files(file_contents)
    output_language = LANGUAGE_NAMES[language]
    sections = {
        "en": [
            "## 1. What does this project do?",
            "## 2. How to run it locally",
            "## 3. The 5 most important files",
            "## 4. Gotchas and non-obvious things",
            "## 5. Where to start for your first contribution",
        ],
        "es": [
            "## 1. ¿Qué hace este proyecto?",
            "## 2. Cómo ejecutarlo localmente",
            "## 3. Los 5 archivos más importantes",
            "## 4. Detalles y aspectos poco evidentes",
            "## 5. Dónde comenzar tu primera contribución",
        ],
    }[language]
    section_list = "\n\n".join(sections)
    return f"""Analyze this codebase and create a concise developer onboarding guide.

CODEBASE:
{files_text}

OUTPUT LANGUAGE: {output_language}

Use these exact Markdown section headings:

{section_list}

REQUIREMENTS:
- Write all explanatory content in {output_language}
- Keep commands, code, file paths, environment variables, and technical names unchanged
- Include concrete commands only when supported by repository evidence
- Explain why each important file matters
- Highlight non-obvious setup or architecture details
- Suggest one realistic first contribution
- Use Markdown and remain concise and actionable

Return only the complete Markdown guide."""


PROMPT_ARCHITECTURE = create_architecture_prompt
PROMPT_FLOWS = create_flows_prompt
PROMPT_GUIDE = create_guide_prompt
