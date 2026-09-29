from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import ImageGenerator
from .layout_builder import build_comic_layout
from .exporters import save_pdf
from ..schemas import ComicResult, PromptRequest


class ComicService:

    def __init__(self):
        self.image_generator = ImageGenerator()

    def generate(self, request: PromptRequest) -> ComicResult:

        # Step 1: Generate 5-panel outline
        outline = generate_outline(request)

        # Step 2: Generate complete story
        story = generate_story(request, outline)

        # Step 3: Generate AI image for every panel
        image_paths = []

        for panel in story.panels:
            image_path = self.image_generator.generate_image(
                panel.image_prompt,
                panel.panel_number,
            )

            image_paths.append(image_path)

        # Step 4: Combine story + images
        layout = build_comic_layout(
            story,
            image_paths,
        )

        # Comic title
        title = f"{request.character_name}'s Adventure"

        # Step 5: Create PDF
        pdf_path = save_pdf(
            title,
            layout,
        )

        # Step 6: Return complete comic result
        return ComicResult(
            title=title,
            panels=layout,
            pdf_path=pdf_path,
        )