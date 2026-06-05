"""U-03 — PRD §9.6: CLI dynamic unit registration then conversion."""

import pytest

from tests import inputs
from tests.conftest import assert_default_table_output


@pytest.mark.prd_s4
def test_cli_registers_cubit_then_converts(
    run_cli, prd_u03_stdin, expected_cubit_2_conversion_values
):
    result = run_cli([], prd_u03_stdin)

    assert_default_table_output(
        result, expected_cubit_2_conversion_values, inputs.PRD_U03_VALUE
    )
