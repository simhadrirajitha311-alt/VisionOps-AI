from __future__ import annotations

from typing import Any

import numpy as np
from ultralytics import YOLO

from app.core.config import settings


class ObjectDetector:
    """Loads a YOLO model once and runs detection or tracking on input frames."""

    _model_cache: dict[str, YOLO] = {}

    def __init__(self, model_name: str | None = None, confidence_threshold: float | None = None) -> None:
        self.model_name = model_name or settings.model_name
        self.confidence_threshold = confidence_threshold if confidence_threshold is not None else settings.confidence_threshold
        self._model: YOLO | None = None

    def _load_model(self) -> YOLO:
        if self.model_name not in self._model_cache:
            self._model_cache[self.model_name] = YOLO(self.model_name)
        self._model = self._model_cache[self.model_name]
        return self._model

    def detect(self, frame: np.ndarray) -> list[dict[str, Any]]:
        model = self._load_model()
        results = model(frame, conf=self.confidence_threshold, verbose=False)
        detections: list[dict[str, Any]] = []
        if not results or len(results) == 0:
            return detections

        boxes = results[0].boxes
        if boxes is None or len(boxes) == 0:
            return detections

        for index in range(len(boxes)):
            box = boxes[index]
            cls = int(box.cls[index]) if hasattr(box, "cls") and len(box.cls) > index else 0
            class_name = model.names.get(cls, "object")
            x1, y1, x2, y2 = [float(value) for value in box.xyxy[index].tolist()]
            confidence = float(box.conf[index]) if hasattr(box, "conf") and len(box.conf) > index else 0.0
            detections.append(
                {
                    "class_id": cls,
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                }
            )
        return detections

    def track(self, frame: np.ndarray) -> list[dict[str, Any]]:
        model = self._load_model()
        results = model.track(frame, persist=True, conf=self.confidence_threshold, verbose=False)
        detections: list[dict[str, Any]] = []
        if not results or len(results) == 0:
            return detections

        boxes = results[0].boxes
        if boxes is None or len(boxes) == 0:
            return detections

        for index in range(len(boxes)):
            box = boxes[index]
            cls = int(box.cls[index]) if hasattr(box, "cls") and len(box.cls) > index else 0
            class_name = model.names.get(cls, "object")
            x1, y1, x2, y2 = [float(value) for value in box.xyxy[index].tolist()]
            confidence = float(box.conf[index]) if hasattr(box, "conf") and len(box.conf) > index else 0.0
            track_id = int(box.id[index]) if hasattr(box, "id") and box.id is not None and len(box.id) > index else None
            detections.append(
                {
                    "track_id": track_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                }
            )
        return detections
