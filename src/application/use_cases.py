"""Application use cases (orchestration)."""

from application.parsing import parse_register_unit
from domain.registry import UnitRegistry


def register_unit_from_string(registry: UnitRegistry, text: str) -> None:
    unit_name, meters_per_unit = parse_register_unit(text)
    registry.register(unit_name, meters_per_unit=meters_per_unit)
