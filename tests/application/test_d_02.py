"""D-02 — PRD S1 · §8.1: meter → format error (parsing)."""

import pytest

from application.parsing import FormatError, parse_unit_value


@pytest.mark.prd_s1
def test_rejects_missing_colon_format(prd_s1_format_input):
    with pytest.raises(FormatError) as exc_info:
        parse_unit_value(prd_s1_format_input)

    message = str(exc_info.value)
    assert "invalid format" in message.lower()
    assert "unit:value" in message
