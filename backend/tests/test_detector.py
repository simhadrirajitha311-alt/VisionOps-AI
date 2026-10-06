from app.events.schemas import DetectionRecord


def test_detection_schema_validation():
    detection = DetectionRecord(
        class_id=0,
        class_name="person",
        confidence=0.94,
        bbox={"x1": 100, "y1": 120, "x2": 300, "y2": 500},
    )

    assert detection.class_name == "person"
    assert detection.bbox["x2"] > detection.bbox["x1"]
    assert 0.0 <= detection.confidence <= 1.0
