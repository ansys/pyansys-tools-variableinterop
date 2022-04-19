"""
Tests for the type coercion module
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple, Type

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import (
    BooleanValue,
    IntegerValue,
    IVariableValue,
    RealValue,
    StringValue,
    implicit_coerce,
)


class IDummy(ABC):
    """Example interface that accepts variable types"""

    @abstractmethod
    def variable_argument(self, value: IVariableValue) -> IVariableValue:
        ...

    # TODO: methods that accept specific types of IVariableValue
    # TODO: test that it ignores other parameters


class Impl(ABC):
    """Test implementation that just returns what it gets sent"""

    @implicit_coerce
    def variable_argument(self, value: IVariableValue) -> IVariableValue:
        return value


class NotConvertible:
    """Test object that can't be converted to an IVariableValue"""

    pass


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(0, IntegerValue(0), None, id="builtins.int 0"),
        pytest.param(numpy.int8(127), IntegerValue(127), None, id="np.int8 max"),
        pytest.param(numpy.int16(32767), IntegerValue(32767), None, id="np.int16 max"),
        pytest.param(numpy.int32(2147483647), IntegerValue(2147483647),
                     None, id="np.int32 max"),
        pytest.param(numpy.int64(9223372036854775807),
                     IntegerValue(9223372036854775807), None, id="np.int64 max"),
        pytest.param(numpy.int8(-128), IntegerValue(-128), None, id="np.int8 min"),
        pytest.param(numpy.int16(-32768), IntegerValue(-32768), None, id="np.int16 min"),
        pytest.param(numpy.int32(-2147483648), IntegerValue(-2147483648),
                     None, id="np.int32 min"),
        pytest.param(numpy.int64(-9223372036854775808),
                     IntegerValue(-9223372036854775808), None, id="np.int64 min"),
        pytest.param(-9223372036854775809,
                     None, OverflowError, id="builtins.int under 64-bit min"),
        pytest.param(1.2, RealValue(1.2), None, id="builtins.float 1.2"),
        pytest.param(numpy.float32(0.0), RealValue(0.0), None, id="np.float32 0.0"),
        pytest.param(numpy.float32(-1.0), RealValue(-1.0), None, id="np.float32 -1.0"),
        pytest.param(numpy.float32(867.5309), RealValue(numpy.float32(867.5309)), None,
                     id="np.float32 867.5309"),
        pytest.param(numpy.float64(9000.1), RealValue(9000.1), None, id="np.float64 9000.1"),
        pytest.param(numpy.float64(2.2250738585072014e-308), RealValue(2.2250738585072014e-308),
                     None, id="float64 smallest-normal"),
        pytest.param(numpy.float64(1.7976931348623157e+308), RealValue(1.7976931348623157e+308),
                     None, id="float64 abs-max"),
        pytest.param(numpy.float64(-1.7976931348623157e+308), RealValue(-1.7976931348623157e+308),
                     None, id="float64 abs-min"),
        pytest.param(True, BooleanValue(True), None, id='builtins.bool true'),
        pytest.param(False, BooleanValue(False), None, id='builtins.bool false'),
        pytest.param(numpy.bool_(True), BooleanValue(True), None, id='builtins.bool true'),
        pytest.param(numpy.bool_(False), BooleanValue(False), None, id='builtins.bool false'),
        pytest.param("", StringValue(""), None, id="builtins.str empty"),
        pytest.param("ASCII-only", StringValue("ASCII-only"), None,
                     id="builtins.str ascii-codespace"),
        pytest.param("(ノ-_-)ノ ミᴉᴉɔsɐ-uou", StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), None,
                     id="builtins.str unicode-codespace"),
        pytest.param(numpy.str_(""), StringValue(""), None, id="numpy.str_ empty"),
        pytest.param(numpy.str_("ASCII-only"), StringValue("ASCII-only"), None,
                     id="numpy.str_ ascii-codespace"),
        pytest.param(numpy.str_("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), None,
                     id="numpy.str_ unicode-codespace"),
        pytest.param(NotConvertible(), None, TypeError),
        pytest.param(None, None, TypeError)
    ],
)
def test_coerce(source: Any, expect: IVariableValue, expect_exception: Type[BaseException]) -> None:
    """
    Tests implicit_coerce decorator

    Parameters
    ----------
    source The source to pass to the decorated function
    expect The expected result
    expect_exception The exception to expect, or None

    Returns
    -------
    nothing
    """
    sut = Impl()
    with _create_exception_context(expect_exception):
        result = sut.variable_argument(source)
        assert type(expect) == type(result)
        assert expect == result


@implicit_coerce
def accept_real_value(value: RealValue) -> RealValue:
    """
    Test function that accepts a RealValue

    Parameters
    ----------
    value - The input value

    Returns
    -------
    The value passed to it
    """
    return value


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        (5, RealValue(5.0), None),
        (1.2, RealValue(1.2), None),
        (NotConvertible(), None, TypeError),
        (None, None, TypeError)
        # TODO: Lots more cases
    ],
)
def test_coerce_real_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept RealValue

    Parameters
    ----------
    source The source to pass to the decorated function
    expect The expected result
    expect_exception The exception to expect, or None

    Returns
    -------
    nothing
    """
    with _create_exception_context(expect_exception):
        result = accept_real_value(source)
        assert type(expect) == type(result)
        assert expect == result


@implicit_coerce
def accept_optional_real_value(value: Optional[RealValue]) -> RealValue:
    """
    Test function that accepts an Optional[RealValue]

    Parameters
    ----------
    value - The input value

    Returns
    -------
    The value passed to it
    """
    return value


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        (5, RealValue(5.0), None),
        (1.2, RealValue(1.2), None),
        (NotConvertible(), None, TypeError),
        (None, None, None)
        # TODO: Lots more cases
    ],
)
def test_coerce_optional_real_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept Optional[RealValue]

    Parameters
    ----------
    source The source to pass to the decorated function
    expect The expected result
    expect_exception The exception to expect, or None

    Returns
    -------
    nothing
    """
    with _create_exception_context(expect_exception):
        result = accept_optional_real_value(source)
        assert type(expect) == type(result)
        assert expect == result


@implicit_coerce
def accept_with_multiple_args(
    bogus: NotConvertible, value1: RealValue, value2: IVariableValue
) -> Tuple[RealValue, IVariableValue]:
    """
    Test function that accepts a RealValue

    Parameters
    ----------
    value - The input value

    Returns
    -------
    The value passed to it
    """
    return value1, value2


def test_coerce_multiple_args() -> None:
    """
    Tests implicit_coerce decorator when multiple values to be converted

    Parameters
    ----------

    Returns
    -------
    nothing
    """
    result1, result2 = accept_with_multiple_args(NotConvertible(), 2.3, 28)
    assert RealValue == type(result1)
    assert RealValue(2.3) == result1
    assert IntegerValue == type(result2)
    assert IntegerValue(28) == result2
