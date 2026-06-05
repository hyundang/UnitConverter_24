"""PRD §8.1 — conversion TC slots (S2)."""

from __future__ import annotations

import pytest


@pytest.mark.prd_s2
@pytest.mark.skip(reason="Harness skeleton — Test Loop Red")
def test_meter_value_converts_to_all_supported_units() -> None:
    """PRD §8.1 | `meter:2.5` → meter, feet, yard (structure or numeric assert)."""
