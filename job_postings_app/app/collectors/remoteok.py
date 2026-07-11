from __future__ import annotations

from typing import Any

import requests

from app.collectors.common import location_matches, match_keyword


REMOTEOK_URL = "https://remoteok.com/api"


def fetch_remoteok_jobs(keywords: list[str], location: str, limit: int) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []

    headers = {"User-Agent": "job-postings-tracker/1.0"}

    try:
        response = requests.get(REMOTEOK_URL, headers=headers, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return jobs

    for item in payload:
        if not isinstance(item, dict):
            continue

        title = item.get("position") or item.get("title") or ""
        company = item.get("company", "Unknown")
        tags = " ".join(item.get("tags", []))
        candidate_text = f"{title} {company} {tags}"
        matched = match_keyword(candidate_text, keywords)

        if keywords and not matched:
            continue

        job_location = item.get("location") or "Worldwide"
        if not location_matches(job_location, location):
            continue

        jobs.append(
            {
                "source": "remoteok",
                "source_id": str(item.get("id", item.get("url", ""))),
                "title": title,
                "company": company,
                "location": job_location,
                "description": tags,
                "url": item.get("url", ""),
                "posted_at": str(item.get("date", "")),
                "matched_keyword": matched,
            }
        )

        if len(jobs) >= limit:
            break

    return jobs
