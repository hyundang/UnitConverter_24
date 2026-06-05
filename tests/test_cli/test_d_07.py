"""D-07 — PRD FR-4 · §8.2: --format json."""

import json

import pytest


@pytest.mark.prd_s4
def test_meter_2_5_outputs_json_with_three_units(
    run_cli, meter_2_5_stdin, expected_conversion_values, supported_units
):
    result = run_cli(["--format", "json"], meter_2_5_stdin)

    assert result.returncode == 0, result.stderr

    data = json.loads(result.stdout)
    for unit in supported_units:
        assert unit in data
        assert data[unit] == pytest.approx(expected_conversion_values[unit])
