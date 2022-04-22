"""
Unit tests for checking equality of IVariableValues.

For most types equality handling is gained for free by extending the
numpy types, so these tests are just verifying that is working correctly.
"""
from pathlib import Path
from uuid import UUID

import numpy as np
import pytest
from test_file_value import _TestFileValue

from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
from ansys.common.variableinterop.file_array_value import FileArrayValue
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
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
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
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
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
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
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
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(_TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                     _TestFileValue(Path("d"), "e", "f", UUID(int=1)),
                     True, id="Same id"),
        pytest.param(_TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                     _TestFileValue(Path("d"), "e", "f", UUID(int=2)),
                     False, id="Different ids"),
    ]
)
def test_equality_of_file_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for FileValue.

    Parameters
    ----------
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(RealArrayValue(values=[1.1, 2.2, 3.3]), RealArrayValue(values=[1.1, 2.2, 3.3]),
                     True, id="Matching Reals"),
        pytest.param(RealArrayValue(values=[1.1, 2.2, 3.3]), RealArrayValue(values=[1.1, 9.9, 3.3]),
                     False, id="Different Reals"),
    ]
)
def test_equality_of_real_array_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for RealArrayValue.

    Parameters
    ----------
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(IntegerArrayValue(values=[1, 2, 3]), IntegerArrayValue(values=[1, 2, 3]),
                     True, id="Matching Ints"),
        pytest.param(IntegerArrayValue(values=[1, 2, 3]), IntegerArrayValue(values=[1, 2, 4]),
                     False, id="Different Ints"),
    ]
)
def test_equality_of_integer_array_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for IntegerArrayValue.

    Parameters
    ----------
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(StringArrayValue(values=['a', 'b', 'c']),
                     StringArrayValue(values=['a', 'b', 'c']),
                     True, id="Matching Strings"),
        pytest.param(StringArrayValue(values=['a', 'b', 'c']),
                     StringArrayValue(values=['a', 'b', 'd']),
                     False, id="Different Strings"),
    ]
)
def test_equality_of_string_array_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for StringArrayValue.

    Parameters
    ----------
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(BooleanArrayValue(values=[True, False, True]),
                     BooleanArrayValue(values=[True, False, True]),
                     True, id="Matching Bools"),
        pytest.param(BooleanArrayValue(values=[True, False, True]),
                     BooleanArrayValue(values=[False, False, True]),
                     False, id="Different Bools"),
    ]
)
def test_equality_of_boolean_array_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for BooleanArrayValue.

    Parameters
    ----------
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "lhs,rhs,expected",
    [
        pytest.param(FileArrayValue(values=[
                        _TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                        _TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                     ]),
                     FileArrayValue(values=[
                         _TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                         _TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                     ]),
                     True, id="Same Files"),
        pytest.param(FileArrayValue(values=[
                        _TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                        _TestFileValue(Path("a"), "b", "c", UUID(int=1))
                    ]),
                    FileArrayValue(values=[
                        _TestFileValue(Path("a"), "b", "c", UUID(int=1)),
                        _TestFileValue(Path("a"), "b", "c", UUID(int=2))
                    ]),
                    False, id="Different Different"),
    ]
)
def test_equality_of_file_array_values(
        lhs: variable_value.IVariableValue,
        rhs: variable_value.IVariableValue,
        expected: bool) -> None:
    """
    Equality tests for FileArrayValue.

    Parameters
    ----------
    lhs : IVariableValue
        Left-hand of the equality operation.
    rhs : IVariableValue
        Right-hand of the equality operation.
    expected : bool
        The expected result of equality check.
    """
    # SUT
    result: bool = lhs == rhs

    # Verification
    assert result == expected
