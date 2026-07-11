from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class JobPosting(Base):
    __tablename__ = "job_postings"
    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_source_source_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source: Mapped[str] = mapped_column(String(50), index=True)
    source_id: Mapped[str] = mapped_column(String(255), index=True)
    title: Mapped[str] = mapped_column(String(500))
    company: Mapped[str] = mapped_column(String(255), default="Unknown")
    location: Mapped[str] = mapped_column(String(255), default="Unknown")
    description: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(String(1000), default="")
    posted_at: Mapped[str] = mapped_column(String(100), default="")
    matched_keyword: Mapped[str] = mapped_column(String(100), default="")
    collected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
