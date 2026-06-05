"""CLI entry point. Run from repo root: python src/cli.py"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

from application.parsing import parse_unit_value
from domain.conversion import convert_all
from domain.validation import validate_unit
from infrastructure.config_loader import load_registry

REPO_ROOT = Path(__file__).resolve().parent.parent
UNITS_CONFIG_PATH = REPO_ROOT / "config" / "units.json"
FORMAT_JSON = "json"
FORMAT_CSV = "csv"
FORMAT_TABLE = "table"
CSV_VALUE_DECIMALS = 4
TABLE_SOURCE_DECIMALS = 1
TABLE_SAME_UNIT_DECIMALS = 1
TABLE_OTHER_UNIT_DECIMALS = 4
TABLE_EQUALS = "="
CSV_UNIT_HEADER = "unit"
CSV_VALUE_HEADER = "value"


def _format_csv(results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([CSV_UNIT_HEADER, CSV_VALUE_HEADER])
    for unit, converted in results.items():
        writer.writerow([unit, f"{converted:.{CSV_VALUE_DECIMALS}f}"])
    return buffer.getvalue()


def _format_table(
    source_unit: str, source_value: float, results: dict[str, float]
) -> str:
    source_display = f"{source_value:.{TABLE_SOURCE_DECIMALS}f}"
    lines: list[str] = []
    for target_unit, converted in results.items():
        if target_unit == source_unit:
            converted_display = f"{converted:.{TABLE_SAME_UNIT_DECIMALS}f}"
        else:
            converted_display = f"{converted:.{TABLE_OTHER_UNIT_DECIMALS}f}"
        lines.append(
            f"{source_display} {source_unit} {TABLE_EQUALS} "
            f"{converted_display} {target_unit}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default="table")
    args = parser.parse_args(argv)

    if args.format not in (FORMAT_JSON, FORMAT_CSV, FORMAT_TABLE):
        return 1

    line = sys.stdin.read().strip()
    registry = load_registry(UNITS_CONFIG_PATH)
    unit, value = parse_unit_value(line)
    validate_unit(unit, registry)
    results = convert_all(value, unit, registry)

    if args.format == FORMAT_JSON:
        print(json.dumps(results))
    elif args.format == FORMAT_CSV:
        print(_format_csv(results), end="")
    else:
        print(_format_table(unit, value, results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
