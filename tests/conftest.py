"""Shared pytest fixtures for UnitConverter_24 Test Loop."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests import inputs

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


def assert_default_table_output(result, expected_conversion_values, supported_units):
    assert result.returncode == 0, result.stderr

    lines = [line for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) == 3

    for unit in supported_units:
        matching = [line for line in lines if line.rstrip().endswith(unit)]
        assert len(matching) == 1
        assert "meter" in matching[0]
        assert "=" in matching[0]

    assert f"{expected_conversion_values['feet']:.4f}" in result.stdout
    assert f"{expected_conversion_values['yard']:.4f}" in result.stdout
    assert f"{expected_conversion_values['meter']:.1f}" in result.stdout


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
