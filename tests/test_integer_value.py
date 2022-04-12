from typing import Any

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import (
    IntegerValue,
    IVariableValue,
    BooleanValue,
    RealValue,
    StringValue,
    to_integer_value,
)

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


@pytest.mark.parametrize(
    'source,expected_result',
    [
        pytest.param(IntegerValue(0), '0', id='zero'),
        pytest.param(IntegerValue(1), '1', id='one'),
        pytest.param(IntegerValue(-1), '-1', id='negative one'),
        pytest.param(IntegerValue(8675309), '8675309', id='longer'),
        pytest.param(IntegerValue(-8675309), '-8675309', id='negative, longer'),
        pytest.param(IntegerValue(9223372036854775807), '9223372036854775807', id='max 64 bit'),
        pytest.param(IntegerValue(-9223372036854775808), '-9223372036854775808', id='min 64 bit'),
    ]
)
def test_to_api_string(source: IntegerValue, expected_result: str):
    """
    Verify that to_api_string for IntegerValue works correctly for valid cases.
    Parameters
    ----------
    source the original IntegerValue
    expected_value the expected API string
    """
    # Execute
    result: str = source.to_api_string()

    # Verify
    assert type(result) is str
    assert result == expected_result


@pytest.mark.parametrize(
    'source,expected_result',
    [
        pytest.param(IntegerValue(0), RealValue(0.0), id='zero'),
        pytest.param(IntegerValue(1), RealValue(1.0), id='one'),
        pytest.param(IntegerValue(-1), RealValue(-1.0), id='negative one'),
        pytest.param(IntegerValue(8675309), RealValue(8675309.0), id='larger'),
        pytest.param(IntegerValue(-8675309), RealValue(-8675309.0), id='larger negative'),
        pytest.param(IntegerValue(4503599627370495), RealValue(4503599627370495.0),
                     id='max 52-bit mantissa'),
        pytest.param(IntegerValue(-4503599627370496), RealValue(-4503599627370496.0),
                     id='min 52-bit mantissa'),
        pytest.param(IntegerValue(9223372036854775807), RealValue(9.223372036854776e+18),
                     id='max 64 bit'),
        pytest.param(IntegerValue(-9223372036854775808), RealValue(-9.223372036854776e+18),
                     id='min 64 bit'),
    ],
)
def test_to_real_value(source: IntegerValue, expected_result: RealValue) -> None:
    """
    Verify that conversions to RealValue work correctly.

    Parameters
    ----------
    source the original IntegerValue
    expected_result the expected RealValue
    """
    # Execute
    result: RealValue = source.to_real_value()

    # Verify
    assert type(result) is RealValue
    assert result == expected_result


