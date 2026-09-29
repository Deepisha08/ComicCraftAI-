from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate 5-panel AI comics using Gemini and Stable Diffusion.",
    version="1.0.0",
)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

# Routes
app.include_router(router)


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "ok",
        "service": "ComicCraft",
    }