from google import genai

from ..config import get_settings


def get_gemini_client():
    settings = get_settings()

    return genai.Client(
        api_key=settings.gemini_api_key,
    )