"""
Unit tests for checking equality of IVariableValues.

For most types equality handling is gained for free by extending the
numpy types, so these tests are just verifying that is working correctly.
"""

import numpy as np
import pytest

from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
import ansys.common.variableinterop.variable_value as variable_value


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(RealValue(222.1), RealValue(222.1), True,
                     id="Matching Reals"),
        pytest.param(RealValue(222.323), RealValue(223.32), False,
                     id="Different Reals"),
        # Correct operation is not defined, these are given for characterization testing.
        pytest.param(RealValue(np.nan), RealValue(np.nan), False,
                     id="NaN to NaN"),
        pytest.param(RealValue(0), RealValue(np.nan), False,
                     id="Real to NaN"),
        pytest.param(RealValue(np.nan), RealValue(0), False,
                     id="NaN to Real"),
        pytest.param(RealValue(np.NINF), RealValue(np.inf), False,
                     id="-INF to INF"),
        pytest.param(RealValue(np.NINF), RealValue(np.NINF), True,
                     id="-INF to -INF"),
        pytest.param(RealValue(np.inf), RealValue(np.inf), True,
                     id="INF to INF"),
        pytest.param(RealValue(1.0),
                     RealValue(1.0 + np.finfo(np.float64).eps),
                     False,
                     id="Real to Real plus Epsilon")
    ]
)
def test_equality_of_real_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for RealValue.

    Parameters
    ----------
    lhs Left-hand of the equality operation.
    rhs Right-hand of the equality operation.
    expected The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(IntegerValue(222), IntegerValue(222), True,
                     id="Matching Ints"),
        pytest.param(IntegerValue(222), IntegerValue(223), False,
                     id="Different Ints"),
    ]
)
def test_equality_of_integer_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for IntegerValue.

    Parameters
    ----------
    lhs Left-hand of the equality operation.
    rhs Right-hand of the equality operation.
    expected The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(StringValue("asdf"), StringValue("asdf"), True,
                     id="Matching Strings"),
        pytest.param(StringValue("asdf"), StringValue("qwerty"), False,
                     id="Different Strings"),
        pytest.param(StringValue("asdf"), StringValue("ASDF"), False,
                     id="Different Case"),
    ]
)
def test_equality_of_string_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for StringValue.

    Parameters
    ----------
    lhs Left-hand of the equality operation.
    rhs Right-hand of the equality operation.
    expected The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(BooleanValue(True), BooleanValue(True), True,
                     id="True with True"),
        pytest.param(BooleanValue(False), BooleanValue(False), True,
                     id="False with False"),
        pytest.param(BooleanValue(True), BooleanValue(False), False,
                     id="True with False"),
        pytest.param(BooleanValue(False), BooleanValue(True), False,
                     id="False with True"),
    ]
)
def test_equality_of_boolean_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for BooleanValue.

    Parameters
    ----------
    lhs Left-hand of the equality operation.
    rhs Right-hand of the equality operation.
    expected The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected
