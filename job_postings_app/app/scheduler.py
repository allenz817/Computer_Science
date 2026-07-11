from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.services import collect_jobs


scheduler = BackgroundScheduler(timezone="UTC")


def _scheduled_collection() -> None:
    collect_jobs(settings.default_keywords, settings.default_location)


def start_scheduler() -> None:
    if scheduler.running:
        return

    scheduler.add_job(
        _scheduled_collection,
        "interval",
        minutes=settings.scheduler_minutes,
        id="scheduled_job_collection",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
