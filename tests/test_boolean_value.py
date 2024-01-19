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
from typing import Any, Callable, List, Tuple, Type, Union

import numpy as np
import pytest

import ansys.tools.variableinterop as acvi
from test_utils import _create_exception_context

# region bool-ness

BooleanTypes = Union[bool, np.bool_, acvi.BooleanValue]
"""Union of the "Boolean" types under test."""

boolean_types: List[Type] = [bool, np.bool_, acvi.BooleanValue]
"""List of "Boolean" types to test."""

boolean_values: List[bool] = [True, False]
"""List of "Boolean" values to test."""


def cross_types(source: List[Tuple[Any, ...]]):
    """Given a list of test tuples, build a list where for each test given there is one
    test for each type in boolean_types."""
    r = []
    for test in source:
        for type_ in boolean_types:
            t = (test[0], type_) + test[1:]
            r.append(t)
    return r


unary_tests: List[Tuple[Any, ...]] = [
    ("identity", True, lambda a: a, True),
    ("identity", False, lambda a: a, False),
    ("not", True, lambda a: not a, False),
    ("not", False, lambda a: not a, True),
    ("bool", True, lambda a: bool(a), True),
    ("bool", False, lambda a: bool(a), False),
    # ~
]
"""
List of unary operation tests.

Each tuple is in the order:
identifier, value, operator, expected
"""

unary_boolean_types_tests = cross_types(unary_tests)
"""List of unary operation test for each boolean type under test."""


@pytest.mark.parametrize("_,type_,value,operator,expected", unary_boolean_types_tests)
def test_boolean_unary_operators(
    _: str,
    type_: Type,
    value: bool,
    operator: Callable[[BooleanTypes], BooleanTypes],
    expected: bool,
):
    """
    Testing of unary operators against the different Boolean types to see what bool and
    numpy.bool_ do and to see if BooleanValue is consistent with numpy.bool_.

    Parameters
    ----------
    _ : str
        An identifier of the operator testing.
    type_ : Type
        The type of Boolean to test: bool, numpy.bool_ or BooleanValue.
    value : bool
        The value of the Boolean operand to test.
    operator : Callable[[BooleanTypes], BooleanTypes]
        A lambda or function that represents the unary operation.
    expected : bool
        The value of the expected Boolean results.
    """
    # Setup
    operand = type_(value)

    # SUT
    result = operator(operand)

    # Verify logical value of results
    assert expected == result
    # Verify type of results is either bool or same as operand
    result_type = type(result)
    assert isinstance(result, (bool, type_)), f"type of results is {result_type}"


