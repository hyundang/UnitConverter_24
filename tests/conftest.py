"""Shared pytest fixtures for UnitConverter_24 Test Loop."""

from __future__ import annotations

import pytest

from tests import inputs


@pytest.fixture
def prd_inputs() -> type[inputs]:
    """PRD §8.1 input constants."""
    return inputs


@pytest.fixture
def supported_units() -> tuple[str, ...]:
    """IS-2 baseline units (registry surface placeholder)."""
    return ("meter", "feet", "yard")
