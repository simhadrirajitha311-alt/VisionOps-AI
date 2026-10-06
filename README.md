# VisionOps AI

VisionOps AI is a real-time computer vision platform for object detection, zone monitoring, event tracking, and automation workflows. The project combines a FastAPI backend with a React + Vite frontend for local monitoring and dashboard interactions.

## Features

- Real-time video processing pipeline
- Detection and tracking workflows
- Restricted-zone and alert event support
- System metrics and health endpoints
- Web dashboard for live status and inspection
- SQLite-backed configuration and event storage

## Stack

- Backend: Python, FastAPI, OpenCV, Ultralytics
- Frontend: React, TypeScript, Vite
- Database: SQLite via SQLAlchemy
- Container tooling: Docker / Docker Compose

## Repository layout

- [backend](backend) — API, detection pipeline, database, and tests
- [frontend](frontend) — React dashboard and UI assets
- [docs](docs) — project documentation and architecture notes
- [docker-compose.yml](docker-compose.yml) — local multi-service orchestration
- [Dockerfile](Dockerfile) — backend container image
- [Makefile](Makefile) — common developer commands
- [.env.example](.env.example) — environment variable template

## Quick start

### Option 1: Local development

1. Create a Python environment and install backend dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start the API:
   ```bash
   cd backend
   PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. In a second terminal, install and start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev -- --host 0.0.0.0 --port 3000
   ```

4. Open the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

### Option 2: Docker Compose

```bash
docker compose up --build
```

This starts the backend and frontend together with the project configuration in [docker-compose.yml](docker-compose.yml).

## Environment variables

Copy [.env.example](.env.example) to a local `.env` file and adjust values for your environment.

## Testing

Run the backend suite with:

```bash
cd backend
PYTHONPATH=. pytest -q
```

## Production notes

- Set a secure `SECRET_KEY` before deploying.
- Adjust the camera index and model path based on your hardware.
- Use a real database or managed deployment target when moving beyond local development.
