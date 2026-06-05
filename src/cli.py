"""CLI entry point. Run from repo root: python src/cli.py"""

import argparse
import json
import sys
from pathlib import Path

from application.formatting.output import format_csv, format_table
from application.parsing import FormatError, NumberError
from application.use_cases import process_stdin_lines
from domain.validation import UnknownUnitError
from infrastructure.config_loader import load_registry

REPO_ROOT = Path(__file__).resolve().parent.parent
UNITS_CONFIG_PATH = REPO_ROOT / "config" / "units.json"
FORMAT_JSON = "json"
FORMAT_CSV = "csv"
FORMAT_TABLE = "table"


def _render_output(
    output_format: str, unit: str, value: float, results: dict[str, float]
) -> tuple[str, bool]:
    """Return rendered stdout and whether print should use end=''."""
    if output_format == FORMAT_JSON:
        return json.dumps(results), False
    if output_format == FORMAT_CSV:
        return format_csv(results), True
    return format_table(unit, value, results), False


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
    except (FormatError, NumberError, UnknownUnitError) as exc:
        print(exc, file=sys.stderr)
        return 1

    if processed is None:
        return 1

    unit, value, results = processed

    output, suppress_trailing_newline = _render_output(
        args.format, unit, value, results
    )
    print(output, end="" if suppress_trailing_newline else "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
