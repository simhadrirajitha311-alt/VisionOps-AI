from __future__ import annotations

from typing import Any


class ObjectTracker:
    """Simple persistent object tracking based on nearest centroid matching."""

    def __init__(self, max_lost_frames: int = 5) -> None:
        self.next_track_id = 1
        self.active_tracks: dict[int, dict[str, Any]] = {}
        self.max_lost_frames = max_lost_frames

    def _centroid(self, detection: dict[str, Any]) -> tuple[float, float]:
        bbox = detection.get("bbox", {})
        x1 = float(bbox.get("x1", 0))
        y1 = float(bbox.get("y1", 0))
        x2 = float(bbox.get("x2", x1))
        y2 = float(bbox.get("y2", y1))
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    def update(self, detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        assigned: list[dict[str, Any]] = []
        existing_track_ids = list(self.active_tracks.keys())

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                assigned.append({**detection, "track_id": int(track_id)})
                self.active_tracks[int(track_id)] = detection
                continue

            best_track_id = None
            best_distance = float("inf")
            for current_id in existing_track_ids:
                current = self.active_tracks.get(current_id, {})
                if current.get("class_name") != detection.get("class_name"):
                    continue
                distance = self._distance(self._centroid(current), self._centroid(detection))
                if distance < best_distance:
                    best_distance = distance
                    best_track_id = current_id

            if best_track_id is not None and best_distance < 120:
                detection["track_id"] = best_track_id
                self.active_tracks[best_track_id] = detection
            else:
                detection["track_id"] = self.next_track_id
                self.active_tracks[self.next_track_id] = detection
                self.next_track_id += 1

            assigned.append({**detection, "track_id": int(detection["track_id"])})

        self.active_tracks = {track_id: detection for track_id, detection in self.active_tracks.items() if any(item.get("track_id") == track_id for item in assigned)}
        return assigned

    @staticmethod
    def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
