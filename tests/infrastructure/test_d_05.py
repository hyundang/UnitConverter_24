"""D-05 — PRD FR-6 · §8.2: units.json load · README ratios."""

import pytest

from infrastructure.config_loader import load_registry
from domain.conversion import convert_all


@pytest.mark.prd_s4
def test_load_registry_from_json_with_readme_ratios(
    readme_units_json,
    supported_units,
    expected_meters_per_unit,
    expected_conversion_values,
    prd_s2_input,
):
    registry = load_registry(readme_units_json)

    assert set(registry.unit_names()) == set(supported_units)
    for unit, meters_per_unit in expected_meters_per_unit.items():
        assert registry.meters_per_unit(unit) == pytest.approx(meters_per_unit)

    source_unit, value = prd_s2_input
    results = convert_all(value, source_unit, registry)

    assert set(results.keys()) == set(supported_units)
    for unit, expected in expected_conversion_values.items():
        assert results[unit] == pytest.approx(expected)
