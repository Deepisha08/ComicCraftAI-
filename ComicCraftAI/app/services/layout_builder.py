from typing import List

from ..schemas import (
    ComicPanel,
    StoryResponse,
)


def build_comic_layout(
    story: StoryResponse,
    image_paths: List[str],
) -> List[ComicPanel]:

    layout = []

    for panel, image_path in zip(
        story.panels,
        image_paths,
    ):
        layout.append(
            ComicPanel(
                panel_number=panel.panel_number,
                title=panel.title,
                image_path=image_path,
                scene_description=panel.scene_description,
                caption=panel.caption,
                narration=panel.narration,
                dialogue=panel.dialogue,
                image_prompt=panel.image_prompt,
            )
        )

    return layout