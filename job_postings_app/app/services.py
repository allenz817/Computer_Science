from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError

from app.collectors.common import split_keywords
from app.collectors.remoteok import fetch_remoteok_jobs
from app.collectors.remotive import fetch_remotive_jobs
from app.config import settings
from app.database import SessionLocal
from app.models import JobPosting


def collect_jobs(raw_keywords: str, location: str) -> dict[str, int]:
    keywords = split_keywords(raw_keywords)
    limit = settings.max_results_per_source

    fetched = []
    fetched.extend(fetch_remotive_jobs(keywords, location, limit))
    fetched.extend(fetch_remoteok_jobs(keywords, location, limit))

    added = 0

    with SessionLocal() as session:
        for item in fetched:
            post = JobPosting(
                source=item["source"],
                source_id=item["source_id"],
                title=item["title"],
                company=item["company"],
                location=item["location"],
                description=item["description"],
                url=item["url"],
                posted_at=item["posted_at"],
                matched_keyword=item["matched_keyword"],
                collected_at=datetime.utcnow(),
            )
            session.add(post)
            try:
                session.commit()
                added += 1
            except IntegrityError:
                session.rollback()

    return {"fetched": len(fetched), "added": added}


def get_latest_jobs(limit: int = 100) -> list[JobPosting]:
    with SessionLocal() as session:
        stmt = select(JobPosting).order_by(desc(JobPosting.collected_at)).limit(limit)
        return list(session.scalars(stmt).all())


def filter_jobs(jobs: Iterable[JobPosting], keywords: str, location: str) -> list[JobPosting]:
    keyword_list = split_keywords(keywords)
    filtered: list[JobPosting] = []

    for job in jobs:
        haystack = f"{job.title} {job.company} {job.description}".lower()
        if keyword_list and not any(k in haystack for k in keyword_list):
            continue

        if location and location.lower() not in (job.location or "").lower():
            continue

        filtered.append(job)

    return filtered
