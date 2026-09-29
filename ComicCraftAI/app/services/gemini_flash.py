import json

from ..config import get_settings
from ..schemas import OutlineResponse, PromptRequest
from .gemini_client import get_gemini_client


def generate_outline(request: PromptRequest) -> OutlineResponse:
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

Return ONLY valid JSON.
Do not use Markdown.
Do not use ```.

Use exactly this JSON structure:

{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "Short title",
      "scene_description": "Visual description",
      "image_prompt": "Detailed image generation prompt"
    }},
    {{
      "panel_number": 2,
      "title": "Short title",
      "scene_description": "Visual description",
      "image_prompt": "Detailed image generation prompt"
    }},
    {{
      "panel_number": 3,
      "title": "Short title",
      "scene_description": "Visual description",
      "image_prompt": "Detailed image generation prompt"
    }},
    {{
      "panel_number": 4,
      "title": "Short title",
      "scene_description": "Visual description",
      "image_prompt": "Detailed image generation prompt"
    }},
    {{
      "panel_number": 5,
      "title": "Short title",
      "scene_description": "Visual description",
      "image_prompt": "Detailed image generation prompt"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
    )

    raw = response.text.strip()

    # Remove Markdown code fences if the model adds them.
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
        raw = raw.rsplit("```", 1)[0].strip()

    try:
        data = json.loads(raw)
        return OutlineResponse.model_validate(data)

    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(
            f"Gemini returned invalid comic outline JSON: {exc}\n"
            f"Response received:\n{raw}"
        ) from exc