"""D-03 — PRD S1 · §8.1: inch:1 → unknown unit + hint (validation)."""

import pytest

from domain.validation import UnknownUnitError, validate_unit


@pytest.mark.prd_s1
def test_rejects_unknown_unit_with_supported_units_hint(
    default_registry, supported_units, prd_s1_unknown_parsed
):
    unit, _value = prd_s1_unknown_parsed

    with pytest.raises(UnknownUnitError) as exc_info:
        validate_unit(unit, default_registry)

    message = str(exc_info.value)
    assert "unknown unit" in message.lower()
    for supported in supported_units:
        assert supported in message
