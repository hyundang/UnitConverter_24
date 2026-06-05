"""D-10 — PRD S3 · FR-3: one unit add · OCP registry extension."""

import pytest

from domain.conversion import convert_all


@pytest.mark.prd_s3
def test_adding_one_unit_enables_conversion_without_logic_change(
    registry_with_fathom,
    s3_mock_input,
    expected_fathom_conversion_values,
    prd_s2_input,
    expected_conversion_values,
):
    source_unit, value = s3_mock_input
    results = convert_all(value, source_unit, registry_with_fathom)

    assert set(results.keys()) == set(expected_fathom_conversion_values.keys())
    for unit, expected in expected_fathom_conversion_values.items():
        assert results[unit] == pytest.approx(expected)

    meter_unit, meter_value = prd_s2_input
    regression = convert_all(meter_value, meter_unit, registry_with_fathom)
    for unit, expected in expected_conversion_values.items():
        assert regression[unit] == pytest.approx(expected)
