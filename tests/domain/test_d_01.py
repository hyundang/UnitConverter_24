"""D-01 — PRD S2 · §8.1: meter:2.5 → all supported units."""

import pytest

from domain.conversion import convert_all
from tests import inputs


@pytest.mark.prd_s2
def test_meter_2_5_converts_to_all_supported_units(
    default_registry, supported_units, prd_s2_input
):
    source_unit, value = prd_s2_input

    results = convert_all(value, source_unit, default_registry)

    assert set(results.keys()) == set(supported_units)
    assert results["meter"] == pytest.approx(value)
    assert results["feet"] == pytest.approx(value * inputs.METER_TO_FEET)
    assert results["yard"] == pytest.approx(value * inputs.METER_TO_YARD)
