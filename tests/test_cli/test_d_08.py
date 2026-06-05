"""D-08 — PRD FR-4 · §8.2: --format csv."""

import csv
import io

import pytest


@pytest.mark.prd_s4
def test_meter_2_5_outputs_csv_with_header_and_rows(
    run_cli, prd_s2_stdin_input, expected_conversion_values, supported_units
):
    result = run_cli(["--format", "csv"], prd_s2_stdin_input)

    assert result.returncode == 0, result.stderr

    lines = [line for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) >= 4
    assert "," in lines[0]

    rows = list(csv.DictReader(io.StringIO(result.stdout)))
    assert len(rows) >= 3

    output_lower = result.stdout.lower()
    for unit in supported_units:
        assert unit in output_lower

    for unit, expected in expected_conversion_values.items():
        assert f"{expected:.4f}" in result.stdout
