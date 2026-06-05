"""Load unit registry from JSON config (FR-6)."""

import json
from pathlib import Path

from domain.registry import UnitRegistry

UNITS_KEY = "units"
METERS_PER_UNIT_KEY = "meters_per_unit"


def load_registry(config_path: Path) -> UnitRegistry:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    units = config[UNITS_KEY]

    registry = UnitRegistry()
    for unit_name, unit_config in units.items():
        registry.register(
            unit_name,
            meters_per_unit=unit_config[METERS_PER_UNIT_KEY],
        )
    return registry
