# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Unit tests for array_value_conversion."""
from typing import Type

import pytest

import ansys.tools.variableinterop as acvi
import ansys.tools.variableinterop.array_value_conversion as array_value_conversion
from test_utils import _assert_incompatible_types_exception, _create_exception_context


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(
            acvi.BooleanArrayValue(values=[True]),
            acvi.RealArrayValue(values=[1.0]),
            id="Boolean single value",
        ),
        pytest.param(
            acvi.BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            acvi.RealArrayValue(
                values=[[[0.0, 1.0, 0.0], [1.0, 0.0, 1.0]], [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]]
            ),
            id="Boolean 3d",
        ),
        pytest.param(
            acvi.IntegerArrayValue(values=[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, -1, -2]]]),
            acvi.RealArrayValue(
                values=[[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], [[7.0, 8.0, 9.0], [0.0, -1.0, -2.0]]]
            ),
            id="Integer 3d",
        ),
        pytest.param(
            acvi.RealArrayValue(
                values=[
                    [[1.49, 1.50, 1.51], [2.449, 2.450, 2.451]],
                    [[-1.49, -1.50, -1.51], [-2.449, -2.450, -2.451]],
                ]
            ),
            acvi.RealArrayValue(
                values=[
                    [[1.49, 1.50, 1.51], [2.449, 2.450, 2.451]],
                    [[-1.49, -1.50, -1.51], [-2.449, -2.450, -2.451]],
                ]
            ),
            id="Real 3d",
        ),
        pytest.param(
            acvi.StringArrayValue(
                values=[
                    [["1", "2.0", "3.1"], ["4", "5.", "6"]],
                    [["7", "8", "9"], ["0", "-1", "-2.1"]],
                ]
            ),
            acvi.RealArrayValue(
                values=[[[1.0, 2.0, 3.1], [4.0, 5.0, 6.0]], [[7.0, 8.0, 9.0], [0.0, -1.0, -2.1]]]
            ),
            id="String 3d",
        ),
    ],
)
def test_to_real_array_value(source: acvi.IVariableValue, expected_result: acvi.RealArrayValue):
    """
    Test behavior of to_real_array_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result : RealArrayValue
        The expected result of the test.
    """
    # SUT
    result: acvi.RealArrayValue = array_value_conversion.to_real_array_value(source)

    # Verify
    assert type(result) == acvi.RealArrayValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(
            acvi.BooleanArrayValue(values=[True]),
            acvi.IntegerArrayValue(values=[1]),
            id="Boolean single value",
        ),
        pytest.param(
            acvi.BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            acvi.IntegerArrayValue(values=[[[0, 1, 0], [1, 0, 1]], [[0, 0, 1], [1, 0, 0]]]),
            id="Boolean 3d",
        ),
        pytest.param(
            acvi.IntegerArrayValue(values=[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, -1, -2]]]),
            acvi.IntegerArrayValue(values=[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, -1, -2]]]),
            id="Integer 3d",
        ),
        pytest.param(
            acvi.RealArrayValue(values=[3.1]),
            acvi.IntegerArrayValue(values=[3]),
            id="Real single value",
        ),
        pytest.param(
            acvi.RealArrayValue(
                values=[
                    [[1.49, 1.50, 1.51], [2.449, 2.450, 2.451]],
                    [[-1.49, -1.50, -1.51], [-2.449, -2.450, -2.451]],
                ]
            ),
            acvi.IntegerArrayValue(values=[[[1, 2, 2], [2, 2, 2]], [[-1, -2, -2], [-2, -2, -2]]]),
            id="Real 3d",
        ),
        pytest.param(
            acvi.StringArrayValue(
                values=[
                    [["1.49", "1.50", "1.51"], ["2.449", "2.450", "2.451"]],
                    [["-1.49", "-1.50", "-1.51"], ["-2.449", "-2.450", "-2.451"]],
                ]
            ),
            acvi.IntegerArrayValue(values=[[[1, 2, 2], [2, 2, 2]], [[-1, -2, -2], [-2, -2, -2]]]),
            id="String 3d",
        ),
    ],
)
def test_to_integer_array_value(
    source: acvi.IVariableValue, expected_result: acvi.IntegerArrayValue
) -> None:
    """
    Test behavior of to_integer_array_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result : IntegerArrayValue
        The expected result of the test.
    """
    # SUT
    result: acvi.IntegerArrayValue = array_value_conversion.to_integer_array_value(source)

    # Verify
    assert type(result) == acvi.IntegerArrayValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(
            acvi.BooleanArrayValue(values=[True]),
            acvi.BooleanArrayValue(values=[True]),
            id="Boolean single value",
        ),
        pytest.param(
            acvi.BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            acvi.BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            id="Boolean 3d",
        ),
        pytest.param(
            acvi.IntegerArrayValue(values=[[[0, 1, 2], [3, 4, 5]], [[6, 7, 8], [0, -1, -2]]]),
            acvi.BooleanArrayValue(
                values=[
                    [[False, True, True], [True, True, True]],
                    [[True, True, True], [False, True, True]],
                ]
            ),
            id="Integer 3d",
        ),
        pytest.param(
            acvi.RealArrayValue(values=[3.1]),
            acvi.BooleanArrayValue(values=[True]),
            id="Real single value",
        ),
        pytest.param(
            acvi.RealArrayValue(
                values=[
                    [[0.0, 1.50, 0.0], [2.449, 0.0, 2.451]],
                    [[-1.49, 0.0, -1.51], [0.0, -2.450, -2.451]],
                ]
            ),
            acvi.BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[True, False, True], [False, True, True]],
                ]
            ),
            id="Real 3d",
        ),
        pytest.param(
            acvi.StringArrayValue(
                values=[
                    [["0", "1"], ["0.0", "1.0"], ["inf", "NaN"]],
                    [["no", "yes"], ["n", "y"], ["false", "true"]],
                ]
            ),
            acvi.BooleanArrayValue(
                values=[
                    [[False, True], [False, True], [True, True]],
                    [[False, True], [False, True], [False, True]],
                ]
            ),
            id="String 3d",
        ),
    ],
)
def test_to_boolean_array_value(
    source: acvi.IVariableValue, expected_result: acvi.BooleanArrayValue
) -> None:
    """
    Test behavior of to_boolean_array_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result : BooleanArrayValue
        The expected result of the test.
    """
    # SUT
    result: acvi.BooleanArrayValue = array_value_conversion.to_boolean_array_value(source)

    # Verify
    assert type(result) == acvi.BooleanArrayValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(
            acvi.BooleanArrayValue(values=[True]),
            acvi.StringArrayValue(values=["True"]),
            id="Boolean single value",
        ),
        pytest.param(
            acvi.BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            acvi.StringArrayValue(
                values=[
                    [["False", "True", "False"], ["True", "False", "True"]],
                    [["False", "False", "True"], ["True", "False", "False"]],
                ]
            ),
            id="Boolean 3d",
        ),
        pytest.param(
            acvi.IntegerArrayValue(values=[[[0, 1, 2], [3, 4, 5]], [[6, 7, 8], [0, -1, -2]]]),
            acvi.StringArrayValue(
                values=[[["0", "1", "2"], ["3", "4", "5"]], [["6", "7", "8"], ["0", "-1", "-2"]]]
            ),
            id="Integer 3d",
        ),
        pytest.param(
            acvi.RealArrayValue(values=[3.1]),
            acvi.StringArrayValue(values=["3.1"]),
            id="Real single value",
        ),
        pytest.param(
            acvi.RealArrayValue(
                values=[
                    [[0.0, 1.50, 0.0], [2.449, 0.0, 2.451]],
                    [[-1.49, 0.0, -1.51], [0.0, -2.450, -2.451]],
                ]
            ),
            acvi.StringArrayValue(
                values=[
                    [["0.0", "1.5", "0.0"], ["2.449", "0.0", "2.451"]],
                    [["-1.49", "0.0", "-1.51"], ["0.0", "-2.45", "-2.451"]],
                ]
            ),
            id="Real 3d",
        ),
        pytest.param(
            acvi.StringArrayValue(
                values=[
                    [["0", "1"], ["0.0", "1.0"]],
                    [["abc", "xyz"], ['"quoted"', "white \n\t space"]],
                ]
            ),
            acvi.StringArrayValue(
                values=[
                    [["0", "1"], ["0.0", "1.0"]],
                    [["abc", "xyz"], ['"quoted"', "white \n\t space"]],
                ]
            ),
            id="String 3d",
        ),
    ],
)
def test_to_string_array_value(
    source: acvi.IVariableValue, expected_result: acvi.StringArrayValue
) -> None:
    """
    Test behavior of to_string_array_value().

    Parameters
    ----------
    source : IVariableValue
        The IVariableValue to be converted.
    expected_result : StringArrayValue
        The expected result of the test.
    """
    # SUT
    result: acvi.StringArrayValue = array_value_conversion.to_string_array_value(source)

    # Verify
    assert type(result) == acvi.StringArrayValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(acvi.BooleanValue(True), acvi.IncompatibleTypesException, id="Boolean"),
        pytest.param(acvi.IntegerValue(1), acvi.IncompatibleTypesException, id="Integer"),
        pytest.param(acvi.RealValue(1.49), acvi.IncompatibleTypesException, id="Real"),
        pytest.param(acvi.StringValue("a string"), acvi.IncompatibleTypesException, id="String"),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", ""]]), ValueError, id="String empty"
        ),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", "garbage"]]),
            ValueError,
            id="String garbage",
        ),
    ],
)
def test_to_real_array_value_raises(
    source: acvi.IVariableValue, expected_exception: Type[BaseException]
) -> None:
    """
    Test behavior of to_real_array_value() when it is expected to raise an exception.

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
            _ = array_value_conversion.to_real_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(
                    str(e), source.__class__.__name__, acvi.RealArrayValue.__name__
                )
            raise e


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(acvi.BooleanValue(True), acvi.IncompatibleTypesException, id="Boolean"),
        pytest.param(acvi.IntegerValue(1), acvi.IncompatibleTypesException, id="Integer"),
        pytest.param(acvi.RealValue(1.49), acvi.IncompatibleTypesException, id="Real"),
        pytest.param(acvi.StringValue("a string"), acvi.IncompatibleTypesException, id="String"),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", ""]]), ValueError, id="String empty"
        ),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", "garbage"]]),
            ValueError,
            id="String garbage",
        ),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", "Inf"]]),
            OverflowError,
            id="String Inf",
        ),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", "NaN"]]),
            ValueError,
            id="String empty",
        ),
    ],
)
def test_to_integer_array_value_raises(
    source: acvi.IVariableValue, expected_exception: Type[BaseException]
) -> None:
    """
    Test behavior of to_integer_array_value() when it is expected to raise an exception.

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
            _ = array_value_conversion.to_integer_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(
                    str(e), source.__class__.__name__, acvi.IntegerArrayValue.__name__
                )
            raise e


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(acvi.BooleanValue(True), acvi.IncompatibleTypesException, id="Boolean"),
        pytest.param(acvi.IntegerValue(1), acvi.IncompatibleTypesException, id="Integer"),
        pytest.param(acvi.RealValue(1.49), acvi.IncompatibleTypesException, id="Real"),
        pytest.param(acvi.StringValue("a string"), acvi.IncompatibleTypesException, id="String"),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", ""]]), ValueError, id="String empty"
        ),
        pytest.param(
            acvi.StringArrayValue(values=[["1", "2.0"], ["4", "garbage"]]),
            ValueError,
            id="String garbage",
        ),
    ],
)
def test_to_boolean_array_value_raises(
    source: acvi.IVariableValue, expected_exception: Type[BaseException]
) -> None:
    """
    Test behavior of to_boolean_array_value() when it is expected to raise an exception.

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
            _ = array_value_conversion.to_boolean_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(
                    str(e), source.__class__.__name__, acvi.BooleanArrayValue.__name__
                )
            raise e


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        pytest.param(acvi.BooleanValue(True), acvi.IncompatibleTypesException, id="Boolean"),
        pytest.param(acvi.IntegerValue(1), acvi.IncompatibleTypesException, id="Integer"),
        pytest.param(acvi.RealValue(1.49), acvi.IncompatibleTypesException, id="Real"),
        pytest.param(acvi.StringValue("a string"), acvi.IncompatibleTypesException, id="String"),
    ],
)
def test_to_string_array_value_raises(
    source: acvi.IVariableValue, expected_exception: Type[BaseException]
) -> None:
    """
    Test behavior of to_string_array_value() when it is expected to raise an exception.

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
            _ = array_value_conversion.to_string_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(
                    str(e), source.__class__.__name__, acvi.StringArrayValue.__name__
                )
            raise e
