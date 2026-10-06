from __future__ import annotations

import time
from typing import Any

import cv2
import numpy as np

from app.vision.camera import CameraManager
from app.vision.detector import ObjectDetector
from app.vision.tracker import ObjectTracker
from app.vision.zones import ZoneManager


class VisionProcessor:
    """Coordinates camera, detection, tracking, and zone overlays."""

    def __init__(self, source: int | str = 0) -> None:
        self.camera = CameraManager(source=source)
        self.detector = ObjectDetector()
        self.tracker = ObjectTracker()
        self.zones = ZoneManager()
        self.latest_frame: np.ndarray | None = None
        self.last_metrics: dict[str, Any] = {
            "fps": 0.0,
            "inference_latency_ms": 0.0,
            "frame_processing_time_ms": 0.0,
            "detected_object_count": 0,
            "event_count": 0,
            "camera_status": "offline",
        }
        self._frame_times: list[float] = []

    def add_zone(self, zone: dict[str, Any]) -> dict[str, Any]:
        return self.zones.add_zone(zone)

    def render_frame(self, frame: np.ndarray | None = None) -> np.ndarray:
        if frame is None:
            frame = self._blank_frame()
        overlay = frame.copy()
        for zone in self.zones.zones.values():
            polygon = [(int(x), int(y)) for x, y in zone.get("polygon", [])]
            if polygon:
                cv2.polylines(overlay, [np.array(polygon, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=2)
                cv2.putText(overlay, zone.get("name", "Zone"), (polygon[0][0] + 10, polygon[0][1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        return overlay

    def process(self, frame: np.ndarray | None = None) -> dict[str, Any]:
        started = time.perf_counter()
        if frame is None:
            frame = self.camera.read_frame()
        if frame is None:
            return {"detections": [], "annotated_frame": self._blank_frame(), "metrics": self.last_metrics}

        detections = self.detector.detect(frame)
        tracked = self.tracker.update(detections)
        self.latest_frame = self.render_frame(frame)

        elapsed_ms = (time.perf_counter() - started) * 1000
        self.last_metrics["frame_processing_time_ms"] = round(elapsed_ms, 2)
        self.last_metrics["detected_object_count"] = len(tracked)
        self.last_metrics["camera_status"] = "online" if self.camera.is_open else "offline"
        self.last_metrics["inference_latency_ms"] = round(elapsed_ms, 2)
        return {"detections": tracked, "annotated_frame": self.latest_frame, "metrics": self.last_metrics}

    def _blank_frame(self) -> np.ndarray:
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def open_camera(self) -> bool:
        return self.camera.open()

    def release_camera(self) -> None:
        self.camera.release()

    def snapshot(self) -> np.ndarray:
        frame = self.camera.read_frame()
        if frame is None:
            return self._blank_frame()
        return self.render_frame(frame)
