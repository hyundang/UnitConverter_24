"""U-02 — PRD §9.2 · S1: CLI invalid format message and hint."""

import pytest

from tests import inputs


@pytest.mark.prd_s1
def test_cli_rejects_invalid_format_with_hint(run_cli, u02_invalid_format_input):
    result = run_cli([], u02_invalid_format_input)

    output = f"{result.stdout}\n{result.stderr}"
    assert result.returncode != 0
    assert "invalid format" in output.lower()
    assert "unit:value" in output.lower()


@pytest.mark.prd_s1
def test_cli_rejects_non_numeric_value_with_message(run_cli, prd_s1_number_input):
    result = run_cli([], prd_s1_number_input)

    assert result.returncode != 0
    assert result.stderr.strip() == "Invalid number: abc"
    assert result.stdout == ""


@pytest.mark.prd_s1
def test_cli_rejects_unknown_unit_with_supported_units_hint(run_cli):
    result = run_cli([], inputs.PRD_S1_UNKNOWN_INPUT)

    assert result.returncode != 0
    assert (
        result.stderr.strip()
        == "unknown unit: inch. Supported units: meter, feet, yard"
    )
    assert result.stdout == ""
