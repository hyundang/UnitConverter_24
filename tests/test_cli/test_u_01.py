"""U-01 — PRD §9.1: CLI happy path meter:2.5."""

import pytest

from tests.conftest import assert_default_table_output


@pytest.mark.prd_s2
def test_cli_happy_path_meter_2_5_outputs_three_lines(
    run_cli, prd_s2_stdin_input, expected_conversion_values, supported_units
):
    result = run_cli([], prd_s2_stdin_input)
    assert_default_table_output(result, expected_conversion_values, supported_units)
