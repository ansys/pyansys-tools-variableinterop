"""
Tests for the type coercion module
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple

import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import IntegerValue, IVariableValue, RealValue, implicit_coerce


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
        (0, IntegerValue(0), None),
        (1.2, RealValue(1.2), None),
        (NotConvertible(), None, TypeError),
        (None, None, TypeError)
        # TODO: Lots more cases
    ],
)
def test_coerce(source: Any, expect: IVariableValue, expect_exception: BaseException):
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
def test_coerce_real_value(source: Any, expect: IVariableValue, expect_exception: BaseException):
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
    source: Any, expect: IVariableValue, expect_exception: BaseException
):
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


def test_coerce_multiple_args():
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
