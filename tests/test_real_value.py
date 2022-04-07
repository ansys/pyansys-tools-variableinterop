from typing import Any

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import IntegerValue, RealValue


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
def test_initvalue_conversion_invalid(
        orig_real: RealValue, expected_exception: BaseException):
    with _create_exception_context(expected_exception):
        result: IntegerValue = orig_real.to_int_value()