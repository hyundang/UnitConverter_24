"""U-01 — PRD §9.1: CLI happy path meter:2.5."""

import pytest


@pytest.mark.prd_s2
def test_cli_happy_path_meter_2_5_outputs_three_lines(
    run_cli, prd_s2_stdin_input, expected_conversion_values, supported_units
):
    result = run_cli([], prd_s2_stdin_input)

    assert result.returncode == 0, result.stderr

    lines = [line for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) == 3

    for unit in supported_units:
        matching = [line for line in lines if unit in line]
        assert len(matching) == 1
        assert "meter" in matching[0]
        assert "=" in matching[0]

    assert f"{expected_conversion_values['feet']:.4f}" in result.stdout
    assert f"{expected_conversion_values['yard']:.4f}" in result.stdout
    assert f"{expected_conversion_values['meter']:.1f}" in result.stdout
