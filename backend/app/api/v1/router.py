from fastapi import APIRouter
from app.api.v1 import auth, users, concepts, lessons, videos, quizzes, bookmarks, progress, search, analytics, admin, pipeline

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(concepts.router, prefix="/concepts", tags=["Concepts"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
api_router.include_router(videos.router, prefix="/videos", tags=["Videos"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["Bookmarks"])
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
