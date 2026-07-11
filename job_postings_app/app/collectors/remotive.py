from __future__ import annotations

from typing import Any

import requests

from app.collectors.common import location_matches, match_keyword


REMOTIVE_URL = "https://remotive.com/api/remote-jobs"


def fetch_remotive_jobs(keywords: list[str], location: str, limit: int) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []

    try:
        response = requests.get(REMOTIVE_URL, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return jobs

    for item in payload.get("jobs", []):
        title = item.get("title", "")
        company = item.get("company_name", "Unknown")
        candidate_text = f"{title} {company} {item.get('description', '')}"
        matched = match_keyword(candidate_text, keywords)

        if keywords and not matched:
            continue

        job_location = item.get("candidate_required_location", "Unknown")
        if not location_matches(job_location, location):
            continue

        jobs.append(
            {
                "source": "remotive",
                "source_id": str(item.get("id", item.get("url", ""))),
                "title": title,
                "company": company,
                "location": job_location,
                "description": item.get("description", ""),
                "url": item.get("url", ""),
                "posted_at": item.get("publication_date", ""),
                "matched_keyword": matched,
            }
        )

        if len(jobs) >= limit:
            break

    return jobs
