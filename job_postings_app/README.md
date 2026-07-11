# Job Postings App

A lightweight app that collects job postings based on keyword and location criteria, stores them in SQLite, and displays them in a local web dashboard.

## Important note about LinkedIn

This MVP intentionally uses API-friendly/public sources to avoid violating LinkedIn restrictions. It is designed so you can add compliant integrations later.

## Features

- Collect jobs by `keywords` and `location`
- Sources included: Remotive and RemoteOK
- Deduplicate postings in SQLite
- Filter and browse jobs in a FastAPI dashboard
- Scheduled background collection using APScheduler

## Quick start

1. Open a terminal in this folder.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and edit values if needed.
5. Run the app:

```bash
uvicorn run:app --reload
```

6. Open `http://127.0.0.1:8000`.

## Environment variables

- `APP_TITLE`: app title
- `DB_PATH`: sqlite file path
- `DEFAULT_KEYWORDS`: comma-separated keywords
- `DEFAULT_LOCATION`: location filter
- `SCHEDULER_MINUTES`: background collection frequency
- `MAX_RESULTS_PER_SOURCE`: upper bound per source pull

## Project layout

- `app/main.py`: FastAPI routes and page rendering
- `app/services.py`: collection orchestration and filtering
- `app/collectors/*.py`: source-specific fetchers
- `app/models.py`: SQLAlchemy models
- `app/scheduler.py`: periodic collection
- `templates/index.html`: dashboard
- `static/style.css`: styling
