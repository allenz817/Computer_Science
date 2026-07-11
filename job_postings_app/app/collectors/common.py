from __future__ import annotations

from typing import Iterable


def split_keywords(raw_keywords: str) -> list[str]:
    return [k.strip().lower() for k in raw_keywords.split(",") if k.strip()]


def match_keyword(text: str, keywords: Iterable[str]) -> str:
    value = (text or "").lower()
    for keyword in keywords:
        if keyword in value:
            return keyword
    return ""


def location_matches(job_location: str, requested_location: str) -> bool:
    if not requested_location:
        return True
    return requested_location.lower() in (job_location or "").lower()
