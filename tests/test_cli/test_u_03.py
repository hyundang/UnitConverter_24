"""U-03 — PRD §9.6: CLI dynamic unit registration then conversion."""

import pytest


@pytest.mark.prd_s4
def test_cli_registers_cubit_then_converts(
    run_cli, prd_u03_stdin, expected_cubit_2_conversion_values
):
    result = run_cli([], prd_u03_stdin)

    assert result.returncode == 0, result.stderr

    output_lower = result.stdout.lower()
    assert "cubit" in output_lower

    for unit, expected in expected_cubit_2_conversion_values.items():
        assert f"{expected:.4f}" in result.stdout
