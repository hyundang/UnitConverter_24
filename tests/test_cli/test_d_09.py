"""D-09 — PRD FR-4 · §8.2: default table output (D-01 equivalent)."""

import pytest

from tests import inputs
from tests.conftest import assert_default_table_output


@pytest.mark.prd_s4
def test_meter_2_5_outputs_default_grid_table(
    run_cli, meter_2_5_stdin, expected_conversion_values
):
    result = run_cli([], meter_2_5_stdin)
    assert_default_table_output(
        result, expected_conversion_values, inputs.PRD_S2_VALUE
    )
