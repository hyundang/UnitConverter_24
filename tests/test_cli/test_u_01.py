"""U-01 — PRD §9.1: CLI happy path meter:2.5."""

import pytest

from tests import inputs
from tests.conftest import assert_default_table_output


@pytest.mark.prd_s2
def test_cli_happy_path_meter_2_5_outputs_grid_table(
    run_cli, meter_2_5_stdin, expected_conversion_values
):
    result = run_cli([], meter_2_5_stdin)
    assert_default_table_output(
        result, expected_conversion_values, inputs.PRD_S2_VALUE
    )
