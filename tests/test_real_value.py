from typing import Any

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import (
    BooleanValue,
    IntegerValue,
    IVariableValue,
    RealValue,
    StringValue,
    to_real_value,
)


@pytest.mark.parametrize(
    "arg,expect_equality,expect_exception",
    [
        pytest.param(0, numpy.float64(0), None, id="zero"),
        pytest.param(1.0, numpy.float64(1.0), None, id="one"),
        pytest.param(-1.0, numpy.float64(-1.0), None, id="negative-one"),
        pytest.param(2.2250738585072014e-308, numpy.float64(2.2250738585072014e-308), None,
                     id="smallest-normal"),
        pytest.param(1.7976931348623157e+308, numpy.float64(1.7976931348623157e+308), None,
                     id="abs-max"),
        pytest.param(-1.7976931348623157e+308, numpy.float64(-1.7976931348623157e+308), None,
                     id="abs-min"),
        pytest.param(float('inf'), numpy.float64('inf'), None, id="inf"),
        pytest.param(float('-inf'), numpy.float64('-inf'), None, id="neg-inf"),
        pytest.param(float('NaN'), numpy.float64('NaN'), None, id="NaN"),

        # TODO: Should we override the numpy behavior here?
        pytest.param(None, numpy.float64('NaN'), None, id="None"),

        # TODO: Should we support subnormal floats? Numpy allows it
        # (with loss of precision, see below)
        pytest.param(2.2250738585072014e-309, numpy.float64(2.225073858507203e-309), None,
                     id="subnormal"),

        # TODO: Should we support string representations of numbers over/under max/min?
        # (Numpy converts to inf):
        pytest.param('1.7976931348623157e+308', numpy.float64(1.7976931348623157e+308), None,
                     id="abs-max"),
        pytest.param('-1.7976931348623157e+308', numpy.float64(-1.7976931348623157e+308), None,
                     id="abs-min"),

        # TODO: Should we support string representations at all?
        # Should we pass-through to numpy, mimic fromAPIString, mimic fromFormattedString?
        pytest.param('some garbage text', numpy.float64('NaN'), ValueError, id="garbage-text"),
        pytest.param('0', numpy.float64(0), None, id="zero-text"),
        pytest.param('-1.0', numpy.float64(-1.0), None, id="negative-one-text"),
        pytest.param('1.0', numpy.float64(1.0), None, id="one-text"),
    ])
def test_construct(
        arg: Any, expect_equality: numpy.float64, expect_exception: BaseException) -> None:
    """Verify that __init__ for RealValue correctly instantiates the superclass data."""
    with _create_exception_context(expect_exception):
        instance = RealValue(arg)

        if expect_exception is None:
            if not numpy.isnan(expect_equality):
                assert instance == expect_equality
            else:
                assert numpy.isnan(instance)


def __valid_toint_id_gen(orig_val: RealValue) -> str:
    """
    Generate an ID for the parameterized tests for converting
    RealValues to IntegerValues when the conversion is valid.

    Parameters
    ----------
    orig_val the original value

    Returns
    -------
    a suitable ID for the test
    """
    return str(orig_val)


@pytest.mark.parametrize(
    "orig_real,expected_result",
    [
        pytest.param(RealValue(0.0), IntegerValue(0)),
        pytest.param(RealValue(1.0), IntegerValue(1)),
        pytest.param(RealValue(1.45), IntegerValue(1)),
        pytest.param(RealValue(1.49), IntegerValue(1)),
        pytest.param(RealValue(1.5), IntegerValue(2)),
        pytest.param(RealValue(1.7), IntegerValue(2)),
        pytest.param(RealValue(2.1), IntegerValue(2)),
        pytest.param(RealValue(2.5), IntegerValue(3)),
        pytest.param(RealValue(2.7), IntegerValue(3)),
        pytest.param(RealValue(-1.0), IntegerValue(-1)),
        pytest.param(RealValue(-1.45), IntegerValue(-1)),
        pytest.param(RealValue(-1.49), IntegerValue(-1)),
        pytest.param(RealValue(-1.5), IntegerValue(-2)),
        pytest.param(RealValue(-1.7), IntegerValue(-2)),
        pytest.param(RealValue(-2.1), IntegerValue(-2)),
        pytest.param(RealValue(-2.5), IntegerValue(-3)),
        pytest.param(RealValue(-2.7), IntegerValue(-3))
    ], ids=__valid_toint_id_gen
)
def test_intvalue_conversion_valid(
        orig_real: RealValue, expected_result: IntegerValue):
    # Execute
    result: IntegerValue = orig_real.to_int_value()

    # Verify
    assert isinstance(result, IntegerValue)
    assert result == expected_result


@pytest.mark.parametrize(
    "orig_real,expected_exception",
    [
        pytest.param(RealValue(9.3e18), OverflowError, id="over max"),
        pytest.param(RealValue(-9.3e18), OverflowError, id="under min"),
        pytest.param(RealValue(numpy.float64('inf')), OverflowError, id="+infinity"),
        pytest.param(RealValue(numpy.float64('-inf')), OverflowError, id="-infinity"),
        pytest.param(RealValue(numpy.float64('NaN')), ValueError, id="NaN"),
    ],
)
def test_intvalue_conversion_invalid(
        orig_real: RealValue, expected_exception: BaseException):
    with _create_exception_context(expected_exception):
        result: IntegerValue = orig_real.to_int_value()


