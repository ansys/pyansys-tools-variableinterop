"""
Unit tests for scalar_value_conversion.
"""

import sys
from typing import Type

import numpy
import pytest
from test_utils import _assert_incompatible_types_exception, _create_exception_context

from ansys.tools.variableinterop import (
    EMPTY_FILE,
    BooleanArrayValue,
    BooleanValue,
    FileArrayValue,
    FileValue,
    IncompatibleTypesException,
    IntegerArrayValue,
    IntegerValue,
    IVariableValue,
    RealArrayValue,
    RealValue,
    StringArrayValue,
    StringValue,
    to_boolean_value,
    to_integer_value,
    to_real_value,
    to_string_value,
)


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(BooleanValue(True), RealValue(1.0), id="Boolean True"),
        pytest.param(BooleanValue(False), RealValue(0.0), id="Boolean False"),
        pytest.param(IntegerValue(0), RealValue(0.0), id="Integer 0"),
        pytest.param(IntegerValue(3), RealValue(3.0), id="Integer 3"),
        pytest.param(
            IntegerValue(9223372036854775807), RealValue(9223372036854775807.0), id="Integer max"
        ),
        pytest.param(
            IntegerValue(-9223372036854775808), RealValue(-9223372036854775808.0), id="Integer min"
        ),
        pytest.param(StringValue("1"), RealValue(1.0), id="String 1"),
        pytest.param(StringValue("inf"), RealValue(numpy.float64("inf")), id="String inf"),
        pytest.param(StringValue("-inf"), RealValue(numpy.float64("-inf")), id="String -inf"),
        pytest.param(StringValue("-1"), RealValue(-1.0), id="String -1"),
        pytest.param(
            StringValue("9223372036854775807"),
            RealValue(9223372036854775807.0),
            id="String int-max",
        ),
        pytest.param(
            StringValue("-9223372036854775808"),
            RealValue(-9223372036854775808.0),
            id="String int-min",
        ),
        pytest.param(StringValue("3.14159"), RealValue(3.14159), id="String 3.14159"),
        pytest.param(
            StringValue("2.2250738585072014e-308"),
            RealValue(2.2250738585072014e-308),
            id="String smallest-normal",
        ),
        pytest.param(
            StringValue("1.7976931348623157e+308"),
            RealValue(1.7976931348623157e308),
            id="String abs-max",
        ),
        pytest.param(
            StringValue("-1.7976931348623157e+308"),
            RealValue(-1.7976931348623157e308),
            id="String abs-min",
        ),
    ],
)
def test_to_real_value(source: IVariableValue, expected_result: RealValue):
    """
    Test behavior of to_real_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result: RealValue
        The expected result of the test.
    """
    # SUT
    result: RealValue = to_real_value(source)

    # Verify
    assert type(result) == RealValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(BooleanValue(True), IntegerValue(1), id="Boolean True"),
        pytest.param(BooleanValue(False), IntegerValue(0), id="Boolean False"),
        pytest.param(RealValue(0.0), IntegerValue(0), id="Real 0.0"),
        pytest.param(RealValue(1.49), IntegerValue(1), id="Real 1.49"),
        pytest.param(RealValue(1.50), IntegerValue(2), id="Real 1.5"),
        pytest.param(RealValue(1.51), IntegerValue(2), id="Real 1.51"),
        pytest.param(RealValue(-1.49), IntegerValue(-1), id="Real -1.49"),
        pytest.param(RealValue(-1.50), IntegerValue(-2), id="Real -1.5"),
        pytest.param(RealValue(-1.51), IntegerValue(-2), id="Real -1.51"),
        pytest.param(StringValue("1.49"), IntegerValue(1), id="String 1.49"),
        pytest.param(StringValue("1.50"), IntegerValue(2), id="String 1.5"),
        pytest.param(StringValue("1.51"), IntegerValue(2), id="String 1.51"),
        pytest.param(StringValue("-1.49"), IntegerValue(-1), id="String -1.49"),
        pytest.param(StringValue("-1.50"), IntegerValue(-2), id="String -1.5"),
        pytest.param(StringValue("-1.51"), IntegerValue(-2), id="String -1.51"),
        pytest.param(StringValue("1"), IntegerValue(1.0), id="String 1"),
        pytest.param(StringValue("-1"), IntegerValue(-1.0), id="String -1"),
        pytest.param(
            StringValue("9223372036854775807"),
            IntegerValue(9223372036854775807),
            id="String int-max",
        ),
        pytest.param(
            StringValue("-9223372036854775808"),
            IntegerValue(-9223372036854775808),
            id="String int-min",
        ),
        pytest.param(StringValue("-3.14159"), IntegerValue(-3), id="String -3.14159"),
    ],
)
def test_to_integer_value(source: IVariableValue, expected_result: IntegerValue) -> None:
    """
    Test behavior of to_integer_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result : IntegerValue
        The expected result of the test.
    """
    # SUT
    result: IntegerValue = to_integer_value(source)

    # Verify
    assert type(result) == IntegerValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        # Boolean to Boolean Tests
        pytest.param(BooleanValue(True), BooleanValue(True), id="BooleanValue(True)"),
        pytest.param(BooleanValue(False), BooleanValue(False), id="BooleanValue(False)"),
        # Integer to Boolean Tests
        pytest.param(
            IntegerValue(numpy.iinfo(numpy.int64).min), BooleanValue(True), id="IntegerValue(MIN)"
        ),
        pytest.param(IntegerValue(-1), BooleanValue(True), id="IntegerValue(-1)"),
        pytest.param(IntegerValue(0), BooleanValue(False), id="IntegerValue(0)"),
        pytest.param(IntegerValue(1), BooleanValue(True), id="IntegerValue(1)"),
        pytest.param(
            IntegerValue(numpy.iinfo(numpy.int64).max), BooleanValue(True), id="IntegerValue(MAX)"
        ),
        # Real to Boolean Tests
        pytest.param(RealValue(float("-inf")), BooleanValue(True), id="RealValue(-∞)"),
        pytest.param(RealValue(-sys.float_info.max), BooleanValue(True), id="RealValue(-MAX)"),
        pytest.param(RealValue(-1.0), BooleanValue(True), id="RealValue(-1.0)"),
        pytest.param(RealValue(-sys.float_info.epsilon), BooleanValue(True), id="RealValue(-ε)"),
        pytest.param(RealValue(-sys.float_info.min), BooleanValue(True), id="RealValue(-MIN)"),
        pytest.param(RealValue(-0.0), BooleanValue(False), id="RealValue(-0.0)"),
        pytest.param(RealValue(0.0), BooleanValue(False), id="RealValue(0.0)"),
        pytest.param(RealValue(sys.float_info.min), BooleanValue(True), id="RealValue(MIN)"),
        pytest.param(RealValue(sys.float_info.epsilon), BooleanValue(True), id="RealValue(ε)"),
        pytest.param(RealValue(1.0), BooleanValue(True), id="RealValue(1.0)"),
        pytest.param(RealValue(sys.float_info.max), BooleanValue(True), id="RealValue(MAX)"),
        pytest.param(RealValue(float("inf")), BooleanValue(True), id="RealValue(∞)"),
        pytest.param(RealValue(float("nan")), BooleanValue(True), id="RealValue(NAN)"),
        # String to Bool Tests
        pytest.param(StringValue("True"), BooleanValue(True), id="StringValue(True)"),
        pytest.param(StringValue("False"), BooleanValue(False), id="StringValue(False)"),
        pytest.param(StringValue("Y"), BooleanValue(True), id="StringValue(Y)"),
        pytest.param(StringValue("N"), BooleanValue(False), id="StringValue(N)"),
        pytest.param(StringValue("yes"), BooleanValue(True), id="StringValue(yes)"),
        pytest.param(StringValue("no"), BooleanValue(False), id="StringValue(no)"),
        pytest.param(StringValue("  true  "), BooleanValue(True), id="StringValue(  true  )"),
        pytest.param(StringValue("  false  "), BooleanValue(False), id="StringValue(  false  )"),
        pytest.param(StringValue("  TRUE  "), BooleanValue(True), id="StringValue(  TRUE  )"),
        pytest.param(StringValue("  FALSE  "), BooleanValue(False), id="StringValue(  FALSE  )"),
        pytest.param(
            StringValue(str(numpy.iinfo(numpy.int64).min)),
            BooleanValue(True),
            id="StringValue(INT64_MIN)",
        ),
        pytest.param(StringValue("-1"), BooleanValue(True), id="StringValue(-1)"),
        pytest.param(StringValue("0"), BooleanValue(False), id="StringValue(0)"),
        pytest.param(StringValue("1"), BooleanValue(True), id="StringValue(1)"),
        pytest.param(
            StringValue(str(numpy.iinfo(numpy.int64).max)),
            BooleanValue(True),
            id="StringValue(INT64_MAX)",
        ),
        pytest.param(
            StringValue("1234567890123456789"),
            BooleanValue(True),
            id="StringValue(1234567890123456789)",
        ),
        pytest.param(StringValue("-inf"), BooleanValue(True), id="StringValue(-inf)"),
        pytest.param(
            StringValue(str(-sys.float_info.max)), BooleanValue(True), id="StringValue(-DLB_MAX)"
        ),
        pytest.param(StringValue("-1.0"), BooleanValue(True), id="StringValue(-1.0)"),
        pytest.param(
            StringValue(str(-sys.float_info.epsilon)),
            BooleanValue(True),
            id="StringValue(-DBL_EPSILON)",
        ),
        pytest.param(
            StringValue(str(-sys.float_info.min)), BooleanValue(True), id="StringValue(-DBL_MIN)"
        ),
        pytest.param(StringValue("-0.0"), BooleanValue(False), id="StringValue(-0.0)"),
        pytest.param(StringValue("0.0"), BooleanValue(False), id="StringValue(0.0)"),
        pytest.param(
            StringValue(str(sys.float_info.min)), BooleanValue(True), id="StringValue(DLB_MIN)"
        ),
        pytest.param(
            StringValue(str(sys.float_info.epsilon)),
            BooleanValue(True),
            id="StringValue(DBL_EPSILON)",
        ),
        pytest.param(StringValue("1.0"), BooleanValue(True), id="StringValue(1.0)"),
        pytest.param(
            StringValue(str(sys.float_info.max)), BooleanValue(True), id="StringValue(DBL_MAX)"
        ),
        pytest.param(StringValue("inf"), BooleanValue(True), id="StringValue(inf)"),
        pytest.param(StringValue("nan"), BooleanValue(True), id="StringValue(nan)"),
    ],
)
def test_to_boolean_value(source: IVariableValue, expected_result: BooleanValue) -> None:
    """
    Test behavior of to_boolean_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result : BooleanValue
        The expected result of the test.
    """
    # SUT
    result: BooleanValue = to_boolean_value(source)

    # Verify
    assert type(result) == BooleanValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(BooleanValue(True), StringValue("True"), id="Boolean true"),
        pytest.param(BooleanValue(False), StringValue("False"), id="Boolean false"),
        pytest.param(IntegerValue(0), StringValue("0"), id="Integer 0"),
        pytest.param(
            IntegerValue(9223372036854775807), StringValue("9223372036854775807"), id="Integer max"
        ),
        pytest.param(
            IntegerValue(-9223372036854775808),
            StringValue("-9223372036854775808"),
            id="Integer min",
        ),
        pytest.param(RealValue(0.0), StringValue("0.0"), id="Real 0.0"),
        pytest.param(
            RealValue(2.2250738585072014e-308),
            StringValue("2.2250738585072014e-308"),
            id="Real smallest-normal",
        ),
        pytest.param(
            RealValue(1.7976931348623157e308),
            StringValue("1.7976931348623157e+308"),
            id="Real abs-max",
        ),
        pytest.param(
            RealValue(-1.7976931348623157e308),
            StringValue("-1.7976931348623157e+308"),
            id="Real abs-min",
        ),
        # Array Types
        pytest.param(
            BooleanArrayValue(values=[True, False, True]),
            StringValue("True,False,True"),
            id="BooleanArrayValue",
        ),
        pytest.param(
            IntegerArrayValue(values=[0, 1, 0]), StringValue("0,1,0"), id="IntegerArrayValue"
        ),
        pytest.param(
            RealArrayValue(values=[1.0, 0.0]), StringValue("1.0,0.0"), id="RealArrayValue"
        ),
        pytest.param(
            StringArrayValue(values=["0", "1", "0"]),
            StringValue('"0","1","0"'),
            id="StringArrayValue",
        ),
    ],
)
def test_to_string_value(source: IVariableValue, expected_result: StringValue) -> None:
    """
    Test behavior of to_string_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result : StringValue
        The expected result of the test.
    """
    # SUT
    result: StringValue = to_string_value(source)

    # Verify
    assert type(result) == StringValue
    assert result == expected_result