binary_tests: List[Tuple[Any, ...]] = [
    # addition
    ("addition", False, False, lambda a, b: a + b, 0, np.False_, None),
    ("addition", False, True, lambda a, b: a + b, 1, np.True_, None),
    ("addition", True, False, lambda a, b: a + b, 1, np.True_, None),
    ("addition", True, True, lambda a, b: a + b, 2, np.True_, None),
    # subtraction
    ("subtraction", False, False, lambda a, b: a - b, 0, TypeError, None),
    ("subtraction", False, True, lambda a, b: a - b, -1, TypeError, None),
    ("subtraction", True, False, lambda a, b: a - b, 1, TypeError, None),
    ("subtraction", True, True, lambda a, b: a - b, 0, TypeError, None),
    # multiplication
    ("multiplication", False, False, lambda a, b: a * b, 0, np.False_, None),
    ("multiplication", False, True, lambda a, b: a * b, 0, np.False_, None),
    ("multiplication", True, False, lambda a, b: a * b, 0, np.False_, None),
    ("multiplication", True, True, lambda a, b: a * b, 1, np.True_, None),
    # division
    ("division", False, False, lambda a, b: a / b, ZeroDivisionError, np.float64("NaN"), None),
    ("division", False, True, lambda a, b: a / b, 0.0, np.float64(0.0), None),
    ("division", True, False, lambda a, b: a / b, ZeroDivisionError, np.float64("inf"), None),
    ("division", True, True, lambda a, b: a / b, 1.0, np.float64(1.0), None),
    # modulus
    ("modulus", False, False, lambda a, b: a % b, ZeroDivisionError, np.int8(0), None),
    ("modulus", False, True, lambda a, b: a % b, 0, np.int8(0), None),
    ("modulus", True, False, lambda a, b: a % b, ZeroDivisionError, np.int8(0), None),
    ("modulus", True, True, lambda a, b: a % b, 0, np.int8(0), None),
    # exponentiation
    ("exponentiation", False, False, lambda a, b: a**b, 1, np.int8(1), None),
    ("exponentiation", False, True, lambda a, b: a**b, 0, np.int8(0), None),
    ("exponentiation", True, False, lambda a, b: a**b, 1, np.int8(1), None),
    ("exponentiation", True, True, lambda a, b: a**b, 1, np.int8(1), None),
    # floor-division
    ("floor-division", False, False, lambda a, b: a // b, ZeroDivisionError, np.int8(0), None),
    ("floor-division", False, True, lambda a, b: a // b, 0, np.int8(0), None),
    ("floor-division", True, False, lambda a, b: a // b, ZeroDivisionError, np.int8(0), None),
    ("floor-division", True, True, lambda a, b: a // b, 1, np.int8(1), None),
    # equal
    ("equal", False, False, lambda a, b: a == b, True, np.True_, None),
    ("equal", False, True, lambda a, b: a == b, False, np.False_, None),
    ("equal", True, False, lambda a, b: a == b, False, np.False_, None),
    ("equal", True, True, lambda a, b: a == b, True, np.True_, None),
    # not equal
    ("not-equal", False, False, lambda a, b: a != b, False, np.False_, None),
    ("not-equal", False, True, lambda a, b: a != b, True, np.True_, None),
    ("not-equal", True, False, lambda a, b: a != b, True, np.True_, None),
    ("not-equal", True, True, lambda a, b: a != b, False, np.False_, None),
    # greater than
    ("greater-than", False, False, lambda a, b: a > b, False, np.False_, None),
    ("greater-than", False, True, lambda a, b: a > b, False, np.False_, None),
    ("greater-than", True, False, lambda a, b: a > b, True, np.True_, None),
    ("greater-than", True, True, lambda a, b: a > b, False, np.False_, None),
    # less than
    ("less-than", False, False, lambda a, b: a < b, False, np.False_, None),
    ("less-than", False, True, lambda a, b: a < b, True, np.True_, None),
    ("less-than", True, False, lambda a, b: a < b, False, np.False_, None),
    ("less-than", True, True, lambda a, b: a < b, False, np.False_, None),
    # greater than or equal
    ("greater-than-or-equal", False, False, lambda a, b: a >= b, True, np.True_, None),
    ("greater-than-or-equal", False, True, lambda a, b: a >= b, False, np.False_, None),
    ("greater-than-or-equal", True, False, lambda a, b: a >= b, True, np.True_, None),
    ("greater-than-or-equal", True, True, lambda a, b: a >= b, True, np.True_, None),
    # less than or equal
    ("less-than-or-equal", False, False, lambda a, b: a <= b, True, np.True_, None),
    ("less-than-or-equal", False, True, lambda a, b: a <= b, True, np.True_, None),
    ("less-than-or-equal", True, False, lambda a, b: a <= b, False, np.False_, None),
    ("less-than-or-equal", True, True, lambda a, b: a <= b, True, np.True_, None),
    # and
    ("and", False, False, lambda a, b: a and b, False, np.False_, acvi.BooleanValue(False)),
    ("and", False, True, lambda a, b: a and b, False, np.False_, acvi.BooleanValue(False)),
    ("and", True, False, lambda a, b: a and b, False, np.False_, acvi.BooleanValue(False)),
    ("and", True, True, lambda a, b: a and b, True, np.True_, acvi.BooleanValue(True)),
    # or
    ("or", False, False, lambda a, b: a or b, False, np.False_, acvi.BooleanValue(False)),
    ("or", False, True, lambda a, b: a or b, True, np.True_, acvi.BooleanValue(True)),
    ("or", True, False, lambda a, b: a or b, True, np.True_, acvi.BooleanValue(True)),
    ("or", True, True, lambda a, b: a or b, True, np.True_, acvi.BooleanValue(True)),
    # is
    # is not
    # &
    ("&", False, False, lambda a, b: a & b, False, np.False_, None),
    ("&", False, True, lambda a, b: a & b, False, np.False_, None),
    ("&", True, False, lambda a, b: a & b, False, np.False_, None),
    ("&", True, True, lambda a, b: a & b, True, np.True_, None),
    # |
    ("|", False, False, lambda a, b: a | b, False, np.False_, None),
    ("|", False, True, lambda a, b: a | b, True, np.True_, None),
    ("|", True, False, lambda a, b: a | b, True, np.True_, None),
    ("|", True, True, lambda a, b: a | b, True, np.True_, None),
    # ^
    ("^", False, False, lambda a, b: a ^ b, False, np.False_, None),
    ("^", False, True, lambda a, b: a ^ b, True, np.True_, None),
    ("^", True, False, lambda a, b: a ^ b, True, np.True_, None),
    ("^", True, True, lambda a, b: a ^ b, False, np.False_, None),
    # <<
    ("<<", False, False, lambda a, b: a << b, 0, np.int8(0), None),
    ("<<", False, True, lambda a, b: a << b, 0, np.int8(0), None),
    ("<<", True, False, lambda a, b: a << b, 1, np.int8(1), None),
    ("<<", True, True, lambda a, b: a << b, 2, np.int8(2), None),
    # <<
    (">>", False, False, lambda a, b: a >> b, 0, np.int8(0), None),
    (">>", False, True, lambda a, b: a >> b, 0, np.int8(0), None),
    (">>", True, False, lambda a, b: a >> b, 1, np.int8(1), None),
    (">>", True, True, lambda a, b: a >> b, 0, np.int8(0), None),
]
"""List of binary operation tests. Each tuple contains in order:
    * identifier : str
        an identifier of the test,
    * operand1 : bool
        first Boolean operand
    * operand2 : bool
        second Boolean operand
    * operator :
        operator to perform on the two operands
    * bool_expected : Any
        expected results if working with bool values. If operation
        raises an Exception, the type of the exception.
    * np_bool_expected : Any
        expected results if working with np.bool_ values. If operation
        raises an Exception, the type of the Exception.
    * booleanValueExpected : Any
        expected results if working with BooleanValue values or None if
        same as np_bool_expected. If operation raises an Exception,
        the type of the Exception.
"""
binary_same_boolean_types_tests = cross_types(binary_tests)


@pytest.mark.parametrize(
    "_,type_,value1,value2,operator,b_expected,np_expected,bv_expected",
    binary_same_boolean_types_tests,
)
def test_boolean_binary_operators_same_types(
    _: str,
    type_: Type,
    value1: bool,
    value2: bool,
    operator: Callable[[BooleanTypes, BooleanTypes], BooleanTypes],
    b_expected: Union[bool, int],
    np_expected: Union[np.bool_, np.int8, Exception],
    bv_expected: Union[acvi.BooleanValue, Exception],
):
    """
    Testing of binary operators against the different Boolean types to see what bool and
    numpy.bool_ do and to see if BooleanValue is consistent with numpy.bool_.

    Parameters
    ----------
    _ : str
        An identifier of the operator testing.
    type_ : Type
        The type of Boolean to test: bool, numpy.bool or BooleanValue.
    value1 : bool
        Value of the first Boolean operand.
    value2 : bool
        Value of the second Boolean operand.
    operator : Callable[[BooleanTypes, BooleanTypes], BooleanTypes]
        Operator to perform on the two operands.
    b_expected : Any
        Expected results if working with bool values. If operation
        raises an Exception, the type of the exception.
    np_expected : Any
        Expected results if working with np.bool_ values. If operation
        raises an Exception, the type of the Exception.
    bv_expected : Any
        Expected results if working with BooleanValue values or None if
        same as np_bool_expected. If operation raises an Exception,
        the type of the Exception.
    """
    # Setup
    operand1 = type_(value1)
    operand2 = type_(value2)
    result = None
    result_ex = None
    expected: Union[
        Union[bool, int], Union[np.bool_, np.int8, Exception], Union[acvi.BooleanValue, Exception]
    ]
    if type_ is bool:
        expected = b_expected
    else:
        expected = np_expected
        if type_ is acvi.BooleanValue and bv_expected is not None:
            expected = bv_expected
    try:
        # SUT
        result = operator(operand1, operand2)
    except BaseException as ex:
        result_ex = ex

    # Verify
    # if expected is a type of exception
    if isinstance(expected, type) and issubclass(expected, BaseException):
        # Verify have no results
        assert result is None
        # Verify type of exception is same as expected
        assert isinstance(
            result_ex, expected
        ), f"type of resulting exception is {type(result)}, expected {expected}"
    else:  # else expected is a value with type
        # Verify logical value of results
        if type(expected).__module__ == np.__name__ and np.isnan(expected):
            assert np.isnan(result) == np.isnan(expected)
        else:
            assert result == expected
        # Verify type of result is same as expected
        assert isinstance(
            result, type(expected)
        ), f"type of result is {type(result)}, expected {type(expected)}"


# endregion


@pytest.mark.parametrize(
    "arg,expect_equality,expect_exception",
    [
        pytest.param(True, True, None, id="true"),
        pytest.param(False, False, None, id="false"),
        pytest.param(None, False, None, id="none"),
        pytest.param("", None, acvi.IncompatibleTypesException, id="empty-string"),
        pytest.param("something", None, acvi.IncompatibleTypesException, id="non-empty-string"),
        pytest.param(
            "false", None, acvi.IncompatibleTypesException, id="non-empty-string-says-false"
        ),
        pytest.param(acvi.IntegerValue(0), False, None, id="from IntegerValue zero"),
        pytest.param(acvi.IntegerValue(-1), True, None, id="from IntegerValue -1"),
        pytest.param(acvi.IntegerValue(1), True, None, id="from IntegerValue 1"),
        pytest.param(acvi.RealValue(0.0), False, None, id="from RealValue zero"),
        pytest.param(acvi.RealValue(-1.0), True, None, id="from RealValue -1"),
        pytest.param(acvi.RealValue(1.0), True, None, id="from RealValue 1"),
        pytest.param(acvi.StringValue("false"), False, None, id="from StringValue 'false'"),
        pytest.param(acvi.StringValue("Y"), True, None, id="from StringValue 'y'"),
        pytest.param(acvi.BooleanValue(False), False, None, id="from BooleanValue False"),
        pytest.param(acvi.BooleanValue(True), True, None, id="from BooleanValue True"),
    ],
)
def test_construct(arg: Any, expect_equality: bool, expect_exception: Type[BaseException]) -> None:
    """Verify that __init__ for BooleanValue correctly instantiates the superclass
    data."""
    with _create_exception_context(expect_exception):
        instance: acvi.BooleanValue = acvi.BooleanValue(arg)
        assert instance == expect_equality


@pytest.mark.parametrize(
    "arg,expected_result",
    [
        pytest.param("True", acvi.BooleanValue(True), id="True"),
        pytest.param("TRUE", acvi.BooleanValue(True), id="TRUE"),
        pytest.param("true", acvi.BooleanValue(True), id="true"),
        pytest.param("TrUe", acvi.BooleanValue(True), id="TrUe"),
        pytest.param("False", acvi.BooleanValue(False), id="False"),
        pytest.param("FALSE", acvi.BooleanValue(False), id="FALSE"),
        pytest.param("false", acvi.BooleanValue(False), id="false"),
        pytest.param("FaLsE", acvi.BooleanValue(False), id="FaLsE"),
        pytest.param("Yes", acvi.BooleanValue(True), id="Yes"),
        pytest.param("YES", acvi.BooleanValue(True), id="YES"),
        pytest.param("y", acvi.BooleanValue(True), id="y"),
        pytest.param("Y", acvi.BooleanValue(True), id="Y"),
        pytest.param("No", acvi.BooleanValue(False), id="No"),
        pytest.param("no", acvi.BooleanValue(False), id="no"),
        pytest.param("n", acvi.BooleanValue(False), id="n"),
        pytest.param("N", acvi.BooleanValue(False), id="N"),
        pytest.param("0", acvi.BooleanValue(False), id="zero"),
        pytest.param("0.0", acvi.BooleanValue(False), id="zero point zero"),
        pytest.param("1", acvi.BooleanValue(True), id="one point zero"),
        pytest.param("1.0", acvi.BooleanValue(True), id="one point zero"),
        pytest.param("true \r\n\t", acvi.BooleanValue(True), id="trailing whitespace true"),
        pytest.param("false \r\n\t", acvi.BooleanValue(False), id="trailing whitespace false"),
        pytest.param("\r\n\t true", acvi.BooleanValue(True), id="leading whitespace true"),
        pytest.param("\r\n\t false", acvi.BooleanValue(False), id="leading whitespace false"),
        pytest.param("NaN", acvi.BooleanValue(True), id="NaN"),
        pytest.param("Infinity", acvi.BooleanValue(True), id="infinity"),
        pytest.param("-Infinity", acvi.BooleanValue(True), id="negative infinity"),
    ],
)
def test_from_api_string_valid(arg: str, expected_result: acvi.BooleanValue) -> None:
    """
    Verify that BooleanValue.from_api_string works for valid cases.

    Parameters
    ----------
    arg : str
        The string to parse.
    expected_result : BooleanValue
        The expected result.
    """
    # Execute
    result: acvi.BooleanValue = acvi.BooleanValue.from_api_string(arg)

    assert result == expected_result


@pytest.mark.parametrize(
    "arg,expected_exception",
    [
        pytest.param("", ValueError, id="empty"),
        pytest.param(" \t\n\r", ValueError, id="all whitespace"),
        pytest.param("4,555", ValueError, id="Number with thousands separator"),
        pytest.param(None, TypeError, id="None"),
    ],
)
def test_from_api_string_invalid(arg: str, expected_exception: Type[BaseException]) -> None:
    with _create_exception_context(expected_exception):
        _: acvi.BooleanValue = acvi.BooleanValue.from_api_string(arg)


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(acvi.BooleanValue(True), "True", id="true"),
        pytest.param(acvi.BooleanValue(False), "False", id="false"),
    ],
)
def test_to_api_string(source: acvi.BooleanValue, expected_result: str) -> None:
    """
    Verify that to_api_string for BooleanValue works correctly for valid cases.

    Parameters
    ----------
    source : BooleanValue
        The original BooleanValue.
    expected_result : str
        The expected API string.
    """
    # Execute
    result: str = source.to_api_string()

    # Verify
    assert type(result) is str
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(acvi.BooleanValue(True), acvi.RealValue(1.0), id="true"),
        pytest.param(acvi.BooleanValue(False), acvi.RealValue(0.0), id="false"),
    ],
)
def test_to_real_value(source: acvi.BooleanValue, expected_result: str) -> None:
    """Verify that conversion to RealValue works correctly."""
    result: acvi.RealValue = source.to_real_value()

    # Verify
    assert type(result) is acvi.RealValue
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(acvi.BooleanValue(True), acvi.IntegerValue(1), id="true"),
        pytest.param(acvi.BooleanValue(False), acvi.IntegerValue(0), id="false"),
    ],
)
def test_to_int_value(source: acvi.BooleanValue, expected_result: str) -> None:
    """
    Verify that conversion to IntegerValue works correctly.

    Parameters
    ----------
    source : BooleanValue
        The original BooleanValue.
    expected_result : str
        The expected result of the conversion.
    """
    # Execute
    result: acvi.IntegerValue = source.to_integer_value()

    # Verify
    assert type(result) is acvi.IntegerValue
    assert result == expected_result


def test_clone() -> None:
    """Verifies that clone returns a new BooleanValue with the same value."""
    # Setup
    sut: acvi.BooleanValue = acvi.BooleanValue(True)

    # SUT
    result: acvi.BooleanValue = sut.clone()

    # Verification
    assert result is not sut
    assert np.equal(result, True)
