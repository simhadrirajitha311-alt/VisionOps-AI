from __future__ import annotations

from typing import Iterator

import cv2
import numpy as np

from app.core.config import settings


class CameraManager:
    """Handles opening, reading, and releasing a camera or video file."""

    def __init__(self, source: int | str = 0, width: int | None = None, height: int | None = None) -> None:
        self.source = source if source != 0 else settings.camera_index
        self.width = width or settings.frame_width
        self.height = height or settings.frame_height
        self.capture: cv2.VideoCapture | None = None

    def open(self) -> bool:
        self.capture = cv2.VideoCapture(self.source)
        if self.capture is None or not self.capture.isOpened():
            return False
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        return True

    def read_frame(self) -> np.ndarray | None:
        if self.capture is None:
            return None
        ok, frame = self.capture.read()
        if not ok or frame is None:
            return None
        return frame

    def stream_frames(self) -> Iterator[np.ndarray]:
        while True:
            frame = self.read_frame()
            if frame is not None:
                yield frame
            else:
                break

    def release(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None

    @property
    def is_open(self) -> bool:
        return self.capture is not None and self.capture.isOpened()
