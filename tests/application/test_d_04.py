"""D-04 — PRD S1 · §8.1: meter:abc → number error (parsing)."""

import pytest

from application.parsing import NumberError, parse_unit_value


@pytest.mark.prd_s1
def test_rejects_non_numeric_value_token(prd_s1_number_input):
    with pytest.raises(NumberError) as exc_info:
        parse_unit_value(prd_s1_number_input)

    assert "abc" in str(exc_info.value)
