# BestFit Job Board API

A Flask-based Job Board API with JWT authentication, role-based access control, and an async application-processing pipeline (Celery + Redis) for confirmation emails and PDF generation.

## Prerequisites

- Python 3.12+
- PostgreSQL
- Redis
- Docker & Docker Compose (recommended for full local setup)

## Installation & Setup

```bash
git clone <repo-url>
cd bestfit_jobboard
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your database, JWT, mail (Mailtrap), and S3-compatible storage credentials (Backblaze B2, R2, etc.).

Set FLASK_APP in project:
```
export FLASK_APP=jobboard
```

Run migrations:
```bash
flask db upgrade
```

Start the app:
```bash
flask run
```

In separate terminals, start Redis and the Celery worker:
```bash
celery -A celery_worker.celery worker --loglevel=info
```

### Docker (all services)

```bash
docker compose up --build
```
Spins up the API, worker, Postgres, and Redis together.

## Usage

Interactive API docs (Swagger UI) are available at `/docs` once the app is running, including a built-in "Authorize" button for testing JWT-protected endpoints directly.

### Key Endpoints

| Endpoint | Description |
|---|---|
| `POST /auth/register` | Register as employer or candidate |
| `POST /auth/login` | Log in, receive JWT tokens |
| `GET /jobs` | List/search/filter job postings (public) |
| `POST /jobs` | Create a job posting (employer only) |
| `PUT/DELETE /jobs/{id}` | Update/delete a job (employer only) |
| `POST /applications` | Submit a job application (candidate only) |
| `GET /applications/{id}/status` | Check async pipeline status (`pending` → `email_sent` → `pdf_ready`) |

Submitting an application triggers a background pipeline: a confirmation email is sent, then a PDF summary of the application is generated and stored, with automatic retries on transient failures.

## Testing

```bash
pytest
```