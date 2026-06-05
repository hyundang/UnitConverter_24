"""Unit registry — meters-per-unit SSOT holder within domain."""


class UnitRegistry:
    def __init__(self) -> None:
        self._meters_per_unit: dict[str, float] = {}

    def register(self, name: str, *, meters_per_unit: float) -> None:
        self._meters_per_unit[name] = meters_per_unit

    def meters_per_unit(self, name: str) -> float:
        return self._meters_per_unit[name]

    def unit_names(self) -> list[str]:
        return list(self._meters_per_unit.keys())
