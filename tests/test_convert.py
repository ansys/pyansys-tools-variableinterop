"""
Unit tests for utils.convert
"""
import pytest

import ansys.common.variableinterop as acvi
import ansys.common.variableinterop.utils.convert as convert
from test_utils import _test_conversion


# region To Scalar Tests
@pytest.mark.skip(reason="Not implemented")
def test_to_real_value(source: acvi.IVariableValue,
                       expected_result: acvi.RealValue,
                       expected_exception: BaseException):
    """
    Test behavior of convert.to_real_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    expected_exception:
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_real_value,
                     acvi.RealValue)


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_value(source: acvi.IVariableValue,
                          expected_result: acvi.IntegerValue,
                          expected_exception: BaseException):
    """
    Test behavior of convert.to_integer_value()

    Parameters
    ----------
    source
        The IVariableValue to be converted.
    expected_result
        The expected result of the test.
    expected_exception
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_integer_value,
                     acvi.IntegerValue)


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_value(source: acvi.IVariableValue,
                          expected_result: acvi.BooleanValue,
                          expected_exception: BaseException):
    """
    Test behavior of convert.to_boolean_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    expected_exception:
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_boolean_value,
                     acvi.BooleanValue)


@pytest.mark.skip(reason="Not implemented")
def test_to_string_value(source: acvi.IVariableValue,
                         expected_result: acvi.StringValue,
                         expected_exception: BaseException):
    """
    Test behavior of convert.to_string_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    expected_exception:
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_string_value,
                     acvi.StringValue)
# endregion


# region To Array Tests
@pytest.mark.skip(reason="Not implemented")
def test_to_real_array_value(source: acvi.IVariableValue,
                             expected_result: acvi.RealArrayValue,
                             expected_exception: BaseException):
    """
    Test behavior of convert.to_real_array_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    expected_exception:
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_real_array_value,
                     acvi.RealArrayValue)


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_array_value(source: acvi.IVariableValue,
                                expected_result: acvi.IntegerArrayValue,
                                expected_exception: BaseException):
    """
    Test behavior of convert.to_integer_array_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    expected_exception:
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_integer_array_value,
                     acvi.IntegerArrayValue)


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_array_value(source: acvi.IVariableValue,
                                expected_result: acvi.BooleanArrayValue,
                                expected_exception: BaseException):
    """
    Test behavior of convert.to_boolean_array_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    expected_exception:
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_boolean_array_value,
                     acvi.BooleanArrayValue)


@pytest.mark.skip(reason="Not implemented")
def test_to_string_array_value(source: acvi.IVariableValue,
                               expected_result: acvi.StringArrayValue,
                               expected_exception: BaseException):
    """
    Test behavior of convert.to_string_array_value()

    Parameters
    ----------
    source:
        The IVariableValue to be converted.
    expected_result:
        The expected result of the test.
    expected_exception:
        Exception that is expected to be thrown (can be None)
    """
    _test_conversion(source, expected_result, expected_exception, convert.to_string_array_value,
                     acvi.StringArrayValue)
# endregion
