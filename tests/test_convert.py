"""
Unit tests for utils.convert
"""
import pytest
from test_utils import _assert_incompatible_types_exception, _create_exception_context
from typing import Type

import ansys.common.variableinterop as acvi
import ansys.common.variableinterop.utils.convert as convert


# region To Scalar Tests
@pytest.mark.skip(reason="Not implemented")
def test_to_real_value(source: acvi.IVariableValue, expected_result: acvi.RealValue):
    """
    Test behavior of convert.to_real_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    """
    # SUT
    result: acvi.RealValue = convert.to_real_value(source)

    # Verify
    assert type(result) == acvi.RealValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_value(source: acvi.IVariableValue, expected_result: acvi.IntegerValue):
    """
    Test behavior of convert.to_integer_value()

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_result
        The expected result of the test.
    """
    # SUT
    result: acvi.IntegerValue = convert.to_integer_value(source)

    # Verify
    assert type(result) == acvi.IntegerValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_value(source: acvi.IVariableValue, expected_result: acvi.BooleanValue):
    """
    Test behavior of convert.to_boolean_value()

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_result
        The expected result of the test.
    """
    # SUT
    result: acvi.BooleanValue = convert.to_boolean_value(source)

    # Verify
    assert type(result) == acvi.BooleanValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_string_value(source: acvi.IVariableValue,
                         expected_result: acvi.StringValue):
    """
    Test behavior of convert.to_string_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    """
    # SUT
    result: acvi.StringValue = convert.to_string_value(source)

    # Verify
    assert type(result) == acvi.StringValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_real_value_raises(source: acvi.IVariableValue,
                              expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_real_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_real_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.RealValue.__name__)
            raise e


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_value_raises(source: acvi.IVariableValue,
                                 expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_integer_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_integer_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.IntegerValue.__name__)
            raise e


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_value_raises(source: acvi.IVariableValue,
                                 expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_boolean_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_boolean_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.BooleanValue.__name__)
            raise e


@pytest.mark.skip(reason="Not implemented")
def test_to_string_value_raises(source: acvi.IVariableValue,
                                expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_string_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_string_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.StringValue.__name__)
            raise e


# endregion


# region To Array Tests
@pytest.mark.skip(reason="Not implemented")
def test_to_real_array_value(source: acvi.IVariableValue,
                             expected_result: acvi.RealArrayValue):
    """
    Test behavior of convert.to_real_array_value()

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_result
        The expected result of the test.
    """
    # SUT
    result: acvi.RealArrayValue = convert.to_real_array_value(source)

    # Verify
    assert type(result) == acvi.RealArrayValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_array_value(source: acvi.IVariableValue,
                                expected_result: acvi.IntegerArrayValue):
    """
    Test behavior of convert.to_integer_array_value()

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_result
        The expected result of the test.
    """
    # SUT
    result: acvi.IntegerArrayValue = convert.to_integer_array_value(source)

    # Verify
    assert type(result) == acvi.IntegerArrayValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_array_value(source: acvi.IVariableValue,
                                expected_result: acvi.BooleanArrayValue):
    """
    Test behavior of convert.to_boolean_array_value()

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_result
        The expected result of the test.
    """
    # SUT
    result: acvi.BooleanArrayValue = convert.to_boolean_array_value(source)

    # Verify
    assert type(result) == acvi.BooleanArrayValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_string_array_value(source: acvi.IVariableValue,
                               expected_result: acvi.StringArrayValue):
    """
    Test behavior of convert.to_string_array_value()

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_result
        The expected result of the test.
    """
    # SUT
    result: acvi.StringArrayValue = convert.to_string_array_value(source)

    # Verify
    assert type(result) == acvi.StringArrayValue
    assert result == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_real_array_value_raises(source: acvi.IVariableValue,
                                    expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_real_array_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_real_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.RealArrayValue.__name__)
            raise e


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_array_value_raises(source: acvi.IVariableValue,
                                       expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_integer_array_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_integer_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.IntegerArrayValue.__name__)
            raise e


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_array_value_raises(source: acvi.IVariableValue,
                                       expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_boolean_array_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_boolean_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.BooleanArrayValue.__name__)
            raise e


@pytest.mark.skip(reason="Not implemented")
def test_to_string_array_value_raises(source: acvi.IVariableValue,
                                      expected_exception: Type[BaseException]):
    """
    Test behavior of convert.to_string_array_value() when it is expected to raise an exception

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_exception
        Exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        try:
            # SUT
            _ = convert.to_string_array_value(source)
        except expected_exception as e:
            # Verify
            if expected_exception == acvi.IncompatibleTypesException:
                _assert_incompatible_types_exception(str(e),
                                                     source.__class__.__name__,
                                                     acvi.StringArrayValue.__name__)
            raise e
# endregion