@pytest.mark.parametrize(
    'orig_real,expected_result',
    [
        pytest.param(RealValue(0), BooleanValue(False), id="zero"),
        pytest.param(RealValue(-0.01), BooleanValue(True), id="negative"),
        pytest.param(RealValue(0.01), BooleanValue(True), id="positive"),
        pytest.param(RealValue(float('inf')), BooleanValue(True), id="inf"),
        pytest.param(RealValue(float('-inf')), BooleanValue(True), id="-inf"),
        pytest.param(RealValue(float('nan')), BooleanValue(True), id="NaN"),

    ],
)
def test_boolean_value_conversion(
        orig_real: RealValue, expected_result: BooleanValue) -> None:
    """
    Verify that RealValues are correctly converted to BooleanValues
    Parameters
    ----------
    orig_real the original real
    expected_result the expected boolean
    """
    result: BooleanValue = orig_real.to_boolean_value()

    # TODO: Figure out the whole numpy.bool_ decomposition issue here
    # assert type(result) is BooleanValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param('4.5', RealValue(4.5), id="basic, positive"),
        pytest.param('-4.5', RealValue(-4.5), id="basic negative"),
        pytest.param('0', RealValue(0), id="zero"),
        pytest.param('2.8E8', RealValue(2.8E8), id="sci notation, positive, capital E"),
        pytest.param('-2.8E8', RealValue(-2.8E8), id="sci notation, negative, capital E"),
        pytest.param('2.8e8', RealValue(2.8E8), id="sci notation, positive, lowercase e"),
        pytest.param('2.8e-8', RealValue(2.8E-8), id="sci notation, negative-exponent"),
        pytest.param('.4', RealValue(0.4), id="no leading zero"),
        pytest.param('4.0', RealValue(4.0), id="whole number, point zero"),
        pytest.param('4.', RealValue(4.0), id="whole number, decimal, no zero"),
        pytest.param('4', RealValue(4), id="whole number, no decimal"),
        pytest.param('+4.7', RealValue(4.7), id="explicit positive"),
        pytest.param('1.7976931348623157e+308', RealValue(1.7976931348623157e+308),
                     id="absolute maximum"),
        pytest.param('-1.7976931348623157e+308', RealValue(-1.7976931348623157e+308),
                     id="absolute minimum"),
        pytest.param('2.2250738585072014e-308', RealValue(2.2250738585072014e-308),
                     id="epsilon"),
        pytest.param(' \t\r\n  867.5309', RealValue(867.5309), id="leading whitespace"),
        pytest.param('867.5309   \t\r\n', RealValue(867.5309), id="trailing whitespace"),
        pytest.param('Inf', RealValue(numpy.float64('inf')), id="Inf"),
        pytest.param('inf', RealValue(numpy.float64('inf')), id="inf"),
        pytest.param('INF', RealValue(numpy.float64('inf')), id="INF"),
        pytest.param('Infinity', RealValue(numpy.float64('inf')), id="Infinity"),
        pytest.param('infinity', RealValue(numpy.float64('inf')), id="infinity"),
        pytest.param('INFINITY', RealValue(numpy.float64('inf')), id="INFINITY"),
        pytest.param('-Inf', RealValue(numpy.float64('-inf')), id="negative Inf"),
        pytest.param('-inf', RealValue(numpy.float64('-inf')), id="negative inf"),
        pytest.param('-INF', RealValue(numpy.float64('-inf')), id="negative INF"),
        pytest.param('-Infinity', RealValue(numpy.float64('-inf')), id="negative Infinity"),
        pytest.param('-infinity', RealValue(numpy.float64('-inf')), id="negative infinity"),
        pytest.param('-INFINITY', RealValue(numpy.float64('-inf')), id="negative INFINITY"),
        pytest.param('1.7976931348623157e+309', RealValue(numpy.float64('Inf')),
                     id="over maximum"),
        pytest.param('-1.7976931348623157e+309', RealValue(numpy.float64('-Inf')),
                     id="under minimum"),
        pytest.param('NaN', RealValue(numpy.float64('NaN')),
                     id="NaN"),
        pytest.param('nan', RealValue(numpy.float64('NaN')),
                     id="nan"),
    ],
)
def test_from_api_string_valid(
        source: str, expected_result: RealValue) -> None:
    """
    Verify that valid cases work on RealValue.from_api_string.

    Parameters
    ----------
    source the string to convert
    expected_result the expected result
    """
    # Execute
    actual_result: RealValue = RealValue.from_api_string(source)

    #Verify
    assert isinstance(actual_result, RealValue)
    if not numpy.isnan(expected_result):
        assert actual_result == expected_result
    else:
        assert numpy.isnan(actual_result)


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param('60Ɛϛ˙ㄥ98', ValueError, id='garbage'),
        pytest.param('1,204.5', ValueError, id='thousands separator'),
        pytest.param('1 204.5', ValueError, id='internal whitespace'),
        pytest.param('2.2.2', ValueError, id='multiple decimals'),
        pytest.param('true', ValueError, id='boolean literal'),
        pytest.param('', ValueError, id='empty string'),
        pytest.param(None, TypeError, id='None'),
    ],
)
def test_from_api_string_invalid(
        source: str, expected_exception: BaseException) -> None:
    """
    Verify that invalid cases correctly raise on from_api_string.

    Parameters
    ----------
    source the string to convert
    expected_exception the expected error raised
    """
    # Execute
    with _create_exception_context(expected_exception):
        actual_result: RealValue = RealValue.from_api_string(source)


