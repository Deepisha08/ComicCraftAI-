import json

from ..config import get_settings
from ..schemas import (
    OutlineResponse,
    PromptRequest,
)
from .gemini_client import get_gemini_client


def generate_outline(
    request: PromptRequest,
) -> OutlineResponse:

    from google.genai import types

    settings = get_settings()

    client = get_gemini_client()

    prompt = f"""
Create a cohesive 5-panel comic outline.

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

Requirements:

1. Create exactly 5 panels.
2. Keep the same protagonist throughout.
3. Keep the setting consistent.
4. Give every panel a short title.
5. scene_description must describe what happens visually.
6. image_prompt must be detailed enough for an image-generation model.
7. Do not put text inside generated images.
8. Make the story suitable for a general audience.
9. Make the five panels form one continuous story.
"""

    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.8,
            response_mime_type="application/json",
            response_schema=OutlineResponse,
        ),
    )

    raw = response.text

    try:
        return OutlineResponse.model_validate_json(raw)

    except Exception:
        cleaned = raw.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.split(
                "\n",
                1,
            )[1]

            cleaned = cleaned.rsplit(
                "```",
                1,
            )[0]

        return OutlineResponse.model_validate(
            json.loads(cleaned)
        )