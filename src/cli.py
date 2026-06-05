"""CLI entry point. Run from repo root: python src/cli.py"""

import argparse
import json
import sys
from pathlib import Path

from application.formatting.output import format_csv, format_table
from application.parsing import (
    REGISTER_EQUALS,
    FormatError,
    parse_unit_value,
)
from application.use_cases import register_unit_from_string
from domain.conversion import convert_all
from domain.validation import validate_unit
from infrastructure.config_loader import load_registry

REPO_ROOT = Path(__file__).resolve().parent.parent
UNITS_CONFIG_PATH = REPO_ROOT / "config" / "units.json"
FORMAT_JSON = "json"
FORMAT_CSV = "csv"
FORMAT_TABLE = "table"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default="table")
    args = parser.parse_args(argv)

    if args.format not in (FORMAT_JSON, FORMAT_CSV, FORMAT_TABLE):
        return 1

    registry = load_registry(UNITS_CONFIG_PATH)
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]

    unit: str | None = None
    value: float | None = None
    results: dict[str, float] | None = None

    for line in lines:
        if REGISTER_EQUALS in line:
            register_unit_from_string(registry, line)
            continue

        try:
            unit, value = parse_unit_value(line)
        except FormatError as exc:
            print(exc, file=sys.stderr)
            return 1

        validate_unit(unit, registry)
        results = convert_all(value, unit, registry)

    if results is None or unit is None or value is None:
        return 1

    if args.format == FORMAT_JSON:
        print(json.dumps(results))
    elif args.format == FORMAT_CSV:
        print(format_csv(results), end="")
    else:
        print(format_table(unit, value, results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
