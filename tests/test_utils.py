from contextlib import contextmanager
from typing import Type

import pytest

import ansys.common.variableinterop as acvi

# TODO: search google, is there a standard way to do this?


@contextmanager
def _dummy_context():
    """
    A dummy context that does nothing so we can always use a with
    statement, even if one isn't needed.
    """
    yield None


def _create_exception_context(expect_exception: Type[BaseException]):
    """
    Creates an object to use in a with block that will test for expect_exception
    to be thrown, or does nothing if expect_exception is None.

    Parameters
    ----------
    expect_exception : Type[BaseException]
        The exception to expect, or None for not expecting an exception.

    Returns
    -------
    A context to use in a with block that will validate the expected exception.
    """
    if expect_exception is not None:
        return pytest.raises(expect_exception)
    else:
        return _dummy_context()


def _test_to_value_visitor(value: acvi.IVariableValue,
                           expected_result: acvi.IVariableValue,
                           expected_exception_type: Type[BaseException],
                           visitor_type: Type[acvi.IVariableValueVisitor],
                           result_type: Type[acvi.IVariableValue] = None) -> None:
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
                assert e.message == \
                       ("Error: Cannot convert from type {0} to type {1}.\n"
                        "Reason: The types are incompatible.") \
                       .format(value.__class__.__name__, result_type.__name__)
            raise e


def _assert_incompatible_types_exception(message: str,
                                         from_: str,
                                         to: str) -> None:
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
    assert message == \
           ("Error: Cannot convert from type {0} to type {1}.\n"
            "Reason: The types are incompatible.") \
           .format(from_, to)
