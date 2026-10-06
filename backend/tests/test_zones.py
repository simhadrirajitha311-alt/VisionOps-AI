from app.vision.zones import ZoneManager


def test_point_in_polygon_and_zone_management():
    zone = {
        "id": "restricted-zone",
        "name": "Restricted Area",
        "type": "restricted",
        "polygon": [[100, 100], [500, 100], [500, 400], [100, 400]],
    }
    manager = ZoneManager()
    manager.add_zone(zone)

    assert manager.has_zone("restricted-zone") is True
    assert manager.point_in_zone((250, 250), "restricted-zone") is True
    assert manager.point_in_zone((50, 50), "restricted-zone") is False

    manager.remove_zone("restricted-zone")
    assert manager.has_zone("restricted-zone") is False
