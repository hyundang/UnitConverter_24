"""Domain validation — registered unit checks (FR-1.3)."""

from domain.registry import UnitRegistry

UNKNOWN_UNIT_LABEL = "unknown unit"


class UnknownUnitError(ValueError):
    """Raised when a unit is not registered in the registry."""


def validate_unit(unit: str, registry: UnitRegistry) -> None:
    registered_units = registry.unit_names()
    if unit in registered_units:
        return

    supported_hint = ", ".join(registered_units)
    raise UnknownUnitError(
        f"{UNKNOWN_UNIT_LABEL}: {unit}. Supported units: {supported_hint}"
    )
