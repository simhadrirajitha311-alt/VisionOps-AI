from app.events.event_engine import EventEngine


def test_event_generation_and_cooldown():
    engine = EventEngine()

    vehicle_entered = {
        "track_id": 7,
        "class_name": "person",
        "confidence": 0.93,
        "bbox": {"x1": 150, "y1": 150, "x2": 250, "y2": 260},
        "zone_id": "restricted-zone",
        "zone_name": "Restricted Area",
    }

    event_1 = engine.process_object_event(vehicle_entered)
    assert event_1["event_type"] == "PERSON_ENTERED_ZONE"

    duplicate = engine.process_object_event(vehicle_entered)
    assert duplicate is None

    dwell_event = engine.process_dwell_event(track_id=7, class_name="person", zone_id="restricted-zone", duration_seconds=18)
    assert dwell_event["event_type"] == "UNUSUAL_DWELL_TIME"
