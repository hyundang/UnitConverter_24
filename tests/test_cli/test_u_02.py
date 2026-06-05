"""U-02 — PRD §9.2 · S1: CLI invalid format message and hint."""

import pytest


@pytest.mark.prd_s1
def test_cli_rejects_invalid_format_with_hint(run_cli, u02_invalid_format_input):
    result = run_cli([], u02_invalid_format_input)

    output = f"{result.stdout}\n{result.stderr}"
    assert result.returncode != 0
    assert "invalid format" in output.lower()
    assert "unit:value" in output.lower()