def test_file_value_to_string_value():
    """Verify that to_string_value fails for FileValue instances."""
    with _create_exception_context(IncompatibleTypesException):
        try:
            _ = to_string_value(EMPTY_FILE)
        except IncompatibleTypesException as thrown:
            _assert_incompatible_types_exception(
                str(thrown), FileValue.__name__, StringValue.__name__
            )
            raise thrown


def test_file_array_value_to_string_value():
    """Verify that to_string_value fails for FileArrayValue instances."""
    with _create_exception_context(IncompatibleTypesException):
        try:
            _ = to_string_value(FileArrayValue())
        except IncompatibleTypesException as thrown:
            _assert_incompatible_types_exception(
                str(thrown), FileArrayValue.__name__, StringValue.__name__
            )
            raise thrown


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(StringValue(""), ValueError, id="String empty"),
        pytest.param(StringValue("garbage"), ValueError, id="String garbage"),
        # Array Types
        pytest.param(
            BooleanArrayValue(values=[True, False, True]),
            IncompatibleTypesException,
            id="BooleanArrayValue",
        ),
        pytest.param(
            IntegerArrayValue(values=[0, 1, 0]), IncompatibleTypesException, id="IntegerArrayValue"
        ),
        pytest.param(
            RealArrayValue(values=[1.0, 0.0]), IncompatibleTypesException, id="RealArrayValue"
        ),
        pytest.param(
            StringArrayValue(values=["0", "1", "0"]),
            IncompatibleTypesException,
            id="StringArrayValue",
        ),
    ],
)
def test_to_real_value_raises(
    source: IVariableValue, expected_exception: Type[BaseException]
) -> None:
    """
    Test behavior of to_real_value() when it is expected to raise an exception.

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_exception : Type[BaseException]
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = to_real_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == IncompatibleTypesException:
                _assert_incompatible_types_exception(
                    str(e), source.__class__.__name__, RealValue.__name__
                )
            raise e


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(RealValue(9.3e18), OverflowError, id="Real over max"),
        pytest.param(RealValue(-9.3e18), OverflowError, id="Real under min"),
        pytest.param(RealValue(numpy.float64("inf")), OverflowError, id="Real +infinity"),
        pytest.param(RealValue(numpy.float64("-inf")), OverflowError, id="Real -infinity"),
        pytest.param(StringValue(""), ValueError, id="String empty"),
        pytest.param(StringValue("garbage"), ValueError, id="String garbage"),
        # Array Types
        pytest.param(
            BooleanArrayValue(values=[True, False, True]),
            IncompatibleTypesException,
            id="BooleanArrayValue",
        ),
        pytest.param(
            IntegerArrayValue(values=[0, 1, 0]), IncompatibleTypesException, id="IntegerArrayValue"
        ),
        pytest.param(
            RealArrayValue(values=[1.0, 0.0]), IncompatibleTypesException, id="RealArrayValue"
        ),
        pytest.param(
            StringArrayValue(values=["0", "1", "0"]),
            IncompatibleTypesException,
            id="StringArrayValue",
        ),
    ],
)
def test_to_integer_value_raises(
    source: IVariableValue, expected_exception: Type[BaseException]
) -> None:
    """
    Test behavior of to_integer_value() when it is expected to raise an exception.

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_exception : Type[BaseException]
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = to_integer_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == IncompatibleTypesException:
                _assert_incompatible_types_exception(
                    str(e), source.__class__.__name__, IntegerValue.__name__
                )
            raise e


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(StringValue(""), ValueError, id="String empty"),
        pytest.param(StringValue("tak"), ValueError, id="String garbage"),
        # Array Types
        pytest.param(
            BooleanArrayValue(values=[True, False, True]),
            IncompatibleTypesException,
            id="BooleanArrayValue",
        ),
        pytest.param(
            IntegerArrayValue(values=[0, 1, 0]), IncompatibleTypesException, id="IntegerArrayValue"
        ),
        pytest.param(
            RealArrayValue(values=[1.0, 0.0]), IncompatibleTypesException, id="RealArrayValue"
        ),
        pytest.param(
            StringArrayValue(values=["0", "1", "0"]),
            IncompatibleTypesException,
            id="StringArrayValue",
        ),
    ],
)
def test_to_boolean_value_raises(
    source: IVariableValue, expected_exception: Type[BaseException]
) -> None:
    """
    Test behavior of to_boolean_value() when it is expected to raise an exception.

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_exception : Type[BaseException]
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = to_boolean_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == IncompatibleTypesException:
                _assert_incompatible_types_exception(
                    str(e), source.__class__.__name__, bool.__name__
                )
            raise e
