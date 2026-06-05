"""D-09 — PRD FR-4 · §8.2: default table output (D-01 equivalent)."""

import pytest

from tests.conftest import assert_default_table_output


@pytest.mark.prd_s4
def test_meter_2_5_outputs_default_table_lines(
    run_cli, meter_2_5_stdin, expected_conversion_values, supported_units
):
    result = run_cli([], meter_2_5_stdin)
    assert_default_table_output(result, expected_conversion_values, supported_units)
