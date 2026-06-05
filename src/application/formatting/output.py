"""Output formatting — JSON-adjacent table/CSV (FR-4)."""

import csv
import io

CSV_VALUE_DECIMALS = 4
TABLE_SOURCE_DECIMALS = 1
TABLE_OTHER_UNIT_DECIMALS = 4
TABLE_UNIT_COL_WIDTH = 7
TABLE_INPUT_COL_WIDTH = 7
TABLE_VALUE_COL_WIDTH = 8
TABLE_BORDER = "+-------+-------+--------+"
TABLE_HEADER_ROW = "| unit  | input | value  |"
CSV_UNIT_HEADER = "unit"
CSV_VALUE_HEADER = "value"


def format_csv(results: dict[str, float]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([CSV_UNIT_HEADER, CSV_VALUE_HEADER])
    for unit, converted in results.items():
        writer.writerow([unit, f"{converted:.{CSV_VALUE_DECIMALS}f}"])
    return buffer.getvalue()


def _format_table_unit_cell(unit: str) -> str:
    return f" {unit}".ljust(TABLE_UNIT_COL_WIDTH)


def _format_table_input_cell(source_value: float) -> str:
    text = f"{source_value:.{TABLE_SOURCE_DECIMALS}f}"
    return text.rjust(TABLE_INPUT_COL_WIDTH - 1) + " "


def _format_table_value_cell(
    converted: float, target_unit: str, source_unit: str, source_value: float
) -> str:
    if target_unit == source_unit:
        text = f"{source_value:.{TABLE_SOURCE_DECIMALS}f}"
    else:
        text = f"{converted:.{TABLE_OTHER_UNIT_DECIMALS}f}"
    return text.rjust(TABLE_VALUE_COL_WIDTH - 1) + " "


def _format_table_data_row(
    unit: str, source_value: float, converted: float, source_unit: str
) -> str:
    unit_cell = _format_table_unit_cell(unit)
    input_cell = _format_table_input_cell(source_value)
    value_cell = _format_table_value_cell(converted, unit, source_unit, source_value)
    return f"|{unit_cell}|{input_cell}|{value_cell}|"


def format_table(
    source_unit: str, source_value: float, results: dict[str, float]
) -> str:
    lines = [
        TABLE_BORDER,
        TABLE_HEADER_ROW,
        TABLE_BORDER,
    ]
    for target_unit, converted in results.items():
        lines.append(
            _format_table_data_row(target_unit, source_value, converted, source_unit)
        )
    lines.append(TABLE_BORDER)
    return "\n".join(lines)
