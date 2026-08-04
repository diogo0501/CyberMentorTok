from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.core.config import get_settings
from app.core.database import init_db
from app.api.v1.router import api_router

settings = get_settings()

VIDEO_OUTPUT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "video_pipeline", "output"))
BACKGROUNDS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "video_pipeline", "backgrounds"))

MEDIA_TYPES = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mkv": "video/x-matroska",
    ".mov": "video/quicktime",
    ".mp3": "audio/mpeg",
    ".ogg": "audio/ogg",
    ".opus": "audio/opus",
    ".json": "application/json",
}

CHARACTERS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "video_pipeline", "characters"))
SCALED_CHARS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "video_pipeline", "temp", "_scaled_chars"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    from app.core.database import async_session
    from app.services.knowledge_graph.seed import seed_knowledge_graph
    from app.services.knowledge_graph.seed_lessons import seed_lessons
    async with async_session() as db:
        await seed_knowledge_graph(db)
        await seed_lessons(db)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="TikTok-style cybersecurity education platform",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "version": settings.APP_VERSION, "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.api_route("/videos/{filename:path}", methods=["GET", "HEAD"])
async def serve_video(filename: str):
    """Serve video files from output directory.

    Supports both flat (output/filename.mp4) and nested (output/lesson_id/filename.webm)
    paths.
    """
    filepath = os.path.normpath(os.path.join(VIDEO_OUTPUT_DIR, filename))

    # Security: ensure resolved path is within output dir
    if not filepath.startswith(VIDEO_OUTPUT_DIR):
        raise HTTPException(status_code=403, detail="Forbidden")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Video not found")

    ext = os.path.splitext(filepath)[1].lower()
    media_type = MEDIA_TYPES.get(ext, "application/octet-stream")

    return FileResponse(filepath, media_type=media_type)


@app.api_route("/backgrounds", methods=["GET"])
async def list_backgrounds():
    """List available background videos."""
    if not os.path.isdir(BACKGROUNDS_DIR):
        return []
    files = []
    for f in sorted(os.listdir(BACKGROUNDS_DIR)):
        if f.lower().endswith((".mp4", ".mkv", ".webm", ".mov")):
            size = os.path.getsize(os.path.join(BACKGROUNDS_DIR, f))
            files.append({
                "name": f,
                "url": f"/backgrounds/{f}",
                "size_mb": round(size / (1024 * 1024), 1),
            })
    return files


@app.api_route("/backgrounds/{filename}", methods=["GET", "HEAD"])
async def serve_background(filename: str):
    """Serve a background video file."""
    filepath = os.path.normpath(os.path.join(BACKGROUNDS_DIR, filename))
    if not filepath.startswith(BACKGROUNDS_DIR):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Background not found")
    ext = os.path.splitext(filepath)[1].lower()
    media_type = MEDIA_TYPES.get(ext, "video/mp4")
    return FileResponse(filepath, media_type=media_type)


@app.api_route("/characters/{filename}", methods=["GET", "HEAD"])
async def serve_character(filename: str):
    """Serve character PNG images."""
    filepath = os.path.normpath(os.path.join(CHARACTERS_DIR, filename))
    if not filepath.startswith(CHARACTERS_DIR):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Character not found")
    return FileResponse(filepath, media_type="image/png")


@app.api_route("/characters/scaled/{filename}", methods=["GET", "HEAD"])
async def serve_scaled_character(filename: str):
    """Serve pre-scaled character PNG images (350x350)."""
    filepath = os.path.normpath(os.path.join(SCALED_CHARS_DIR, filename))
    if not filepath.startswith(SCALED_CHARS_DIR):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Scaled character not found")
    return FileResponse(filepath, media_type="image/png")
