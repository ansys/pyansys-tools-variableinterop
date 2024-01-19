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

from contextlib import contextmanager
from typing import Optional, Type

import pytest

import ansys.tools.variableinterop as acvi


@contextmanager
def _dummy_context():
    """A dummy context that does nothing so we can always use a with statement, even if
    one isn't needed."""
    yield None


def _create_exception_context(expect_exception: Optional[Type[BaseException]]):
    """
    Creates an object to use in a with block that will test for expect_exception to be
    thrown, or does nothing if expect_exception is None.

    Parameters
    ----------
    expect_exception : Type[BaseException]
        The exception to expect, or None for not expecting an exception.

    Returns
    -------
    Optional[Type[BaseException]]
        A context to use in a with block that will validate the expected exception.
    """
    if expect_exception is not None:
        return pytest.raises(expect_exception)
    else:
        return _dummy_context()


def _test_to_value_visitor(
    value: acvi.IVariableValue,
    expected_result: acvi.IVariableValue,
    expected_exception_type: Type[BaseException],
    visitor_type: Type[acvi.IVariableValueVisitor],
    result_type: Type[acvi.IVariableValue] = None,
) -> None:
    """
    General helper function to test ``To__type__Visitor`` classes.

    Parameters
    ----------
    value : acvi.IVariableValue
        The value to be converted.
    expected_result : acvi.IVariableValue
        The expected result of calling 'accept()' (can be None).
    expected_exception_type : Type[BaseException]
        The type of exception that is expected (can be None).
    visitor_type : Type[acvi.IVariableValueVisitor]
        The type of visitor to use.
    result_type : Type[acvi.IVariableValue]
        The type of the expected result (optional, can be derived from expected_result
        if it is not None).
    """
    if result_type is None:
        result_type = type(expected_result)
    with _create_exception_context(expected_exception_type):
        instance = visitor_type()
        try:
            # SUT
            result: acvi.IVariableValue = value.accept(instance)

            # Verify (no exception)
            assert type(result) == type(expected_result)
            assert result == expected_result

        except expected_exception_type as e:
            # Verify (expected exception)
            if expected_exception_type == acvi.IncompatibleTypesException:
                assert str(e) == (
                    "Error: Cannot convert from type {0} to type {1}.\n"
                    "Reason: The types are incompatible."
                ).format(value.__class__.__name__, result_type.__name__)
            raise e


def _assert_incompatible_types_exception(message: str, from_: str, to: str) -> None:
    """
    Helper function to assert IncompatibleTypesException gave the expected message.

    Parameters
    ----------
    message : str
        Expected error message.
    from_ : str
        Type of the source value.
    to : str
        Type to which the test was trying to convert source.
    """
    assert message == (
        "Error: Cannot convert from type {0} to type {1}.\n" "Reason: The types are incompatible."
    ).format(from_, to)
