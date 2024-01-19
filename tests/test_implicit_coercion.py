# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Tests for the implicit type coercion module."""
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple, Type

import numpy
import pytest

from ansys.tools.variableinterop import (
    BooleanArrayValue,
    BooleanValue,
    IntegerArrayValue,
    IntegerValue,
    IVariableValue,
    RealArrayValue,
    RealValue,
    StringArrayValue,
    StringValue,
    implicit_coerce,
)
from test_utils import _create_exception_context


class IDummy(ABC):
    """Example interface that accepts variable types."""

    @abstractmethod
    def variable_argument(self, value: IVariableValue) -> IVariableValue:
        ...


class Impl(ABC):
    """Test implementation that just returns what it gets sent."""

    @implicit_coerce
    def variable_argument(self, value: IVariableValue) -> IVariableValue:
        return value


class NotConvertible:
    """Test object that can't be converted to an IVariableValue."""

    pass


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(0, IntegerValue(0), None, id="builtins.int 0"),
        pytest.param(numpy.int8(127), IntegerValue(127), None, id="np.int8 max"),
        pytest.param(numpy.int16(32767), IntegerValue(32767), None, id="np.int16 max"),
        pytest.param(numpy.int32(2147483647), IntegerValue(2147483647), None, id="np.int32 max"),
        pytest.param(
            numpy.int64(9223372036854775807),
            IntegerValue(9223372036854775807),
            None,
            id="np.int64 max",
        ),
        pytest.param(numpy.int8(-128), IntegerValue(-128), None, id="np.int8 min"),
        pytest.param(numpy.int16(-32768), IntegerValue(-32768), None, id="np.int16 min"),
        pytest.param(numpy.int32(-2147483648), IntegerValue(-2147483648), None, id="np.int32 min"),
        pytest.param(
            numpy.int64(-9223372036854775808),
            IntegerValue(-9223372036854775808),
            None,
            id="np.int64 min",
        ),
        pytest.param(-9223372036854775809, None, OverflowError, id="builtins.int under 64-bit min"),
        pytest.param(1.2, RealValue(1.2), None, id="builtins.float 1.2"),
        pytest.param(
            numpy.float16(-867.5309), RealValue(numpy.float16(-867.5309)), None, id="numpy.float16"
        ),
        pytest.param(numpy.float32(0.0), RealValue(0.0), None, id="np.float32 0.0"),
        pytest.param(numpy.float32(-1.0), RealValue(-1.0), None, id="np.float32 -1.0"),
        pytest.param(
            numpy.float32(867.5309),
            RealValue(numpy.float32(867.5309)),
            None,
            id="np.float32 867.5309",
        ),
        pytest.param(numpy.float64(9000.1), RealValue(9000.1), None, id="np.float64 9000.1"),
        pytest.param(
            numpy.float64(2.2250738585072014e-308),
            RealValue(2.2250738585072014e-308),
            None,
            id="float64 smallest-normal",
        ),
        pytest.param(
            numpy.float64(1.7976931348623157e308),
            RealValue(1.7976931348623157e308),
            None,
            id="float64 abs-max",
        ),
        pytest.param(
            numpy.float64(-1.7976931348623157e308),
            RealValue(-1.7976931348623157e308),
            None,
            id="float64 abs-min",
        ),
        pytest.param(True, BooleanValue(True), None, id="builtins.bool true"),
        pytest.param(False, BooleanValue(False), None, id="builtins.bool false"),
        pytest.param(numpy.bool_(True), BooleanValue(True), None, id="builtins.bool true"),
        pytest.param(numpy.bool_(False), BooleanValue(False), None, id="builtins.bool false"),
        pytest.param("", StringValue(""), None, id="builtins.str empty"),
        pytest.param(
            "ASCII-only", StringValue("ASCII-only"), None, id="builtins.str ascii-codespace"
        ),
        pytest.param(
            "(ノ-_-)ノ ミᴉᴉɔsɐ-uou",
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            None,
            id="builtins.str unicode-codespace",
        ),
        pytest.param(numpy.str_(""), StringValue(""), None, id="numpy.str_ empty"),
        pytest.param(
            numpy.str_("ASCII-only"),
            StringValue("ASCII-only"),
            None,
            id="numpy.str_ ascii-codespace",
        ),
        pytest.param(
            numpy.str_("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            None,
            id="numpy.str_ unicode-codespace",
        ),
        pytest.param(
            numpy.array([8, 6, 7, 5, 3, 0, 9], dtype=numpy.int64),
            IntegerArrayValue(values=[8, 6, 7, 5, 3, 0, 9]),
            None,
            id="numpy.ndarray[int64]",
        ),
        pytest.param(
            numpy.array([8.6, 7.5, 3.09], dtype=numpy.float64),
            RealArrayValue(values=[8.6, 7.5, 3.09]),
            None,
            id="numpy.ndarray[float64]",
        ),
        pytest.param(
            numpy.array([True, False, True], dtype=numpy.bool_),
            BooleanArrayValue(values=[True, False, True]),
            None,
            id="numpy.ndarray[bool_]",
        ),
        pytest.param(
            numpy.array(["lorem", "ipsum", "dolor"], dtype=numpy.str_),
            StringArrayValue(values=["lorem", "ipsum", "dolor"]),
            None,
            id="numpy.ndarray[str_]",
        ),
        pytest.param(
            numpy.array(["mixed", True, 4.57, None], dtype=object),
            None,
            TypeError,
            id="numpy.ndarray[object]",
        ),
        pytest.param(numpy.longdouble(-867.5309), None, TypeError, id="numpy.longdouble fails"),
        pytest.param(numpy.complex_(-867.5309), None, TypeError, id="numpy.complex_ fails"),
        pytest.param(complex(-867.5309), None, TypeError, id="builtins.complex fails"),
        pytest.param(NotConvertible(), None, TypeError),
        pytest.param(None, None, TypeError),
    ],
)
def test_coerce(source: Any, expect: IVariableValue, expect_exception: Type[BaseException]) -> None:
    """
    Tests implicit_coerce decorator.

    Parameters
    ----------
    source The source to pass to the decorated function
    expect The expected result
    expect_exception The exception to expect, or None

    Returns
    -------
    None
    """
    sut = Impl()
    with _create_exception_context(expect_exception):
        result = sut.variable_argument(source)
        assert type(expect) == type(result)
        assert expect == result


