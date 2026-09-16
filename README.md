# Verba — English Speaking Practice

A premium, responsive British-English speaking practice platform for teachers. Verba pairs lesson media, transcripts, comprehension and an in-browser recording studio with a deliberately separated AI architecture: a speech provider owns measurable pronunciation/fluency signals, while Gemini provides language interpretation and next-step guidance.

## Included in this foundation

- **Responsive Next.js product UI**: landing page, teacher dashboard, lesson library/player, recording studio, progress page and admin overview.
- **Accessible interaction foundations**: semantic controls, labelled inputs, visible controls, responsive bottom navigation and transcript-first lesson design.
- **FastAPI service foundation** with Pydantic contracts, CORS configuration and REST route placeholders.
- **PostgreSQL / SQLAlchemy relational model** covering users, lessons/media/transcripts/notes, vocabulary, comprehension, attempts, objective scores, AI feedback, practice words, progress and notifications.
- **Alembic initial migration** and environment configuration.
- **Safe AI boundaries**: Gemini is server-only and validates structured responses; no fake pronunciation scores are generated when a speech provider is unavailable.
- **PWA manifest** and app icon.

## Architecture

```
frontend/             Next.js App Router UI
backend/app/          FastAPI application
  core/               settings and security configuration
  database/           SQLAlchemy session and declarative base
  models/             normalized relational schema
  schemas/            API/AI validation contracts
  services/           Gemini and provider interfaces
backend/alembic/      schema migration environment
```

## Local development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
cd backend
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

The API documentation is available at `http://localhost:8000/docs`.

## PostgreSQL and migrations

Create a PostgreSQL database and set `DATABASE_URL` in `.env`. Apply the initial schema with `alembic upgrade head`. During development, after changing SQLAlchemy models, generate a reviewed revision with:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## Environment variables

Copy `.env.example` to `.env`. `JWT_SECRET` must be a long random secret in production. Configure `GEMINI_API_KEY` only on the backend. Set `SPEECH_PROVIDER` when a production speech service has been connected; the supplied unconfigured adapter fails safely instead of inventing scores.

## AI and speech setup

`GeminiService` submits structured reference text, teacher transcript, provider-owned speech signals and lesson difficulty, then validates the JSON response against `AIAnalysis`. The `SpeechAnalysisService` protocol accepts `en-GB` by default. Implement a provider behind that protocol to supply transcription, timing, pronunciation, fluency and intonation signals. Gemini must not be used to manufacture those measurements.

## Production notes

Use managed PostgreSQL and object storage for media; store URLs and metadata in `lesson_media` / `speaking_attempts`, never media blobs in the database. Configure restrictive CORS origins, a managed secret store and HTTPS. Add a production authentication repository/JWT dependency before exposing auth routes.
