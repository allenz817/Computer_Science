from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_title: str = os.getenv("APP_TITLE", "Job Postings Tracker")
    db_path: str = os.getenv("DB_PATH", "jobs.db")
    default_keywords: str = os.getenv("DEFAULT_KEYWORDS", "python,data,analyst")
    default_location: str = os.getenv("DEFAULT_LOCATION", "United States")
    scheduler_minutes: int = int(os.getenv("SCHEDULER_MINUTES", "60"))
    max_results_per_source: int = int(os.getenv("MAX_RESULTS_PER_SOURCE", "100"))


settings = Settings()
