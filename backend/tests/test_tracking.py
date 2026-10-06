from app.vision.tracker import ObjectTracker


def test_tracking_assigns_persistent_ids_for_mocked_detections():
    tracker = ObjectTracker()

    frame_one = [
        {"track_id": None, "class_name": "person", "confidence": 0.95, "bbox": {"x1": 10, "y1": 20, "x2": 100, "y2": 200}},
        {"track_id": None, "class_name": "car", "confidence": 0.9, "bbox": {"x1": 200, "y1": 30, "x2": 300, "y2": 120}},
    ]
    tracked_one = tracker.update(frame_one)

    assert {item["track_id"] for item in tracked_one} == {1, 2}

    frame_two = [
        {"track_id": None, "class_name": "person", "confidence": 0.9, "bbox": {"x1": 12, "y1": 22, "x2": 102, "y2": 202}},
        {"track_id": None, "class_name": "car", "confidence": 0.88, "bbox": {"x1": 250, "y1": 35, "x2": 320, "y2": 125}},
    ]
    tracked_two = tracker.update(frame_two)

    person_ids = [item["track_id"] for item in tracked_two if item["class_name"] == "person"]
    car_ids = [item["track_id"] for item in tracked_two if item["class_name"] == "car"]
    assert person_ids and person_ids[0] == 1
    assert car_ids and car_ids[0] == 2
