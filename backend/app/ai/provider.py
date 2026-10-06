from __future__ import annotations

from typing import Any

from app.core.config import settings


class AIProvider:
    """Provider-agnostic AI interface. If no key is configured, it falls back to evidence-based summaries."""

    def __init__(self, provider: str | None = None, api_key: str | None = None) -> None:
        self.provider = provider or settings.llm_provider
        self.api_key = api_key or settings.llm_api_key

    def summarize_event(self, event: dict[str, Any]) -> str:
        if not self.api_key:
            event_type = event.get("event_type", "event")
            object_name = event.get("object_class") or "object"
            zone = event.get("zone_id") or "monitored area"
            confidence = event.get("confidence", 0.0)
            return (
                f"Observed {object_name} in {zone}. "
                f"The system recorded a {event_type} with confidence {confidence:.2f}. "
                "This is a fact-based observation, not a speculative claim."
            )
        return f"AI summary for {event.get('event_type', 'event')} is unavailable because the provider is not configured in this environment."

    def explain_anomaly(self, anomaly: dict[str, Any]) -> str:
        if not self.api_key:
            return (
                f"The anomaly score is {anomaly.get('score', 0.0):.2f}. "
                f"Reason: {anomaly.get('reason', 'No reason provided.')}. "
                "Observed facts were used; interpretive context is explicitly separated."
            )
        return "AI explanation unavailable without a configured LLM key."

    def generate_incident_report(self, events: list[dict[str, Any]]) -> str:
        if not events:
            return "No events were detected in the reporting window."
        high_severity = [event for event in events if event.get("severity") == "high"]
        summary = " | ".join(event.get("event_type", "event") for event in events[:3])
        if self.api_key:
            return f"Incident report: {summary}"
        return (
            f"Incident report based on {len(events)} events. "
            f"The most severe events involved {len(high_severity)} high-risk observations. "
            "All statements are grounded in recorded event metadata."
        )
