"""Input string parsing — unit:value format (FR-1.0)."""

UNIT_VALUE_SEPARATOR = ":"


class FormatError(ValueError):
    """Raised when input does not match unit:value format."""


class NumberError(ValueError):
    """Raised when the value token is not numeric."""


def parse_unit_value(text: str) -> tuple[str, float]:
    if UNIT_VALUE_SEPARATOR not in text:
        raise FormatError(
            f"Invalid format. Expected {UNIT_VALUE_SEPARATOR.join(('unit', 'value'))}"
        )

    unit, value_token = text.split(UNIT_VALUE_SEPARATOR, 1)
    if not unit or not value_token:
        raise FormatError(
            f"Invalid format. Expected {UNIT_VALUE_SEPARATOR.join(('unit', 'value'))}"
        )

    try:
        value = float(value_token)
    except ValueError as exc:
        raise NumberError(f"Invalid number: {value_token}") from exc

    return unit, value
