"""
Tests for the type coercion module
"""
from abc import ABC, abstractmethod
import numpy
import pytest
from typing import Any, Optional, Tuple
from test_utils import _create_exception_context

from ansys.common.variableinterop import (
    BooleanValue, IntegerValue, implicit_coerce, IVariableValue, RealValue, StringValue)


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
def test_coerce(source: Any, expect: IVariableValue, expect_exception: BaseException) -> None:
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


@implicit_coerce
def accept_integer_value(value: IntegerValue) -> IntegerValue:
    """
    Test function that accepts an IntegerValue

    Parameters
    ----------
    value - The input value

    Returns
    -------
    The value passed to it
    """
    return value


@implicit_coerce
def accept_boolean_value(value: BooleanValue) -> BooleanValue:
    """
    Test function that accepts a BooleanValue

    Parameters
    ----------
    value - The input value

    Returns
    -------
    The value passed to it
    """
    return value


@implicit_coerce
def accept_string_value(value: StringValue) -> StringValue:
    """
    Test function that accepts a StringValue

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
        pytest.param(5, None, TypeError, id ="builtins.int fails"),
        pytest.param(1.2, RealValue(1.2), None, id="builtins.real"),
        pytest.param(numpy.float64(-867.5309), RealValue(-867.5309), None, id="numpy.float64"),
        pytest.param(True, RealValue(1.0), None, id="builtins.bool true"),
        pytest.param(False, RealValue(0.0), None, id="builtins.bool, false"),
        pytest.param(BooleanValue(True), RealValue(1.0), None, id="BooleanValue true"),
        pytest.param(BooleanValue(False), RealValue(0.0), None, id="BooleanValue false"),
        pytest.param(RealValue(1.2), RealValue(1.2), None, id="RealValue loopback"),
        pytest.param(IntegerValue(5), None, TypeError, id="IntegerValue fails"),
        pytest.param('', None, TypeError, id="Empty string fails"),
        pytest.param('1.2', None, TypeError, id="String containing float representation fails"),
        pytest.param(StringValue(''), None, TypeError, id="StringValue empty fails"),
        pytest.param(StringValue(''), None, TypeError,
                     id="StringValue containing float representation fails"),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails.")
    ],
)
def test_coerce_real_value(
    source: Any, expect: IVariableValue, expect_exception: BaseException
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


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(numpy.int64(9223372036854775807),
                     IntegerValue(9223372036854775807), None, id="np.int64 max"),
        pytest.param(numpy.int64(-9223372036854775808),
                     IntegerValue(-9223372036854775808), None, id="np.int64 min"),
        pytest.param(9223372036854775807,
                     IntegerValue(9223372036854775807), None, id="builtins.int 64-bit max"),
        pytest.param(-9223372036854775808,
                     IntegerValue(-9223372036854775808), None, id="builtins.int 64-bit min"),
        pytest.param(True, IntegerValue(1), None, id="builtins.bool True"),
        pytest.param(numpy.bool_(True), IntegerValue(1), None, id="numpy.bool_ True"),
        pytest.param(BooleanValue(True), IntegerValue(1), None, id="BooleanValue True"),
        pytest.param(False, IntegerValue(0), None, id="builtins.bool True"),
        pytest.param(numpy.bool_(False), IntegerValue(0), None, id="numpy.bool_ True"),
        pytest.param(BooleanValue(False), IntegerValue(0), None, id="BooleanValue True"),
        pytest.param(1.2, None, TypeError, id="builtins.float fails"),
        pytest.param(1.0, None, TypeError, id="builtins.float fails even if integral value"),
        pytest.param(RealValue(1.0), None, TypeError, id="RealValue fails even if integral value"),
        pytest.param("1", None, TypeError, id="builtins.str fails even if it contains an int"),
        pytest.param(numpy.str_("1"), None, TypeError,
                     id="numpy.str_ fails even if it contains an int"),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails.")
    ],
)
def test_coerce_integer_value(
        source: Any, expect: IVariableValue, expect_exception: BaseException
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept IntegerValue

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
        result = accept_integer_value(source)
        assert type(expect) == type(result)
        assert expect == result


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(9999, StringValue("9999"), None, id="builtins.int"),
        pytest.param(numpy.int64(8675309), StringValue("8675309"), None, id="numpy.int64"),
        pytest.param(IntegerValue(-4747), StringValue("-4747"), None, id="IntegerValue"),
        pytest.param(9000.1, StringValue("9000.1"), None, id="builtins.float"),
        pytest.param(numpy.float64(867.5309), StringValue("867.5309"), None, id="numpy.float64"),
        pytest.param(RealValue(47.47), StringValue("47.47"), None, id="RealValue"),
        pytest.param(True, StringValue("True"), None, id="builtins.bool True"),
        pytest.param(False, StringValue("False"), None, id="builtins.bool False"),
        pytest.param(numpy.bool_(True), StringValue("True"), None, id="numpy.bool_ True"),
        pytest.param(numpy.bool_(False), StringValue("False"), None, id="numpy.bool_ False"),
        pytest.param(BooleanValue(True), StringValue("True"), None, id="BooleanValue True"),
        pytest.param(BooleanValue(False), StringValue("False"), None, id="BooleanValue False"),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param("(ノ-_-)ノ ミᴉᴉɔsɐ-uou", StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), None,
                     id="builtins.str"),
        pytest.param(numpy.str_("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), None,
                     id="numpy.str_"),
        pytest.param(StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
                     None, id="StringValue"),
        pytest.param(None, None, TypeError, id="NoneType fails.")
    ],
)
def test_coerce_string_value(
        source: Any, expect: IVariableValue, expect_exception: BaseException
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept StringValue

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
        result = accept_string_value(source)
        assert type(expect) == type(result)
        assert expect == result


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(numpy.int64(9223372036854775807),
                     BooleanValue(True), None, id="np.int64 max"),
        pytest.param(numpy.int64(-9223372036854775808),
                     BooleanValue(True), None, id="np.int64 min"),
        pytest.param(numpy.int64(0),
                     BooleanValue(False), None, id="np.int64 zero"),
        pytest.param(9223372036854775807,
                     BooleanValue(True), None, id="builtins.int 64-bit max"),
        pytest.param(-9223372036854775808,
                     BooleanValue(True), None, id="builtins.int 64-bit min"),
        pytest.param(0, BooleanValue(False), None, id="builtins.int zero"),
        pytest.param(IntegerValue(9223372036854775807),
                     BooleanValue(True), None, id="IntegerValue max"),
        pytest.param(IntegerValue(-9223372036854775808),
                     BooleanValue(True), None, id="IntegerValue min"),
        pytest.param(IntegerValue(0),
                     BooleanValue(False), None, id="IntegerValue zero"),
        pytest.param(-867.5309, BooleanValue(True), None, id="builtins.float negative"),
        pytest.param(867.5309, BooleanValue(True), None, id="builtins.float positive"),
        pytest.param(0.0, BooleanValue(False), None, id="builtins.float zero"),
        pytest.param(numpy.float64(-867.5309), BooleanValue(True), None,
                     id="numpy.float64 negative"),
        pytest.param(numpy.float64(867.5309), BooleanValue(True), None,
                     id="numpy.float64 positive"),
        pytest.param(numpy.float64(0.0), BooleanValue(False), None, id="numpy.float64 zero"),
        pytest.param(RealValue(-867.5309), BooleanValue(True), None,
                     id="RealValue negative"),
        pytest.param(RealValue(867.5309), BooleanValue(True), None,
                     id="RealValue positive"),
        pytest.param(RealValue(0.0), BooleanValue(False), None, id="RealValue zero"),
        pytest.param(numpy.bool_(True), BooleanValue(True), None, id="numpy.bool_ true"),
        pytest.param(numpy.bool_(False), BooleanValue(False), None, id="numpy.bool_ false"),
        pytest.param(BooleanValue(True), BooleanValue(True), None, id="BooleanValue true"),
        pytest.param(BooleanValue(False), BooleanValue(False), None, id="BooleanValue false"),
        pytest.param(True, BooleanValue(True), None, id="builtins.bool true"),
        pytest.param(False, BooleanValue(False), None, id="builtins.bool false"),
        pytest.param("true", None, TypeError, id="builtins.str fails even if it contains 'true'"),
        pytest.param(numpy.str_("true"), None, TypeError,
                     id="numpy.str_ fails even if it contains 'true'"),
        pytest.param(StringValue("true"), None, TypeError,
                     id="StringValue fails even if it contains 'true'"),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails.")
    ],
)
def test_coerce_boolean_value(
        source: Any, expect: IVariableValue, expect_exception: BaseException
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept BooleanValue

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
        result = accept_boolean_value(source)
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
        pytest.param(5, None, TypeError, id ="builtins.int fails"),
        pytest.param(1.2, RealValue(1.2), None, id="builtins.real"),
        pytest.param(True, RealValue(1.0), None, id="builtins.bool true"),
        pytest.param(False, RealValue(0.0), None, id="builtins.bool, false"),
        pytest.param(BooleanValue(True), RealValue(1.0), None, id="BooleanValue true"),
        pytest.param(BooleanValue(False), RealValue(0.0), None, id="BooleanValue false"),
        pytest.param(RealValue(1.2), RealValue(1.2), None, id="RealValue loopback"),
        pytest.param(IntegerValue(5), None, TypeError, id="IntegerValue fails"),
        pytest.param('', None, TypeError, id="Empty string fails"),
        pytest.param('1.2', None, TypeError, id="String containing float representation fails"),
        pytest.param(StringValue(''), None, TypeError, id="StringValue empty fails"),
        pytest.param(StringValue(''), None, TypeError,
                     id="StringValue containing float representation fails"),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, None, id="None coerced to None")
    ],
)
def test_coerce_optional_real_value(
    source: Any, expect: IVariableValue, expect_exception: BaseException
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
