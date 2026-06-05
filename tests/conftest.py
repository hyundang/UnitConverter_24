"""Shared pytest fixtures for UnitConverter_24 Test Loop."""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from application.formatting.output import TABLE_BORDER, TABLE_HEADER_ROW
from tests import inputs

TABLE_HEADERS = ("unit", "input", "value")
INPUT_NUMERIC = re.compile(r"^\d+(\.\d+)?$")

REPO_ROOT = Path(__file__).resolve().parent.parent


def _expected_conversion_values(
    source_unit: str, value: float, meters_per_unit: float
) -> dict[str, float]:
    value_in_meters = value * meters_per_unit
    results = {source_unit: value}
    if source_unit != "meter":
        results["meter"] = value_in_meters
    if source_unit != "feet":
        results["feet"] = value_in_meters * inputs.METER_TO_FEET
    if source_unit != "yard":
        results["yard"] = value_in_meters * inputs.METER_TO_YARD
    return results


@pytest.fixture
def supported_units():
    return list(inputs.SUPPORTED_UNITS)


@pytest.fixture
def default_registry(units_config_path):
    from infrastructure.config_loader import load_registry

    return load_registry(units_config_path)


@pytest.fixture
def prd_s2_input():
    return inputs.PRD_S2_UNIT, inputs.PRD_S2_VALUE


@pytest.fixture
def prd_s1_format_input():
    return inputs.PRD_S1_FORMAT_INPUT


@pytest.fixture
def prd_s1_number_input():
    return inputs.PRD_S1_NUMBER_INPUT


@pytest.fixture
def prd_s1_unknown_parsed():
    return inputs.PRD_S1_UNKNOWN_UNIT, inputs.PRD_S1_UNKNOWN_VALUE


@pytest.fixture
def cli_command():
    return [sys.executable, str(REPO_ROOT / "src" / "cli.py")]


@pytest.fixture
def meter_2_5_stdin():
    return inputs.PRD_S2_INPUT


@pytest.fixture
def expected_conversion_values():
    return _expected_conversion_values(
        inputs.PRD_S2_UNIT,
        inputs.PRD_S2_VALUE,
        meters_per_unit=1.0,
    )


@pytest.fixture
def run_cli(cli_command):
    def _run(extra_args=None, stdin_text=""):
        args = list(cli_command)
        if extra_args:
            args.extend(extra_args)
        return subprocess.run(
            args,
            input=stdin_text,
            text=True,
            capture_output=True,
            cwd=REPO_ROOT,
        )

    return _run


def _is_table_border_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and set(stripped) <= {"+", "-", "|", " "}


def _is_table_header_line(line: str) -> bool:
    lower = line.lower()
    return all(header in lower for header in TABLE_HEADERS)


def _assert_grid_table_structure(stdout: str) -> None:
    lines = stdout.splitlines()
    assert len(lines) >= 4, f"expected bordered grid table, got {len(lines)} lines"
    assert lines[0] == TABLE_BORDER
    assert lines[1] == TABLE_HEADER_ROW
    assert lines[2] == TABLE_BORDER
    assert lines[-1] == TABLE_BORDER
    for line in lines[3:-1]:
        assert line.startswith("|") and line.endswith("|"), (
            f"expected data row with pipe borders: {line!r}"
        )


def _parse_table_data_rows(stdout: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped or _is_table_border_line(stripped) or _is_table_header_line(stripped):
            continue
        if "|" not in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) == 3 and cells[0] and INPUT_NUMERIC.match(cells[1]):
            rows.append({"unit": cells[0], "input": cells[1], "value": cells[2]})
    return rows


def assert_default_table_output(result, expected_conversion_values, source_value):
    assert result.returncode == 0, result.stderr

    _assert_grid_table_structure(result.stdout)

    rows = _parse_table_data_rows(result.stdout)
    assert len(rows) == len(expected_conversion_values), (
        f"expected {len(expected_conversion_values)} data rows, got {len(rows)}"
    )

    by_unit = {row["unit"]: row for row in rows}
    for unit, expected in expected_conversion_values.items():
        assert unit in by_unit, f"missing row for unit: {unit}"
        row = by_unit[unit]

        assert INPUT_NUMERIC.match(row["input"]), (
            f"input must be numeric only: {row['input']!r}"
        )
        assert float(row["input"]) == pytest.approx(source_value)

        assert INPUT_NUMERIC.match(row["value"]), (
            f"value must be numeric only: {row['value']!r}"
        )
        assert float(row["value"]) == pytest.approx(expected, rel=1e-4)


@pytest.fixture
def units_config_path():
    return REPO_ROOT / "config" / "units.json"


@pytest.fixture
def expected_meters_per_unit():
    return {
        "meter": 1.0,
        "feet": 1.0 / inputs.METER_TO_FEET,
        "yard": 1.0 / inputs.METER_TO_YARD,
    }


@pytest.fixture
def readme_units_json(tmp_path, expected_meters_per_unit):
    config = {
        "units": {
            unit: {"meters_per_unit": meters_per_unit}
            for unit, meters_per_unit in expected_meters_per_unit.items()
        }
    }
    path = tmp_path / "units.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


@pytest.fixture
def prd_fr5_register_input():
    return inputs.PRD_FR5_REGISTER_INPUT


@pytest.fixture
def prd_fr5_input():
    return inputs.PRD_FR5_UNIT, inputs.PRD_FR5_VALUE


@pytest.fixture
def expected_cubit_conversion_values():
    return _expected_conversion_values(
        inputs.PRD_FR5_UNIT,
        inputs.PRD_FR5_VALUE,
        inputs.CUBIT_METERS_PER_UNIT,
    )


@pytest.fixture
def registry_with_fathom(default_registry):
    default_registry.register(
        inputs.S3_MOCK_UNIT,
        meters_per_unit=inputs.S3_MOCK_METERS_PER_UNIT,
    )
    return default_registry


@pytest.fixture
def s3_mock_input():
    return inputs.S3_MOCK_UNIT, inputs.S3_MOCK_VALUE


@pytest.fixture
def expected_fathom_conversion_values():
    return _expected_conversion_values(
        inputs.S3_MOCK_UNIT,
        inputs.S3_MOCK_VALUE,
        inputs.S3_MOCK_METERS_PER_UNIT,
    )


@pytest.fixture
def u02_invalid_format_input():
    return inputs.U02_INVALID_FORMAT


@pytest.fixture
def prd_u03_stdin():
    return inputs.PRD_U03_STDIN


@pytest.fixture
def expected_cubit_2_conversion_values():
    return _expected_conversion_values(
        inputs.PRD_FR5_UNIT,
        inputs.PRD_U03_VALUE,
        inputs.CUBIT_METERS_PER_UNIT,
    )
