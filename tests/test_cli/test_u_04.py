"""U-04 — PRD §9.7 · NFR-5: CLI three formats share same conversion values."""

import json

import pytest


@pytest.mark.prd_s4
def test_cli_three_formats_share_same_conversion_values(
    run_cli, prd_s2_stdin_input, expected_conversion_values, supported_units
):
    table_result = run_cli([], prd_s2_stdin_input)
    json_result = run_cli(["--format", "json"], prd_s2_stdin_input)
    csv_result = run_cli(["--format", "csv"], prd_s2_stdin_input)

    assert table_result.returncode == 0, table_result.stderr
    assert json_result.returncode == 0, json_result.stderr
    assert csv_result.returncode == 0, csv_result.stderr

    data = json.loads(json_result.stdout)
    for unit in supported_units:
        assert unit in data
        assert data[unit] == pytest.approx(expected_conversion_values[unit])

    for unit, expected in expected_conversion_values.items():
        assert f"{expected:.4f}" in table_result.stdout
        assert f"{expected:.4f}" in csv_result.stdout
