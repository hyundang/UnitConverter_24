"""Input string parsing — unit:value and unit registration (FR-1.0, FR-5.1)."""

from domain.constants import REFERENCE_UNIT

UNIT_VALUE_SEPARATOR = ":"
REGISTER_EQUALS = "="

class FormatError(ValueError):
    """Raised when input does not match unit:value format."""


class NumberError(ValueError):
    """Raised when the value token is not numeric."""


def _unit_value_format_error() -> FormatError:
    expected = UNIT_VALUE_SEPARATOR.join(("unit", "value"))
    return FormatError(f"Invalid format. Expected {expected}")


def _registration_format_error() -> FormatError:
    return FormatError(f"Invalid format. Expected 1 unit = ratio {REFERENCE_UNIT}")


def _parse_quantity_side(quantity_unit: str) -> tuple[str, str]:
    quantity_parts = quantity_unit.split(None, 1)
    if len(quantity_parts) != 2 or not quantity_parts[0] or not quantity_parts[1]:
        raise _registration_format_error()
    return quantity_parts[0], quantity_parts[1]


def _parse_meters_quantity_token(meters_side: str) -> str:
    meters_parts = meters_side.split()
    if len(meters_parts) != 2 or meters_parts[1] != REFERENCE_UNIT:
        raise _registration_format_error()
    return meters_parts[0]


def parse_unit_value(text: str) -> tuple[str, float]:
    if UNIT_VALUE_SEPARATOR not in text:
        raise _unit_value_format_error()

    unit, value_token = text.split(UNIT_VALUE_SEPARATOR, 1)
    if not unit or not value_token:
        raise _unit_value_format_error()

    try:
        value = float(value_token)
    except ValueError as exc:
        raise NumberError(f"Invalid number: {value_token}") from exc

    return unit, value


def parse_register_unit(text: str) -> tuple[str, float]:
    if REGISTER_EQUALS not in text:
        raise _registration_format_error()

    quantity_unit, meters_side = text.split(REGISTER_EQUALS, 1)
    quantity_token, unit_name = _parse_quantity_side(quantity_unit.strip())
    meters_token = _parse_meters_quantity_token(meters_side.strip())

    try:
        quantity = float(quantity_token)
        meters_quantity = float(meters_token)
    except ValueError as exc:
        raise NumberError(f"Invalid number in registration: {text}") from exc

    meters_per_unit = meters_quantity / quantity
    return unit_name, meters_per_unit
