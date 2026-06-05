"""D-06 — PRD FR-5 · §8.2: register cubit then cubit:1 converts to all units."""

import pytest

from application.use_cases import register_unit_from_string
from domain.conversion import convert_all


@pytest.mark.prd_s4
def test_register_cubit_then_converts_to_all_units(
    default_registry,
    prd_fr5_register_input,
    prd_fr5_input,
    expected_cubit_conversion_values,
):
    register_unit_from_string(default_registry, prd_fr5_register_input)

    source_unit, value = prd_fr5_input
    results = convert_all(value, source_unit, default_registry)

    assert set(results.keys()) == set(expected_cubit_conversion_values.keys())
    for unit, expected in expected_cubit_conversion_values.items():
        assert results[unit] == pytest.approx(expected)
