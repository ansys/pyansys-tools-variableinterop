from typing import Any

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import IntegerValue


@pytest.mark.parametrize(
    "arg,expect_equality,expect_exception",
    [
        pytest.param(0, numpy.int64(0), None, id="zero"),
        pytest.param(1, numpy.int64(1), None, id="one"),
        pytest.param(-1, numpy.int64(-1), None, id="negative-one"),
        pytest.param(9223372036854775807, numpy.int64(9223372036854775807), None, id="max"),
        pytest.param(-9223372036854775808, numpy.int64(-9223372036854775808), None, id="min"),
        pytest.param(9223372036854775808, None, OverflowError, id="max+1"),
        pytest.param(-9223372036854775809, None, OverflowError, id="min-1"),
        pytest.param(1.4, numpy.int64(1), None, id="1.4-to-1"),

        # TODO: Should we override the numpy behavior for any of these cases?
        pytest.param(None, None, TypeError, id="None"),
        pytest.param(1.6, numpy.int64(1), None, id="1.6-to-1"),
        pytest.param(True, numpy.int64(1), None, id="True-to-1"),
        pytest.param(False, numpy.int64(0), None, id="False-to-0"),

        # TODO: Should we support string representations at all?
        # Should we pass-through to numpy, mimic fromAPIString, mimic fromFormattedString?
        pytest.param('some garbage text', None, ValueError, id="garbage-text"),
        pytest.param('-1', numpy.int64(-1), None, id="negative-one-text"),
        pytest.param('1', numpy.int64(1), None, id="one-text"),
    ])
def test_construct(arg: Any, expect_equality: numpy.int64, expect_exception: BaseException) -> None:
    """Verify that __init__ for IntegerValue correctly instantiates the superclass data."""
    with _create_exception_context(expect_exception):
        instance = IntegerValue(arg)

        if expect_exception is None:
            assert instance == expect_equality


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param('0', IntegerValue(0), id='zero'),
        pytest.param('1', IntegerValue(1), id='one'),
        pytest.param('-1', IntegerValue(-1), id='negative one'),
        pytest.param('+42', IntegerValue(42), id='explicit positive'),
        pytest.param('8675309', IntegerValue(8675309), id='larger'),
        pytest.param('047', IntegerValue(47), id='leading zero'),
        pytest.param('1.2E2', IntegerValue(120), id='scientific notation, whole'),
        pytest.param('-1.2E2', IntegerValue(-120), id='scientific notation, whole, negative'),
        pytest.param('1.2e+2', IntegerValue(120),
                     id='scientific notation, lowercase e, explicit positive exponent'),
        pytest.param('\t\n\r 8675309', IntegerValue(8675309), id='leading whitespace'),
        pytest.param('8675309 \t\n\r', IntegerValue(8675309), id='trailing whitespace'),
        pytest.param('\r\n\t 8675309 \t\n\r', IntegerValue(8675309),
                     id='leading and trailing whitespace'),
        pytest.param('9223372036854775807', IntegerValue(9223372036854775807),
                     id='max 64 bit'),
        pytest.param('-9223372036854775808', IntegerValue(-9223372036854775808),
                     id='min 64 bit'),
        pytest.param('9.223372036854775200E+18', IntegerValue(9223372036854774784),
                     id='largest float'),
        pytest.param('-9.223372036854776000E+18', IntegerValue(-9223372036854775808),
                     id='smallest float'),
        # non-integral numbers with decimals should be rounded
        pytest.param('1.5', IntegerValue(2), id='rounding, to even'),
        # rounding should occur away from zero, not to the nearest even
        pytest.param('2.5', IntegerValue(3), id='rounding, to odd'),
        # rounding should occur away from zero, not strictly up
        pytest.param('-1.5', IntegerValue(-2), id='rounding, to odd, negative'),
        # rounding should occur away from zero, not to the nearest even
        pytest.param('-2.5', IntegerValue(-3), id='rounding, to even, negative')
    ]
)
def test_from_api_string_valid(source: str, expected_result: IntegerValue) -> None:
    """
    Verify that valid cases work on IntegerValue.from_api_string

    Parameters
    ----------
    source the string to parse
    expected_result the expected result
    """
    # Execute
    result: IntegerValue = IntegerValue.from_api_string(source)

    # Verify
    assert isinstance(result, IntegerValue)
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param('complete garbage', ValueError, id="complete garbage"),
        pytest.param('', ValueError, id="empty string"),
        pytest.param('    ', ValueError, id="whitespace only"),
        pytest.param('2.2.2', ValueError, id="too many decimals"),
        pytest.param('9.223372036854775300E+18', OverflowError, id="valid float over max int"),
        pytest.param('-9.223372036854777700E+18', OverflowError, id="valid float under max int"),
        pytest.param('1.7976931348623157e+309', OverflowError, id="over max float64"),
        pytest.param('-1.7976931348623157e+309', OverflowError, id="under min float64"),
        pytest.param('47b', ValueError, id="extra characters"),
        pytest.param('NaN', ValueError, id="NaN"),
        pytest.param('Infinity', ValueError, id="Infinity"),
        pytest.param('-Infinity', ValueError, id="negative Infinity"),
        pytest.param('inf', ValueError, id="inf"),
        pytest.param('-inf', ValueError, id="negative inf"),
        pytest.param(None, TypeError, id="None"),
    ],
)
def test_from_api_string_invalid(source: str, expected_exception: IntegerValue) -> None:
    """
    Verify that invalid cases raise on IntegerValue.from_api_string
    Parameters
    ----------
    source the string to parse
    expected_exception the exception to expect
    """
    with _create_exception_context(expected_exception):
        result: IntegerValue = IntegerValue.from_api_string(source)