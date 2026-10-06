from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logging import logger
from app.database.database import init_db
from app.vision.processor import VisionProcessor

app = FastAPI(
    title="VisionOps AI",
    description="Open-source real-time computer vision pipeline for detection, tracking, events, and automation.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _initialize_state() -> None:
    init_db()
    logger.info("Database initialized for VisionOps AI")
    pipeline = VisionProcessor(source=settings.camera_index)
    pipeline.add_zone(
        {
            "id": "restricted-zone",
            "name": "Restricted Area",
            "type": "restricted",
            "polygon": [[100, 100], [500, 100], [500, 400], [100, 400]],
        }
    )
    app.state.pipeline = pipeline
    app.state.events = []
    app.state.detections = []
    app.state.zones = pipeline.zones.zones
    app.state.metrics = pipeline.last_metrics


_initialize_state()


@app.on_event("startup")
def startup() -> None:
    if not hasattr(app.state, "pipeline"):
        _initialize_state()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


app.include_router(router)
