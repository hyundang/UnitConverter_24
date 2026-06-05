"""Shared pytest fixtures for UnitConverter_24 Test Loop."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests import inputs

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def supported_units():
    return list(inputs.SUPPORTED_UNITS)


@pytest.fixture
def default_registry():
    from domain.registry import UnitRegistry

    registry = UnitRegistry()
    registry.register("meter", meters_per_unit=1.0)
    registry.register("feet", meters_per_unit=1.0 / inputs.METER_TO_FEET)
    registry.register("yard", meters_per_unit=1.0 / inputs.METER_TO_YARD)
    return registry


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
def prd_s2_stdin_input():
    return inputs.PRD_S4_INPUT


@pytest.fixture
def expected_conversion_values():
    value = inputs.PRD_S2_VALUE
    return {
        "meter": value,
        "feet": value * inputs.METER_TO_FEET,
        "yard": value * inputs.METER_TO_YARD,
    }


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
    value = inputs.PRD_FR5_VALUE
    meters = value * inputs.CUBIT_METERS_PER_UNIT
    return {
        "cubit": value,
        "meter": meters,
        "feet": meters * inputs.METER_TO_FEET,
        "yard": meters * inputs.METER_TO_YARD,
    }


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
    value = inputs.S3_MOCK_VALUE
    meters = value * inputs.S3_MOCK_METERS_PER_UNIT
    return {
        inputs.S3_MOCK_UNIT: value,
        "meter": meters,
        "feet": meters * inputs.METER_TO_FEET,
        "yard": meters * inputs.METER_TO_YARD,
    }


@pytest.fixture
def u02_invalid_format_input():
    return inputs.U02_INVALID_FORMAT


@pytest.fixture
def prd_u03_stdin():
    return inputs.PRD_U03_STDIN


@pytest.fixture
def expected_cubit_2_conversion_values():
    value = inputs.PRD_U03_VALUE
    meters = value * inputs.CUBIT_METERS_PER_UNIT
    return {
        "cubit": value,
        "meter": meters,
        "feet": meters * inputs.METER_TO_FEET,
        "yard": meters * inputs.METER_TO_YARD,
    }
