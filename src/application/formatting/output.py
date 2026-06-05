"""Output formatting — JSON-adjacent table/CSV (FR-4)."""

import csv
import io

CSV_VALUE_DECIMALS = 4
TABLE_SOURCE_DECIMALS = 1
TABLE_SAME_UNIT_DECIMALS = 4
TABLE_OTHER_UNIT_DECIMALS = 4
TABLE_EQUALS = "="
CSV_UNIT_HEADER = "unit"
CSV_VALUE_HEADER = "value"


def format_csv(results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([CSV_UNIT_HEADER, CSV_VALUE_HEADER])
    for unit, converted in results.items():
        writer.writerow([unit, f"{converted:.{CSV_VALUE_DECIMALS}f}"])
    return buffer.getvalue()


def format_table(
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
