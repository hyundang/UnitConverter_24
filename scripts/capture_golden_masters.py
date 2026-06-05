"""Capture golden master files from the current green baseline.

Run from repo root (REFACTOR 전·동작 변경 후 재캡처 시):

    python scripts/capture_golden_masters.py

Writes under tests/golden/ and updates manifest.json.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = REPO_ROOT / "tests" / "golden"
CLI_DIR = GOLDEN_DIR / "cli"
DOMAIN_DIR = GOLDEN_DIR / "domain"
ERRORS_DIR = GOLDEN_DIR / "errors"
MANIFEST_PATH = GOLDEN_DIR / "manifest.json"

CLI_SCENARIOS = [
    {
        "name": "table_meter_2_5",
        "args": [],
        "stdin": "meter:2.5\n",
        "returncode": 0,
    },
    {
        "name": "json_meter_2_5",
        "args": ["--format", "json"],
        "stdin": "meter:2.5\n",
        "returncode": 0,
    },
    {
        "name": "csv_meter_2_5",
        "args": ["--format", "csv"],
        "stdin": "meter:2.5\n",
        "returncode": 0,
    },
    {
        "name": "u02_invalid_format",
        "args": [],
        "stdin": "meter\n",
        "returncode": 1,
    },
    {
        "name": "u03_register_cubit",
        "args": [],
        "stdin": "1 cubit = 0.4572 meter\ncubit:2\n",
        "returncode": 0,
    },
]


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode("utf-8"))


def _capture_cli() -> list[dict]:
    cli_command = [sys.executable, str(REPO_ROOT / "src" / "cli.py")]
    entries: list[dict] = []

    for scenario in CLI_SCENARIOS:
        result = subprocess.run(
            cli_command + scenario["args"],
            input=scenario["stdin"],
            text=True,
            capture_output=True,
            cwd=REPO_ROOT,
        )
        name = scenario["name"]
        stdout_path = f"cli/{name}.stdout.txt"
        stderr_path = f"cli/{name}.stderr.txt"
        rc_path = f"cli/{name}.rc"

        _write_text(GOLDEN_DIR / stdout_path, result.stdout)
        _write_text(GOLDEN_DIR / stderr_path, result.stderr)
        _write_text(GOLDEN_DIR / rc_path, str(result.returncode))

        entries.append(
            {
                "name": name,
                "kind": "cli",
                "args": scenario["args"],
                "stdin": scenario["stdin"],
                "returncode": result.returncode,
                "stdout": stdout_path,
                "stderr": stderr_path,
                "rc": rc_path,
            }
        )

    return entries


def _capture_domain_and_errors() -> list[dict]:
    sys.path.insert(0, str(REPO_ROOT))
    sys.path.insert(0, str(REPO_ROOT / "src"))

    from application.parsing import FormatError, NumberError, parse_unit_value
    from domain.conversion import convert_all
    from domain.registry import UnitRegistry
    from domain.validation import UnknownUnitError, validate_unit
    from tests import inputs

    entries: list[dict] = []

    registry = UnitRegistry()
    registry.register("meter", meters_per_unit=1.0)
    registry.register("feet", meters_per_unit=1.0 / inputs.METER_TO_FEET)
    registry.register("yard", meters_per_unit=1.0 / inputs.METER_TO_YARD)

    conversions = convert_all(inputs.PRD_S2_VALUE, inputs.PRD_S2_UNIT, registry)
    conversions_path = "domain/meter_2_5_conversions.json"
    _write_text(
        GOLDEN_DIR / conversions_path,
        json.dumps(conversions, sort_keys=True, indent=2) + "\n",
    )
    entries.append(
        {
            "name": "meter_2_5_conversions",
            "kind": "domain",
            "input_unit": inputs.PRD_S2_UNIT,
            "input_value": inputs.PRD_S2_VALUE,
            "output": conversions_path,
        }
    )

    error_cases = [
        ("format_invalid_meter", lambda: parse_unit_value(inputs.PRD_S1_FORMAT_INPUT), FormatError),
        ("number_invalid_abc", lambda: parse_unit_value(inputs.PRD_S1_NUMBER_INPUT), NumberError),
        (
            "unknown_unit_inch",
            lambda: validate_unit(inputs.PRD_S1_UNKNOWN_UNIT, registry),
            UnknownUnitError,
        ),
    ]

    for name, action, expected_type in error_cases:
        try:
            action()
            raise RuntimeError(f"Expected {expected_type.__name__} for {name}")
        except expected_type as exc:
            message = str(exc)

        message_path = f"errors/{name}.txt"
        _write_text(GOLDEN_DIR / message_path, message + "\n")
        entries.append(
            {
                "name": name,
                "kind": "error_message",
                "exception": expected_type.__name__,
                "message": message_path,
            }
        )

    return entries


def main() -> int:
    CLI_DIR.mkdir(parents=True, exist_ok=True)
    DOMAIN_DIR.mkdir(parents=True, exist_ok=True)
    ERRORS_DIR.mkdir(parents=True, exist_ok=True)

    scenarios = _capture_cli() + _capture_domain_and_errors()
    manifest = {
        "version": 1,
        "description": "REFACTOR baseline — regenerate with scripts/capture_golden_masters.py",
        "scenarios": scenarios,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(scenarios)} scenarios to {GOLDEN_DIR.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