@implicit_coerce
def accept_real_value(value: RealValue) -> RealValue:
    """
    Test function that accepts a RealValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    RealValue
        The value passed to it
    """
    return value


@implicit_coerce
def accept_real_array_value(value: RealArrayValue) -> RealArrayValue:
    """
    Test function that accepts a RealValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    RealArrayValue
        The value passed to it
    """
    return value


@implicit_coerce
def accept_integer_value(value: IntegerValue) -> IntegerValue:
    """
    Test function that accepts an IntegerValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    IntegerValue
        The value passed to it
    """
    return value


@implicit_coerce
def accept_integer_array_value(value: IntegerArrayValue) -> IntegerArrayValue:
    """
    Test function that accepts an IntegerArrayValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    IntegerArrayValue
        The value passed to it
    """
    return value


@implicit_coerce
def accept_boolean_value(value: BooleanValue) -> BooleanValue:
    """
    Test function that accepts a BooleanValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    BooleanValue
        The value passed to it
    """
    return value


@implicit_coerce
def accept_boolean_array_value(value: BooleanArrayValue) -> BooleanArrayValue:
    """
    Test function that accepts a BooleanArrayValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    BooleanArrayValue
        The value passed to it
    """
    return value


@implicit_coerce
def accept_string_value(value: StringValue) -> StringValue:
    """
    Test function that accepts a StringValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    StringValue
        The value passed to it
    """
    return value


