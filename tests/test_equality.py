"""
Unit tests for checking equality of IVariableValues.

For most types equality handling is gained for free by extending the
numpy types, so these tests are just verifying that is working correctly.
"""

import numpy as np
import pytest

import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.variable_value as variable_value


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(real_value.RealValue(222.1), real_value.RealValue(222.1), True,
                     id="Matching Reals"),
        pytest.param(real_value.RealValue(222.323), real_value.RealValue(223.32), False,
                     id="Different Reals"),
        # Correct operation is not defined, these are given for characterization testing.
        pytest.param(real_value.RealValue(np.nan), real_value.RealValue(np.nan), False,
                     id="NaN to NaN"),
        pytest.param(real_value.RealValue(0), real_value.RealValue(np.nan), False,
                     id="Real to NaN"),
        pytest.param(real_value.RealValue(np.nan), real_value.RealValue(0), False,
                     id="NaN to Real"),
        pytest.param(real_value.RealValue(np.NINF), real_value.RealValue(np.inf), False,
                     id="-INF to INF"),
        pytest.param(real_value.RealValue(np.NINF), real_value.RealValue(np.NINF), True,
                     id="-INF to -INF"),
        pytest.param(real_value.RealValue(np.inf), real_value.RealValue(np.inf), True,
                     id="INF to INF"),
        pytest.param(real_value.RealValue(1.0),
                     real_value.RealValue(1.0 + np.finfo(np.float64).eps),
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
        pytest.param(integer_value.IntegerValue(222), integer_value.IntegerValue(222), True,
                     id="Matching Ints"),
        pytest.param(integer_value.IntegerValue(222), integer_value.IntegerValue(223), False,
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
        pytest.param(string_value.StringValue("asdf"), string_value.StringValue("asdf"), True,
                     id="Matching Strings"),
        pytest.param(string_value.StringValue("asdf"), string_value.StringValue("qwerty"), False,
                     id="Different Strings"),
        pytest.param(string_value.StringValue("asdf"), string_value.StringValue("ASDF"), False,
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
        pytest.param(boolean_value.BooleanValue(True), boolean_value.BooleanValue(True), True,
                     id="True with True"),
        pytest.param(boolean_value.BooleanValue(False), boolean_value.BooleanValue(False), True,
                     id="False with False"),
        pytest.param(boolean_value.BooleanValue(True), boolean_value.BooleanValue(False), False,
                     id="True with False"),
        pytest.param(boolean_value.BooleanValue(False), boolean_value.BooleanValue(True), False,
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
