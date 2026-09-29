import json

from ..schemas import (
    OutlineResponse,
    PromptRequest,
    StoryResponse,
)
from .gemini_client import get_gemini_client


def generate_story(
    request: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:

    from google.genai import types

    client = get_gemini_client()

    outline_text = outline.model_dump_json()

    prompt = f"""
Create the complete story for a 5-panel comic.

User idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Approved outline:
{outline_text}

Requirements:
1. Create exactly 5 panels.
2. Follow the outline closely.
3. Keep the character and setting consistent.
4. Give each panel a title.
5. Add scene description.
6. Add a short caption.
7. Add narration.
8. Add dialogue.
9. Create a detailed image prompt.
10. Do not put text inside generated images.
11. Keep the story suitable for a general audience.
"""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
            response_schema=StoryResponse,
        ),
    )

    raw = response.text

    try:
        return StoryResponse.model_validate_json(raw)

    except Exception:
        cleaned = raw.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0].strip()

        return StoryResponse.model_validate(
            json.loads(cleaned)
        )