@pytest.mark.parametrize(
    'source,expected_value',
    [
        pytest.param(RealValue(3.0),  '3.0', id='whole number'),
        pytest.param(RealValue(4.5),  '4.5', id='accurate with one place'),
        pytest.param(RealValue(1.7976931348623157e+308), '1.7976931348623157e+308', id='max'),
        pytest.param(RealValue(-1.7976931348623157e+308), '-1.7976931348623157e+308', id='min'),
        pytest.param(RealValue(0.0), '0.0', id='zero'),
        pytest.param(RealValue(float('inf')), 'Infinity', id='Infinity'),
        pytest.param(RealValue(float('-inf')), '-Infinity', id='-Infinity'),
        pytest.param(RealValue(float('nan')), 'NaN', id='NaN'),
        pytest.param(RealValue(2.2250738585072014e-308), '2.2250738585072014e-308', id='epsilon'),
        pytest.param(RealValue(1.0000000000000002), '1.0000000000000002', id='epsilon+1'),
    ]
)
def test_to_api_string(
        source: RealValue, expected_value: str) -> None:
    """
    Verify that the to_api_string method works correctly.

    Parameters
    ----------
    source the original RealValue.
    expected_value the original string.
    """
    # Execute
    result: str = source.to_api_string()

    # Verify
    assert type(result) is str
    assert result == expected_value


@pytest.mark.parametrize(
    'source,expected_value',
    [
        pytest.param(IntegerValue(0), RealValue(0.0), id='integer 0'),
        pytest.param(IntegerValue(1), RealValue(1.0), id='integer 1'),
        pytest.param(IntegerValue(-1), RealValue(-1.0), id='integer -1'),
        pytest.param(IntegerValue(8675309), RealValue(8675309.0), id='larger'),
        pytest.param(IntegerValue(-8675309), RealValue(-8675309.0), id='larger negative'),
        pytest.param(IntegerValue(9223372036854775807), RealValue(9.223372036854776e+18),
                     id='max 64 bit'),
        pytest.param(IntegerValue(-9223372036854775808), RealValue(-9.223372036854776e+18),
                     id='min 64 bit'),
        pytest.param(RealValue(867.5309), RealValue(867.5309), id='loopback'),
        pytest.param(RealValue(1.7976931348623157e+308), numpy.float64(1.7976931348623157e+308),
                     id="loopback min"),
        pytest.param(RealValue(-1.7976931348623157e+308), numpy.float64(-1.7976931348623157e+308),
                     id="loopback max"),
        pytest.param(StringValue('4.5'), RealValue(4.5), id="string, positive"),
        pytest.param(StringValue('-4.5'), RealValue(-4.5), id="string, negative"),
        pytest.param(StringValue('0'), RealValue(0), id="string, zero"),
        pytest.param(StringValue('2.8E8'), RealValue(2.8E8),
                     id="string, sci notation, positive, capital E"),
        pytest.param(StringValue('-2.8e8'), RealValue(-2.8E8),
                     id="string, sci notation, negative, lowercase E"),
        pytest.param(StringValue('5E-2'), RealValue(0.05),
                     id="string, sci notation, negative exponent"),
        pytest.param(StringValue('-Infinity'), RealValue(numpy.float64('-inf')),
                     id="negative Infinity"),
        pytest.param(StringValue('Infinity'), RealValue(numpy.float64('inf')), id="Infinity"),
        pytest.param(StringValue('NaN'), RealValue(numpy.float64('nan')), id="NaN"),

        # TODO: Add boolean value tests when boolean types are ready
        # pytest.param(BooleanValue(True), RealValue(1.0), id='boolean true'),
        # pytest.param(BooleanValue(False), RealValue(0.0), id='boolean false'),
    ],
)
def test_runtime_convert_valid(
        source: IVariableValue, expected_value: RealValue) -> None:
    """
    Verify that the runtime_convert method works on valid cases.

    Parameters
    ----------
    source the source variable to convert to RealValue
    expected_value the expected result of the conversion
    """

    # Execute
    result: RealValue = to_real_value(source)

    # Verify
    assert type(result) is RealValue
    if not numpy.isnan(expected_value):
        assert result == expected_value
    else:
        assert numpy.isnan(expected_value)
