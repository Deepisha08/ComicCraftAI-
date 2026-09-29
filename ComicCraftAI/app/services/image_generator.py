import os
from pathlib import Path

from huggingface_hub import InferenceClient

from ..config import get_settings


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PANELS_DIR = BASE_DIR / "static" / "panels"


class ImageGenerator:
    def __init__(self):
        self.settings = get_settings()

        PANELS_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = InferenceClient(
            provider="auto",
            api_key=self.settings.hf_api_key,
        )

        self.model = os.getenv(
            "DIFFUSION_MODEL",
            "black-forest-labs/FLUX.1-schnell",
        )

    def generate_image(
        self,
        prompt: str,
        panel_number: int,
    ) -> str:

        filename = f"panel_{panel_number}.png"
        output_path = PANELS_DIR / filename

        # Keep the generated image clean.
        # Story text, narration and dialogue will be shown
        # separately below the image in comic_preview.html.
        clean_prompt = (
            f"{prompt}. "
            "Create a clean comic-style illustration only. "
            "Do not include any text, words, letters, numbers, captions, "
            "dialogue, speech bubbles, subtitles, signs, labels, or writing "
            "inside the image. Leave the image completely text-free."
        )

        image = self.client.text_to_image(
            prompt=clean_prompt,
            model=self.model,
            width=512,
            height=512,
        )

        image.save(output_path)

        return f"/static/panels/{filename}"