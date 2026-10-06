from app.anomaly.detector import AnomalyDetector


def test_anomaly_scoring_uses_baseline_rules():
    detector = AnomalyDetector()
    result = detector.evaluate({
        "object_count": 8,
        "duration_seconds": 22,
        "activity_count": 4,
        "unexpected_class": True,
    })

    assert result["is_anomaly"] is True
    assert 0.0 <= result["score"] <= 1.0
    assert result["reason"]
