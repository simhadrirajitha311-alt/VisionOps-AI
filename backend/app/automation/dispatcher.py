from __future__ import annotations

import json
from typing import Any

import httpx


class ActionDispatcher:
    """Dispatches local and webhook-based actions for observed events."""

    def __init__(self, webhook_url: str | None = None) -> None:
        self.webhook_url = webhook_url

    def dispatch(self, event: dict[str, Any]) -> dict[str, Any]:
        actions: list[str] = ["dashboard_notification", "local_log"]
        payload = {
            "event_type": event.get("event_type"),
            "track_id": event.get("track_id"),
            "zone_id": event.get("zone_id"),
            "severity": event.get("severity"),
            "timestamp": event.get("timestamp"),
        }

        if self.webhook_url:
            actions.append("webhook")
            try:
                response = httpx.post(self.webhook_url, content=json.dumps(payload), timeout=5.0)
                response.raise_for_status()
            except httpx.HTTPError:
                actions.append("webhook_failed")

        return {"event": event, "actions": actions}