@implicit_coerce
def accept_string_array_value(value: StringArrayValue) -> StringArrayValue:
    """
    Test function that accepts a StringArrayValue.

    Parameters
    ----------
    value - The input value

    Returns
    -------
    StringArrayValue
        The value passed to it
    """
    return value


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(5, None, TypeError, id="builtins.int fails"),
        pytest.param(1.2, RealValue(1.2), None, id="builtins.real"),
        pytest.param(
            numpy.float16(-867.5309), RealValue(numpy.float16(-867.5309)), None, id="numpy.float16"
        ),
        pytest.param(
            numpy.float32(-867.5309), RealValue(numpy.float32(-867.5309)), None, id="numpy.float32"
        ),
        pytest.param(numpy.float64(-867.5309), RealValue(-867.5309), None, id="numpy.float64"),
        pytest.param(True, RealValue(1.0), None, id="builtins.bool true"),
        pytest.param(False, RealValue(0.0), None, id="builtins.bool, false"),
        pytest.param(BooleanValue(True), RealValue(1.0), None, id="BooleanValue true"),
        pytest.param(BooleanValue(False), RealValue(0.0), None, id="BooleanValue false"),
        pytest.param(RealValue(1.2), RealValue(1.2), None, id="RealValue loopback"),
        pytest.param(numpy.longdouble(-867.5309), None, TypeError, id="numpy.longdouble fails"),
        pytest.param(numpy.complex_(-867.5309), None, TypeError, id="numpy.complex_ fails"),
        pytest.param(complex(-867.5309), None, TypeError, id="builtins.complex fails"),
        pytest.param(IntegerValue(5), None, TypeError, id="IntegerValue fails"),
        pytest.param("", None, TypeError, id="Empty string fails"),
        pytest.param("1.2", None, TypeError, id="String containing float representation fails"),
        pytest.param(StringValue(""), None, TypeError, id="StringValue empty fails"),
        pytest.param(
            StringValue(""), None, TypeError, id="StringValue containing float representation fails"
        ),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(numpy.float64(-867.5309), RealValue(-867.5309), None, id="numpy.float64"),
        pytest.param(None, None, TypeError, id="NoneType fails."),
        pytest.param(IntegerArrayValue(values=[1]), None, TypeError, id="IntegerArrayValue"),
        pytest.param(RealArrayValue(values=[1.0]), None, TypeError, id="RealArrayValue"),
        pytest.param(BooleanArrayValue(values=[True]), None, TypeError, id="BooleanArrayValue"),
        pytest.param(StringArrayValue(values=["1"]), None, TypeError, id="StringArrayValue"),
    ],
)
def test_coerce_real_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    RealValue.

    Parameters
    ----------
    source The source to pass to the decorated function
    expect The expected result
    expect_exception The exception to expect, or None

    Returns
    -------
    None
    """
    with _create_exception_context(expect_exception):
        result = accept_real_value(source)
        assert type(expect) == type(result)
        assert expect == result


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(
            numpy.array(
                [-1.7976931348623157e308, 0.0, 2.2250738585072014e-308, 1.7976931348623157e308],
                dtype=numpy.float64,
            ),
            RealArrayValue(
                values=[
                    -1.7976931348623157e308,
                    0.0,
                    2.2250738585072014e-308,
                    1.7976931348623157e308,
                ]
            ),
            None,
            id="np.ndarray[float64]",
        ),
        pytest.param(
            RealArrayValue(
                values=[
                    -1.7976931348623157e308,
                    0.0,
                    2.2250738585072014e-308,
                    1.7976931348623157e308,
                ]
            ),
            RealArrayValue(
                values=[
                    -1.7976931348623157e308,
                    0.0,
                    2.2250738585072014e-308,
                    1.7976931348623157e308,
                ]
            ),
            None,
            id="RealArrayValue loopback",
        ),
        pytest.param(
            numpy.array([True, False, True], dtype=numpy.bool_),
            RealArrayValue(values=[1.0, 0.0, 1.0]),
            None,
            id="np.ndarray[bool_]",
        ),
        pytest.param(
            BooleanArrayValue(values=[True, False, True]),
            RealArrayValue(values=[1.0, 0.0, 1.0]),
            None,
            id="BooleanArrayValue",
        ),
        pytest.param(
            numpy.array([1.0], dtype=numpy.longdouble), None, TypeError, id="np.ndarray[longdouble]"
        ),
        pytest.param(
            numpy.array(["mixed", True, 4.57, None], dtype=object),
            None,
            TypeError,
            id="numpy.ndarray[object]",
        ),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(1, None, TypeError, id="Scalar int fails"),
        pytest.param(True, None, TypeError, id="Scalar bool fails"),
        pytest.param(None, None, TypeError, id="NoneType fails."),
        pytest.param(IntegerArrayValue(values=[1]), None, TypeError, id="IntegerArrayValue"),
        pytest.param(StringArrayValue(values=["1"]), None, TypeError, id="StringArrayValue"),
    ],
)
def test_coerce_real_array_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    RealValue.

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
        result = accept_real_array_value(source)
        assert type(expect) == type(result)
        assert expect == result


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(numpy.int8(127), IntegerValue(127), None, id="np.int8 max"),
        pytest.param(numpy.int8(-128), IntegerValue(-128), None, id="np.int8 min"),
        pytest.param(numpy.int16(32767), IntegerValue(32767), None, id="np.int16 max"),
        pytest.param(numpy.int16(-32768), IntegerValue(-32768), None, id="np.int16 min"),
        pytest.param(numpy.int32(2147483647), IntegerValue(2147483647), None, id="np.int32 max"),
        pytest.param(numpy.int32(-2147483648), IntegerValue(-2147483648), None, id="np.int32 min"),
        pytest.param(
            numpy.int64(9223372036854775807),
            IntegerValue(9223372036854775807),
            None,
            id="np.int64 max",
        ),
        pytest.param(
            numpy.int64(-9223372036854775808),
            IntegerValue(-9223372036854775808),
            None,
            id="np.int64 min",
        ),
        pytest.param(
            9223372036854775807,
            IntegerValue(9223372036854775807),
            None,
            id="builtins.int 64-bit max",
        ),
        pytest.param(
            -9223372036854775808,
            IntegerValue(-9223372036854775808),
            None,
            id="builtins.int 64-bit min",
        ),
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
        pytest.param(
            numpy.str_("1"), None, TypeError, id="numpy.str_ fails even if it contains an int"
        ),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails."),
        pytest.param(IntegerArrayValue(values=[1]), None, TypeError, id="IntegerArrayValue"),
        pytest.param(RealArrayValue(values=[1.0]), None, TypeError, id="RealArrayValue"),
        pytest.param(BooleanArrayValue(values=[True]), None, TypeError, id="BooleanArrayValue"),
        pytest.param(StringArrayValue(values=["1"]), None, TypeError, id="StringArrayValue"),
    ],
)
def test_coerce_integer_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    IntegerValue.

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
        pytest.param(
            numpy.array([127, 0, -128], dtype=numpy.int8),
            IntegerArrayValue(values=[127, 0, -128]),
            None,
            id="np.ndarray[int8]",
        ),
        pytest.param(
            numpy.array([32767, 0, -32768], dtype=numpy.int16),
            IntegerArrayValue(values=[32767, 0, -32768]),
            None,
            id="np.ndarray[int16]",
        ),
        pytest.param(
            numpy.array([2147483647, 0, -2147483648], dtype=numpy.int32),
            IntegerArrayValue(values=[2147483647, 0, -2147483648]),
            None,
            id="np.ndarray[int32]",
        ),
        pytest.param(
            numpy.array([9223372036854775807, 0, -9223372036854775808], dtype=numpy.int64),
            IntegerArrayValue(values=[9223372036854775807, 0, -9223372036854775808]),
            None,
            id="np.ndarray[int64]",
        ),
        pytest.param(
            numpy.array([True, False, True], dtype=numpy.bool_),
            IntegerArrayValue(values=[1, 0, 1]),
            None,
            id="np.ndarray[bool_]",
        ),
        pytest.param(
            IntegerArrayValue(values=[9223372036854775807, 0, -9223372036854775808]),
            IntegerArrayValue(values=[9223372036854775807, 0, -9223372036854775808]),
            None,
            id="IntegerArrayValue",
        ),
        pytest.param(
            BooleanArrayValue(values=[True, False, True]),
            IntegerArrayValue(values=[1, 0, 1]),
            None,
            id="BooleanArrayValue",
        ),
        pytest.param(
            numpy.array([1.0, 2.7], dtype=numpy.float64), None, TypeError, id="float64 array fails"
        ),
        pytest.param(
            numpy.array(["1", "2"], dtype=numpy.str_), None, TypeError, id="str array fails"
        ),
        pytest.param(
            numpy.array(["mixed", True, 4.57, None], dtype=object),
            None,
            TypeError,
            id="numpy.ndarray[object]",
        ),
        pytest.param(0, None, TypeError, id="scalar int fails"),
        pytest.param(numpy.int64(0), None, TypeError, id="scalar np.int64 fails"),
        pytest.param(IntegerValue(0), None, TypeError, id="scalar IntegerValue fails"),
        pytest.param(True, None, TypeError, id="scalar bool fails"),
        pytest.param(numpy.bool_(True), None, TypeError, id="scalar np.bool_ fails"),
        pytest.param(BooleanValue(True), None, TypeError, id="scalar BooleanValue fails"),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails."),
    ],
)
def test_coerce_integer_array_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    IntegerArrayValue.

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
        result = accept_integer_array_value(source)
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
        pytest.param(
            "(ノ-_-)ノ ミᴉᴉɔsɐ-uou", StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), None, id="builtins.str"
        ),
        pytest.param(
            numpy.str_("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            None,
            id="numpy.str_",
        ),
        pytest.param(
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            None,
            id="StringValue",
        ),
        pytest.param(None, None, TypeError, id="NoneType fails."),
        pytest.param(IntegerArrayValue(values=[1]), None, TypeError, id="IntegerArrayValue"),
        pytest.param(RealArrayValue(values=[1.0]), None, TypeError, id="RealArrayValue"),
        pytest.param(BooleanArrayValue(values=[True]), None, TypeError, id="BooleanArrayValue"),
        pytest.param(StringArrayValue(values=["1"]), None, TypeError, id="StringArrayValue"),
    ],
)
def test_coerce_string_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    StringValue.

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
        pytest.param(
            numpy.array([9223372036854775807, 0, -9223372036854775808], dtype=numpy.int64),
            StringArrayValue(values=["9223372036854775807", "0", "-9223372036854775808"]),
            None,
            id="np.ndarray[int64]",
        ),
        pytest.param(
            numpy.array([True, False, True], dtype=numpy.bool_),
            StringArrayValue(values=["True", "False", "True"]),
            None,
            id="np.ndarray[bool_]",
        ),
        pytest.param(
            IntegerArrayValue(values=["9223372036854775807", "0", "-9223372036854775808"]),
            StringArrayValue(values=["9223372036854775807", "0", "-9223372036854775808"]),
            None,
            id="IntegerArrayValue",
        ),
        pytest.param(
            BooleanArrayValue(values=[True, False, True]),
            StringArrayValue(values=["True", "False", "True"]),
            None,
            id="BooleanArrayValue",
        ),
        pytest.param(
            numpy.array(
                [-1.7976931348623157e308, 0.0, 2.2250738585072014e-308, 1.7976931348623157e308],
                dtype=numpy.float64,
            ),
            StringArrayValue(
                values=[
                    "-1.7976931348623157e+308",
                    "0.0",
                    "2.2250738585072014e-308",
                    "1.7976931348623157e+308",
                ]
            ),
            None,
            id="np.ndarray[float64]",
        ),
        pytest.param(
            RealArrayValue(
                values=[
                    -1.7976931348623157e308,
                    0.0,
                    2.2250738585072014e-308,
                    1.7976931348623157e308,
                ]
            ),
            StringArrayValue(
                values=[
                    "-1.7976931348623157e+308",
                    "0.0",
                    "2.2250738585072014e-308",
                    "1.7976931348623157e+308",
                ]
            ),
            None,
            id="RealArrayValue",
        ),
        pytest.param(
            numpy.array(["strings", "are", "fun"], dtype=numpy.str_),
            StringArrayValue(values=["strings", "are", "fun"]),
            None,
            id="np.ndarray[str_]",
        ),
        pytest.param(
            StringArrayValue(values=["strings", "are", "fun"]),
            StringArrayValue(values=["strings", "are", "fun"]),
            None,
            id="StringArrayValue",
        ),
        pytest.param(
            numpy.array(["mixed", True, 4.57, None], dtype=object),
            None,
            TypeError,
            id="numpy.ndarray[object]",
        ),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails."),
    ],
)
def test_coerce_string_array_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    StringValue.

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
        result = accept_string_array_value(source)
        assert type(expect) == type(result)
        assert expect == result


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(numpy.int64(0), None, TypeError, id="np.int64 zero"),
        pytest.param(0, None, TypeError, id="builtins.int zero"),
        pytest.param(IntegerValue(0), None, TypeError, id="IntegerValue zero"),
        pytest.param(0.0, None, TypeError, id="builtins.float zero"),
        pytest.param(numpy.float64(0.0), None, TypeError, id="numpy.float64 zero"),
        pytest.param(RealValue(0.0), None, TypeError, id="RealValue zero"),
        pytest.param(numpy.bool_(True), BooleanValue(True), None, id="numpy.bool_ true"),
        pytest.param(numpy.bool_(False), BooleanValue(False), None, id="numpy.bool_ false"),
        pytest.param(BooleanValue(True), BooleanValue(True), None, id="BooleanValue true"),
        pytest.param(BooleanValue(False), BooleanValue(False), None, id="BooleanValue false"),
        pytest.param(True, BooleanValue(True), None, id="builtins.bool true"),
        pytest.param(False, BooleanValue(False), None, id="builtins.bool false"),
        pytest.param("true", None, TypeError, id="builtins.str fails even if it contains 'true'"),
        pytest.param(
            numpy.str_("true"), None, TypeError, id="numpy.str_ fails even if it contains 'true'"
        ),
        pytest.param(
            StringValue("true"), None, TypeError, id="StringValue fails even if it contains 'true'"
        ),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails."),
        pytest.param(IntegerArrayValue(values=[1]), None, TypeError, id="IntegerArrayValue"),
        pytest.param(RealArrayValue(values=[1.0]), None, TypeError, id="RealArrayValue"),
        pytest.param(BooleanArrayValue(values=[True]), None, TypeError, id="BooleanArrayValue"),
        pytest.param(StringArrayValue(values=["1"]), None, TypeError, id="StringArrayValue"),
    ],
)
def test_coerce_boolean_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    BooleanValue.

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


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(
            numpy.array([True, False, True, False], dtype=numpy.bool_),
            BooleanArrayValue(values=[True, False, True, False]),
            None,
            id="numpy.ndarray[bool]",
        ),
        pytest.param(
            BooleanArrayValue(values=[True, False, True, False]),
            BooleanArrayValue(values=[True, False, True, False]),
            None,
            id="BooleanArrayValue loopback",
        ),
        pytest.param(
            numpy.array(["mixed", True, 4.57, None], dtype=object),
            None,
            TypeError,
            id="numpy.ndarray[object]",
        ),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, TypeError, id="NoneType fails."),
        pytest.param(IntegerArrayValue(values=[1]), None, TypeError, id="IntegerArrayValue"),
        pytest.param(RealArrayValue(values=[1.0]), None, TypeError, id="RealArrayValue"),
        pytest.param(StringArrayValue(values=["1"]), None, TypeError, id="StringArrayValue"),
    ],
)
def test_coerce_boolean_array_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    BooleanValue.

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
        result = accept_boolean_array_value(source)
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
        pytest.param(5, None, TypeError, id="builtins.int fails"),
        pytest.param(1.2, RealValue(1.2), None, id="builtins.real"),
        pytest.param(True, RealValue(1.0), None, id="builtins.bool true"),
        pytest.param(False, RealValue(0.0), None, id="builtins.bool, false"),
        pytest.param(BooleanValue(True), RealValue(1.0), None, id="BooleanValue true"),
        pytest.param(BooleanValue(False), RealValue(0.0), None, id="BooleanValue false"),
        pytest.param(RealValue(1.2), RealValue(1.2), None, id="RealValue loopback"),
        pytest.param(IntegerValue(5), None, TypeError, id="IntegerValue fails"),
        pytest.param("", None, TypeError, id="Empty string fails"),
        pytest.param("1.2", None, TypeError, id="String containing float representation fails"),
        pytest.param(StringValue(""), None, TypeError, id="StringValue empty fails"),
        pytest.param(
            StringValue(""), None, TypeError, id="StringValue containing float representation fails"
        ),
        pytest.param(NotConvertible(), None, TypeError, id="random other type fails"),
        pytest.param(None, None, None, id="None coerced to None"),
    ],
)
def test_coerce_optional_real_value(
    source: Any, expect: IVariableValue, expect_exception: Type[BaseException]
) -> None:
    """
    Tests implicit_coerce decorator when calling a function declared to accept
    Optional[RealValue]

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
    Test function that accepts a RealValue.

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
    Tests implicit_coerce decorator when multiple values to be converted.

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


