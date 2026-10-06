from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

    @model_validator(mode="after")
    def validate_coordinates(self) -> "BoundingBox":
        if self.x2 < self.x1:
            raise ValueError("x2 must be greater than or equal to x1")
        if self.y2 < self.y1:
            raise ValueError("y2 must be greater than or equal to y1")
        return self


class DetectionRecord(BaseModel):
    class_id: int
    class_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: dict[str, float]


class TrackedObject(BaseModel):
    track_id: int
    class_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bbox: dict[str, float]


class ZoneDefinition(BaseModel):
    id: str
    name: str
    type: str = "restricted"
    polygon: list[list[int]]


class EventPayload(BaseModel):
    event_type: str
    track_id: int | None = None
    zone_id: str | None = None
    confidence: float | None = None
    timestamp: str
    severity: str = "medium"
    metadata: dict[str, Any] = {}
    status: str = "new"


class SystemStatus(BaseModel):
    status: str
    camera: dict[str, Any]
    metrics: dict[str, Any]
