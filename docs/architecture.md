# VisionOps AI Architecture

## Overview

The VisionOps AI platform is structured as a small service-oriented application:

- A FastAPI backend exposes APIs for system health, detections, metrics, events, and camera zones.
- A video processor handles frame acquisition, object detection, and tracking logic.
- A database layer persists metadata and event records.
- A Vite + React frontend renders live status dashboards and camera monitoring UI.

## Request flow

1. The browser loads the frontend dashboard from the React app.
2. The frontend queries the backend health and system status endpoints.
3. The backend retrieves the current pipeline state, metrics, and zone metadata.
4. The vision pipeline returns detection and event data used by the UI.

## Components

### Backend

- `app.main` creates the FastAPI app and initializes the vision pipeline.
- `app.api.routes` contains HTTP routes used by clients and monitoring systems.
- `app.vision.*` holds detection, tracking, and event logic.
- `app.database.*` manages SQLite persistence and models.

### Frontend

- `src/App.tsx` coordinates the dashboard data and user interactions.
- Vite serves the UI and uses the configured API base URL.

## Operational notes

- Local development uses `uvicorn` and Vite dev servers.
- Docker Compose can run both services together for a consistent environment.
- The system is designed to be expanded with additional automation triggers and alert rules.