@pytest.mark.parametrize(
    "arg",
    [
        pytest.param(RealValue(42), id="RealValue"),
        pytest.param(IntegerValue(9001), id="IntegerValue"),
        pytest.param(BooleanValue(True), id="BooleanValue"),
        pytest.param(StringValue("string data"), id="StringValue"),
        pytest.param(RealArrayValue(values=[42.4, 48.5, 900.2]), id="RealArrayValue"),
        pytest.param(IntegerArrayValue(values=[9001, 0, 1, 2]), id="IntegerArrayValue"),
        pytest.param(BooleanArrayValue(values=[True, False, True]), id="BooleanArrayValue"),
        pytest.param(StringArrayValue(values=["lorem", "ipsum", "dolor"]), id="StringArrayValue"),
    ],
)
def test_no_coerce_no_copy(arg: IVariableValue) -> None:
    """
    Verifies that if no type coercion is necessary, no unnecessary copies are made.

    Parameters
    ----------
    arg the argument to pass to the decorated function
    """
    # Setup
    sut = Impl()

    # Execute
    result = sut.variable_argument(arg)

    # Verify
    assert result is arg, "No copy should have been made"


def test_coerce_failure_message_scalar_free() -> None:
    sut = Impl()

    try:
        result = sut.variable_argument(NotConvertible())
        assert False, "Should have failed by now"
    except TypeError as thrown:
        print(thrown)
        assert (
            str(thrown) == f"Implicit coercion from {NotConvertible} to "
            f"{IVariableValue} is not allowed. "
            "An explicit conversion may exist."
        )


