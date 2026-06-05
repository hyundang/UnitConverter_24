"""CLI entry point. Run from repo root: python src/cli.py"""

import argparse
import json
import sys
from pathlib import Path

from application.formatting.output import format_csv, format_table
from application.parsing import FormatError
from application.use_cases import process_stdin_lines
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

    try:
        processed = process_stdin_lines(registry, lines)
    except FormatError as exc:
        print(exc, file=sys.stderr)
        return 1

    if processed is None:
        return 1

    unit, value, results = processed

    if args.format == FORMAT_JSON:
        print(json.dumps(results))
    elif args.format == FORMAT_CSV:
        print(format_csv(results), end="")
    else:
        print(format_table(unit, value, results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
