from __future__ import annotations

from typing import Any


class ZoneManager:
    """Manages named monitoring zones and point-in-polygon checks."""

    def __init__(self) -> None:
        self.zones: dict[str, dict[str, Any]] = {}

    def add_zone(self, zone: dict[str, Any]) -> dict[str, Any]:
        zone_id = zone.get("id") or zone.get("name")
        if not zone_id:
            raise ValueError("Zone requires an id or name")
        self.zones[str(zone_id)] = zone
        return zone

    def remove_zone(self, zone_id: str) -> None:
        self.zones.pop(zone_id, None)

    def has_zone(self, zone_id: str) -> bool:
        return zone_id in self.zones

    def get_zone(self, zone_id: str) -> dict[str, Any] | None:
        return self.zones.get(zone_id)

    def point_in_polygon(self, point: tuple[float, float], polygon: list[list[float]]) -> bool:
        x, y = point
        inside = False
        for i in range(len(polygon)):
            xi, yi = polygon[i]
            xj, yj = polygon[(i + 1) % len(polygon)]
            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi)
            if intersect:
                inside = not inside
        return inside

    def point_in_zone(self, point: tuple[float, float], zone_id: str) -> bool:
        zone = self.zones.get(zone_id)
        if zone is None:
            return False
        polygon = zone.get("polygon", [])
        return bool(polygon) and self.point_in_polygon(point, polygon)

    def zone_center(self, zone_id: str) -> tuple[float, float] | None:
        zone = self.zones.get(zone_id)
        if zone is None:
            return None
        polygon = zone.get("polygon") or []
        if not polygon:
            return None
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        return (sum(xs) / len(xs), sum(ys) / len(ys))