@pytest.mark.parametrize(
    'source,expected_result',
    [
        pytest.param(RealValue(0.0), IntegerValue(0), id="0.0 to 0"),
        pytest.param(RealValue(1.0), IntegerValue(1), id="1.0 to 1"),
        pytest.param(RealValue(1.45), IntegerValue(1), id="1.45 to 1"),
        pytest.param(RealValue(1.49), IntegerValue(1), id="1.49 to 1"),
        pytest.param(RealValue(1.5), IntegerValue(2), id="1.5 to 2"),
        pytest.param(RealValue(1.7), IntegerValue(2), id="1.7 to 2"),
        pytest.param(RealValue(2.1), IntegerValue(2), id="2.1 to 2"),
        pytest.param(RealValue(2.5), IntegerValue(3), id="2.5 to 2"),
        pytest.param(RealValue(2.7), IntegerValue(3), id="2.7 to 2"),
        pytest.param(RealValue(-1.0), IntegerValue(-1), id="-1.0 to -1"),
        pytest.param(RealValue(-1.45), IntegerValue(-1), id="-1.45 to -1"),
        pytest.param(RealValue(-1.49), IntegerValue(-1), id="-1.49 to -1"),
        pytest.param(RealValue(-1.5), IntegerValue(-2), id="-1.5 to -2"),
        pytest.param(RealValue(-1.7), IntegerValue(-2), id="-1.7 to -2"),
        pytest.param(RealValue(-2.1), IntegerValue(-2), id="-2.1 to -2"),
        pytest.param(RealValue(-2.5), IntegerValue(-3), id="-2.5 to -3"),
        pytest.param(RealValue(-2.7), IntegerValue(-3), id="-2.7 to -3"),

        pytest.param(IntegerValue(0), IntegerValue(0), id="loopback 0"),
        pytest.param(IntegerValue(-1), IntegerValue(-1), id="loopback -1"),
        pytest.param(IntegerValue(1), IntegerValue(1), id="loopback 1"),
        pytest.param(IntegerValue(9223372036854775807), IntegerValue(9223372036854775807),
                     id='loopback max 64 bit'),
        pytest.param(IntegerValue(-9223372036854775808), IntegerValue(-9223372036854775808),
                     id='min 64 bit'),

        pytest.param(StringValue('0'), IntegerValue(0), id='string, zero'),
        pytest.param(StringValue('1'), IntegerValue(1), id='string, one'),
        pytest.param(StringValue('-1'), IntegerValue(-1), id='string, negative one'),
        pytest.param(StringValue('+42'), IntegerValue(42), id='string, explicit positive'),
        pytest.param(StringValue('047'), IntegerValue(47), id='string, leading zero'),
        pytest.param(StringValue('1.2E2'), IntegerValue(120),
                     id='string, scientific notation, whole'),
        pytest.param(StringValue('-1.2E2'), IntegerValue(-120),
                     id='string, scientific notation, whole, negative'),
        pytest.param(StringValue('1.2e+2'), IntegerValue(120),
                     id='string, scientific notation, lowercase e, explicit positive exponent'),
        pytest.param(StringValue('9223372036854775807'), IntegerValue(9223372036854775807),
                     id='string, max 64 bit'),
        pytest.param(StringValue('-9223372036854775808'), IntegerValue(-9223372036854775808),
                     id='string, min 64 bit'),
        pytest.param(StringValue('1.5'), IntegerValue(2), id='string, rounding, to even'),
        pytest.param(StringValue('2.5'), IntegerValue(3), id='string, rounding, to odd'),
        pytest.param(StringValue('-1.5'), IntegerValue(-2),
                     id='string, rounding, to odd, negative'),
        pytest.param(StringValue('-2.5'), IntegerValue(-3),
                     id='string, rounding, to even, negative'),
        pytest.param(BooleanValue(True), IntegerValue(1),
                     id='boolean true'),
        pytest.param(BooleanValue(False), IntegerValue(0),
                     id='boolean false')
    ]
)
def test_to_integer_value(source: IVariableValue, expected_result: IntegerValue):
    # Execute
    result: IntegerValue = to_integer_value(source)

    # Verify
    assert type(result) is IntegerValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(StringValue('complete garbage'), ValueError, id="complete garbage"),
        pytest.param(StringValue(''), ValueError, id="empty string"),
        pytest.param(StringValue('    '), ValueError, id="whitespace only"),
        pytest.param(StringValue('2.2.2'), ValueError, id="string, too many decimals"),
        pytest.param(StringValue('9.223372036854775300E+18'), OverflowError,
                     id="string, valid float over max int"),
        pytest.param(StringValue('-9.223372036854777700E+18'), OverflowError,
                     id="string, valid float under max int"),
        pytest.param(StringValue('1.7976931348623157e+309'), OverflowError,
                     id="string, over max float64"),
        pytest.param(StringValue('-1.7976931348623157e+309'), OverflowError,
                     id="string, under min float64"),
        pytest.param(StringValue('47b'), ValueError, id="extra characters"),
        pytest.param(StringValue('NaN'), ValueError, id="string, NaN"),
        pytest.param(StringValue('Infinity'), ValueError, id="string, Infinity"),
        pytest.param(StringValue('-Infinity'), ValueError, id="string, negative Infinity"),
        pytest.param(RealValue(9.223372036854775300E+18), OverflowError,
                     id="valid float over max int"),
        pytest.param(RealValue(-9.223372036854777700E+18), OverflowError,
                     id="valid float under max int"),
        pytest.param(RealValue(1.7976931348623157e+309), OverflowError,
                     id="over max float64"),
        pytest.param(RealValue(-1.7976931348623157e+309), OverflowError,
                     id="under min float64"),
        pytest.param(RealValue(float('NaN')), ValueError, id="NaN"),
        pytest.param(RealValue(float('Infinity')), OverflowError, id="Infinity"),
        pytest.param(RealValue(float('-Infinity')), OverflowError, id="negative Infinity"),
    ],
)
def test_to_integer_value_invalid(source: IVariableValue, expected_exception: BaseException):
    # Execute
    with _create_exception_context(expected_exception):
        result: IntegerValue = to_integer_value(source)
