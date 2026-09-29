from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.templating import Jinja2Templates

from .schemas import PromptRequest
from .services.comic_service import ComicService


router = APIRouter()

templates = Jinja2Templates(directory="./templates")

service = ComicService()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


@router.post("/generate")
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
    photo: UploadFile | None = File(None),
):
    try:
        # Save uploaded photo if provided
        if photo and photo.filename:
            photo_path = "static/panels/uploaded_photo.jpg"

            with open(photo_path, "wb") as f:
                f.write(await photo.read())

        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        result = service.generate(data)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "comic": result.model_dump(),
            },
        )

    except Exception as exc:
        print("GENERATE ERROR:", repr(exc))

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(exc),
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):
    try:
        result = service.generate(payload)
        return result.model_dump()

    except Exception as exc:
        print("JSON GENERATE ERROR:", repr(exc))
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get("/export/{filename}")
async def export_success(
    request: Request,
    filename: str,
):
    pdf_url = f"/static/exports/{filename}"

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "request": request,
            "pdf_url": pdf_url,
            "filename": filename,
        },
    )


@router.get("/test-image")
async def test_image(
    prompt: str = (
        "A friendly fox in an enchanted forest, "
        "colorful anime comic illustration"
    ),
):
    try:
        path = service.image_generator.generate_image(
            prompt,
            panel_number=0,
        )

        return {
            "status": "ok",
            "image_path": path,
        }

    except Exception as exc:
        print("IMAGE ERROR:", repr(exc))
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc