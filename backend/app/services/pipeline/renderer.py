from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lesson import Lesson
from app.models.video import Video, BackgroundVideo
from app.models.rendering import RenderingJob


class VideoRenderer:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def start_render(self, lesson_id: str, background_category: str = "minecraft_parkour") -> dict:
        result = await self.db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = result.scalar_one_or_none()
        if not lesson:
            return {"error": "Lesson not found"}

        bg_result = await self.db.execute(
            select(BackgroundVideo).where(BackgroundVideo.category == background_category, BackgroundVideo.is_active == True)
        )
        background = bg_result.scalars().first()

        job = RenderingJob(
            lesson_id=lesson_id,
            status="queued",
            background_video_id=background.id if background else None,
            voice_config={"stewie": {"speed": 1.2, "pitch": 1.1}, "peter": {"speed": 0.8, "pitch": 0.7}},
            subtitle_config={"max_chars_per_line": 42, "max_lines": 2, "font_size": 24},
            render_config={"resolution": "1080x1920", "fps": 30, "bitrate": "2M", "format": "mp4"},
        )
        self.db.add(job)
        await self.db.flush()

        video = Video(
            lesson_id=lesson_id, background_video_id=background.id if background else None,
            url="", duration_seconds=lesson.estimated_duration_seconds, status="pending",
            rendering_job_id=job.id, voice_config=job.voice_config,
        )
        self.db.add(video)
        await self.db.commit()

        return {"status": "queued", "job_id": job.id, "video_id": video.id}

    async def process_render(self, job_id: str) -> dict:
        result = await self.db.execute(select(RenderingJob).where(RenderingJob.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            return {"error": "Job not found"}
        job.status = "completed"
        job.progress_percent = 100.0
        await self.db.commit()
        return {"status": "completed", "job_id": job.id}
