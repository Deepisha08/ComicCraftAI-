from fastapi.testclient import TestClient

from app.main import app
from app.schemas import (
    PromptRequest,
    StoryResponse,
    PanelStory,
)
from app.services.layout_builder import (
    build_comic_layout,
)

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_prompt_validation():
    payload = PromptRequest(
        story_prompt="A fox explores a magical forest.",
        character_name="Luna",
        setting="forest",
        tone="funny",
        art_style="comic book",
    )

    assert payload.character_name == "Luna"


def test_layout_builder():
    story = StoryResponse(
        panels=[
            PanelStory(
                panel_number=i,
                title=f"Panel {i}",
                scene_description="A scene.",
                caption="Caption",
                narration="Narration",
                dialogue="Hello!",
                image_prompt="Comic illustration",
            )
            for i in range(1, 6)
        ]
    )

    image_paths = [
        f"/static/panels/panel_{i}.png"
        for i in range(1, 6)
    ]

    layout = build_comic_layout(
        story,
        image_paths,
    )

    assert len(layout) == 5
    assert layout[0].panel_number == 1