from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from typing import Any

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.core.config import settings
from app.vision.processor import VisionProcessor

router = APIRouter(prefix="/api")


def _get_pipeline(request: Request) -> VisionProcessor:
    return request.app.state.pipeline


@router.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/system/status")
def system_status(request: Request) -> dict[str, Any]:
    pipeline = _get_pipeline(request)
    metrics = pipeline.last_metrics
    return {
        "status": "ok",
        "camera": {
            "source": settings.camera_index,
            "status": metrics.get("camera_status", "offline"),
            "frame_width": settings.frame_width,
            "frame_height": settings.frame_height,
        },
        "metrics": metrics,
        "objects": metrics.get("detected_object_count", 0),
        "events": metrics.get("event_count", 0),
        "fps": metrics.get("fps", 0.0),
        "inference_latency_ms": metrics.get("inference_latency_ms", 0.0),
    }


@router.get("/detections")
def detections(request: Request) -> list[dict[str, Any]]:
    pipeline = _get_pipeline(request)
    return getattr(request.app.state, "detections", []) or []


@router.get("/events")
def list_events(request: Request) -> list[dict[str, Any]]:
    return list(getattr(request.app.state, "events", []))


@router.get("/events/{event_id}")
def get_event(request: Request, event_id: str) -> dict[str, Any]:
    for event in getattr(request.app.state, "events", []):
        if str(event.get("id", event.get("event_type"))) == str(event_id):
            return event
    raise HTTPException(status_code=404, detail="Event not found")


@router.post("/events/{event_id}/acknowledge")
def acknowledge_event(request: Request, event_id: str) -> dict[str, str]:
    events = getattr(request.app.state, "events", [])
    for event in events:
        if str(event.get("id", event.get("event_type"))) == str(event_id):
            event["status"] = "acknowledged"
            return {"status": "acknowledged", "event_id": event_id}
    raise HTTPException(status_code=404, detail="Event not found")


@router.get("/zones")
def list_zones(request: Request) -> list[dict[str, Any]]:
    return list(getattr(request.app.state, "zones", []).values())


@router.post("/zones")
def add_zone(request: Request) -> dict[str, Any]:
    payload = request.json()
    zone = payload
    pipeline = _get_pipeline(request)
    created = pipeline.add_zone(zone)
    request.app.state.zones[created["id"]] = created
    return created


@router.delete("/zones/{zone_id}")
def delete_zone(request: Request, zone_id: str) -> dict[str, str]:
    pipeline = _get_pipeline(request)
    pipeline.zones.remove_zone(zone_id)
    request.app.state.zones.pop(zone_id, None)
    return {"status": "deleted", "zone_id": zone_id}


@router.get("/metrics")
def metrics(request: Request) -> dict[str, Any]:
    pipeline = _get_pipeline(request)
    return pipeline.last_metrics


@router.get("/video/stream")
def video_stream(request: Request) -> StreamingResponse:
    def generate() -> Any:
        pipeline = _get_pipeline(request)
        while True:
            frame = pipeline.snapshot()
            if frame is None:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ok, encoded = cv2.imencode(".jpg", frame)
            if not ok:
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + encoded.tobytes() +
                b"\r\n"
            )
            time.sleep(0.033)

    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/health")
def health_root() -> dict[str, Any]:
    return {"status": "ok"}
