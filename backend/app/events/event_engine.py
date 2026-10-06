from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.config import settings


class EventEngine:
    """Creates structured events from tracked object activity and zone state."""

    def __init__(self, cooldown_seconds: int | None = None) -> None:
        self.cooldown_seconds = cooldown_seconds or settings.event_cooldown_seconds
        self.recent_events: dict[tuple[str, int | str], datetime] = {}
        self.events: list[dict[str, Any]] = []

    def _should_emit(self, event_type: str, track_id: int | str | None, zone_id: str | None = None) -> bool:
        key = (event_type, track_id if track_id is not None else zone_id or "global")
        now = datetime.now(timezone.utc)
        previous = self.recent_events.get(key)
        if previous and now - previous < timedelta(seconds=self.cooldown_seconds):
            return False
        self.recent_events[key] = now
        return True

    def process_object_event(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        track_id = payload.get("track_id")
        zone_id = payload.get("zone_id")
        event_type = payload.get("event_type") or (
            "PERSON_ENTERED_ZONE" if payload.get("class_name") == "person" and zone_id else "OBJECT_DETECTED"
        )

        if zone_id and payload.get("class_name") == "person":
            event_type = "PERSON_ENTERED_ZONE"

        if self._should_emit(event_type, track_id, zone_id):
            result = {
                "event_type": event_type,
                "track_id": track_id,
                "zone_id": zone_id,
                "confidence": payload.get("confidence", 0.0),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": "high" if event_type == "PERSON_ENTERED_ZONE" else "medium",
                "object_class": payload.get("class_name"),
                "metadata": payload.get("metadata", {}),
                "status": "new",
            }
            self.events.append(result)
            return result
        return None

    def process_dwell_event(self, track_id: int, class_name: str, zone_id: str, duration_seconds: float) -> dict[str, Any] | None:
        threshold = 15
        if duration_seconds < threshold:
            return None
        event_type = "UNUSUAL_DWELL_TIME"
        if self._should_emit(event_type, track_id, zone_id):
            result = {
                "event_type": event_type,
                "track_id": track_id,
                "zone_id": zone_id,
                "confidence": 0.9,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": "high",
                "object_class": class_name,
                "metadata": {"duration_seconds": duration_seconds, "threshold_seconds": threshold},
                "status": "new",
            }
            self.events.append(result)
            return result
        return None

    def process_count_event(self, object_count: int, threshold: int = 5) -> dict[str, Any] | None:
        if object_count < threshold:
            return None
        event_type = "OBJECT_COUNT_THRESHOLD"
        if self._should_emit(event_type, object_count):
            result = {
                "event_type": event_type,
                "track_id": None,
                "zone_id": None,
                "confidence": min(1.0, object_count / max(threshold, 1) * 0.9),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": "medium",
                "object_class": "scene",
                "metadata": {"object_count": object_count, "threshold": threshold},
                "status": "new",
            }
            self.events.append(result)
            return result
        return None

    def acknowledge(self, event_id: str | int) -> bool:
        for event in self.events:
            if str(event.get("id", "")) == str(event_id):
                event["status"] = "acknowledged"
                return True
        return False
