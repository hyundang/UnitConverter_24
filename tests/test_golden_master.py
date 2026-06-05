"""Golden master regression — REFACTOR baseline (동작·출력 고정).

재캡처: python scripts/capture_golden_masters.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from application.parsing import FormatError, NumberError, parse_unit_value
from domain.conversion import convert_all
from domain.validation import UnknownUnitError, validate_unit
from tests import inputs

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"
MANIFEST_PATH = GOLDEN_DIR / "manifest.json"

ERROR_TYPES = {
    "FormatError": FormatError,
    "NumberError": NumberError,
    "UnknownUnitError": UnknownUnitError,
}


def _load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _read_golden(relative_path: str) -> str:
    return (GOLDEN_DIR / relative_path).read_text(encoding="utf-8")


def _cli_scenarios() -> list[dict]:
    return [s for s in _load_manifest()["scenarios"] if s["kind"] == "cli"]


@pytest.mark.parametrize(
    "scenario",
    _cli_scenarios(),
    ids=[s["name"] for s in _cli_scenarios()],
)
def test_golden_cli_output_matches_baseline(scenario, run_cli):
    result = run_cli(scenario["args"], scenario["stdin"])

    assert result.returncode == int(_read_golden(scenario["rc"]).strip())
    assert result.stdout == _read_golden(scenario["stdout"])
    assert result.stderr == _read_golden(scenario["stderr"])


def test_golden_domain_meter_2_5_conversions(default_registry):
    scenario = next(
        s for s in _load_manifest()["scenarios"] if s["name"] == "meter_2_5_conversions"
    )
    expected = json.loads(_read_golden(scenario["output"]))

    results = convert_all(
        scenario["input_value"],
        scenario["input_unit"],
        default_registry,
    )

    assert results == expected


@pytest.mark.parametrize(
    "scenario",
    [s for s in _load_manifest()["scenarios"] if s["kind"] == "error_message"],
    ids=[s["name"] for s in _load_manifest()["scenarios"] if s["kind"] == "error_message"],
)
def test_golden_error_messages_match_baseline(scenario, default_registry):
    expected = _read_golden(scenario["message"]).rstrip("\n")
    exc_type = ERROR_TYPES[scenario["exception"]]

    if scenario["name"] == "format_invalid_meter":
        with pytest.raises(exc_type) as exc_info:
            parse_unit_value(inputs.PRD_S1_FORMAT_INPUT)
    elif scenario["name"] == "number_invalid_abc":
        with pytest.raises(exc_type) as exc_info:
            parse_unit_value(inputs.PRD_S1_NUMBER_INPUT)
    elif scenario["name"] == "unknown_unit_inch":
        with pytest.raises(exc_type) as exc_info:
            validate_unit(inputs.PRD_S1_UNKNOWN_UNIT, default_registry)
    else:
        pytest.fail(f"Unhandled golden error scenario: {scenario['name']}")

    assert str(exc_info.value) == expected
