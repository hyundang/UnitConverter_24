"""PRD §8.1 — validation TC slots (S1)."""

from __future__ import annotations

import pytest


@pytest.mark.prd_s1
@pytest.mark.skip(reason="Harness skeleton — Test Loop Red")
def test_rejects_missing_colon_format() -> None:
    """PRD §8.1 | `meter` → format error, exit."""


@pytest.mark.prd_s1
@pytest.mark.skip(reason="Harness skeleton — Test Loop Red")
def test_rejects_unknown_unit() -> None:
    """PRD §8.1 | `inch:1` → unknown unit + supported hint."""


@pytest.mark.prd_s1
@pytest.mark.skip(reason="Harness skeleton — Test Loop Red")
def test_rejects_non_numeric_value() -> None:
    """PRD §8.1 | `meter:abc` → number error."""
