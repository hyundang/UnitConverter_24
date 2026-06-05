"""Application use cases (orchestration)."""

from application.parsing import REGISTER_EQUALS, parse_register_unit, parse_unit_value
from domain.conversion import convert_all
from domain.registry import UnitRegistry
from domain.validation import validate_unit


def register_unit_from_string(registry: UnitRegistry, text: str) -> None:
    unit_name, meters_per_unit = parse_register_unit(text)
    registry.register(unit_name, meters_per_unit=meters_per_unit)


def process_stdin_lines(
    registry: UnitRegistry, lines: list[str]
) -> tuple[str, float, dict[str, float]] | None:
    unit: str | None = None
    value: float | None = None
    results: dict[str, float] | None = None

    for line in lines:
        if REGISTER_EQUALS in line:
            register_unit_from_string(registry, line)
            continue

        unit, value = parse_unit_value(line)
        validate_unit(unit, registry)
        results = convert_all(value, unit, registry)

    if results is None or unit is None or value is None:
        return None

    return unit, value, results
