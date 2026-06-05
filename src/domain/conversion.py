"""Length conversion — registry-driven, no hardcoded ratios."""

from domain.registry import UnitRegistry


def convert_all(value: float, source_unit: str, registry: UnitRegistry) -> dict[str, float]:
    source_meters_per_unit = registry.meters_per_unit(source_unit)
    value_in_meters = value * source_meters_per_unit

    return {
        unit: value_in_meters / registry.meters_per_unit(unit)
        for unit in registry.unit_names()
    }
