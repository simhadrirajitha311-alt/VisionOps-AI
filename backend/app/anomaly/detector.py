from __future__ import annotations

from typing import Any


class AnomalyDetector:
    """Baseline statistical anomaly detection designed to be extensible."""

    def evaluate(self, metrics: dict[str, Any]) -> dict[str, Any]:
        object_count = float(metrics.get("object_count", 0))
        duration_seconds = float(metrics.get("duration_seconds", 0))
        activity_count = float(metrics.get("activity_count", 0))
        unexpected_class = bool(metrics.get("unexpected_class", False))

        score = 0.0
        reasons: list[str] = []

        if object_count > 5:
            score += 0.35
            reasons.append("Object count exceeded the expected baseline.")
        if duration_seconds > 15:
            score += 0.30
            reasons.append("Object remained in a monitored zone longer than expected.")
        if activity_count > 3:
            score += 0.20
            reasons.append("Activity frequency increased beyond the baseline pattern.")
        if unexpected_class:
            score += 0.15
            reasons.append("Unexpected object class detected.")

        score = min(1.0, score)
        is_anomaly = score > 0.5
        reason = ". ".join(reasons) if reasons else "No baseline anomaly conditions were triggered."
        return {
            "is_anomaly": is_anomaly,
            "score": round(score, 2),
            "reason": reason,
        }