def test_coerce_failure_message_array_free() -> None:
    sut = Impl()

    try:
        result = sut.variable_argument(numpy.array([], dtype=object))
        assert False, "Should have failed by now"
    except TypeError as thrown:
        print(thrown)
        assert (
            str(thrown) == f"Implicit coercion from {numpy.ndarray} "
            f"with dtype {numpy.object_} to "
            f"{IVariableValue} is not allowed. "
            "An explicit conversion may exist."
        )


def test_coerce_failure_message_scalar_specific() -> None:
    try:
        result = accept_real_value("string")
        assert False, "Should have failed by now"
    except TypeError as thrown:
        print(thrown)
        assert (
            str(thrown) == f"Implicit coercion from {str} to "
            f"{RealValue} is not allowed. "
            "An explicit conversion may exist."
        )


def test_coerce_failure_message_array_specific() -> None:
    try:
        result = accept_real_array_value("string")
        assert False, "Should have failed by now"
    except TypeError as thrown:
        print(thrown)
        assert (
            str(thrown) == f"Implicit coercion from {str} to "
            f"{RealArrayValue} is not allowed. "
            "An explicit conversion may exist."
        )


def test_coerce_failure_message_array_free_source_array() -> None:
    try:
        result = accept_real_array_value(numpy.array([], dtype=object))
        assert False, "Should have failed by now"
    except TypeError as thrown:
        print(thrown)
        assert (
            str(thrown) == f"Implicit coercion from {numpy.ndarray} "
            f"with dtype {numpy.object_} to "
            f"{RealArrayValue} is not allowed. "
            "An explicit conversion may exist."
        )
