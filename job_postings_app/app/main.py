from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import init_db
from app.scheduler import start_scheduler, stop_scheduler
from app.services import collect_jobs, filter_jobs, get_latest_jobs


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title=settings.app_title, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request, keywords: str = "", location: str = ""):
    all_jobs = get_latest_jobs(limit=300)
    filtered_jobs = filter_jobs(all_jobs, keywords, location)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "jobs": filtered_jobs,
            "job_count": len(filtered_jobs),
            "default_keywords": settings.default_keywords,
            "default_location": settings.default_location,
            "keywords": keywords,
            "location": location,
        },
    )


@app.post("/collect")
def collect(
    keywords: str = Form(default=settings.default_keywords),
    location: str = Form(default=settings.default_location),
):
    result = collect_jobs(keywords, location)
    return RedirectResponse(
        url=f"/?keywords={keywords}&location={location}&fetched={result['fetched']}&added={result['added']}",
        status_code=303,
    )
