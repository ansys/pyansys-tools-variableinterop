"""
Unit tests for utils.convert
"""
import pytest

import ansys.common.variableinterop as acvi
import ansys.common.variableinterop.utils.convert as convert


# region To Scalar Tests
@pytest.mark.skip(reason="Not implemented")
def test_to_real_value(source: acvi.IVariableValue, expected_result: acvi.RealValue):
    assert convert.to_real_value(source) == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_value(source: acvi.IVariableValue, expected_result: acvi.IntegerValue):
    assert convert.to_integer_value(source) == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_value(source: acvi.IVariableValue, expected_result: acvi.BooleanValue):
    assert convert.to_boolean_value(source) == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_string_value(source: acvi.IVariableValue, expected_result: acvi.StringValue):
    assert convert.to_string_value(source) == expected_result
# endregion


# region To Array Tests
@pytest.mark.skip(reason="Not implemented")
def test_to_real_array_value(source: acvi.IVariableValue,
                             expected_result: acvi.RealArrayValue):
    assert convert.to_real_array_value(source) == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_integer_array_value(source: acvi.IVariableValue,
                                expected_result: acvi.IntegerArrayValue):
    assert convert.to_integer_array_value(source) == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_boolean_array_value(source: acvi.IVariableValue,
                                expected_result: acvi.BooleanArrayValue):
    assert convert.to_boolean_array_value(source) == expected_result


@pytest.mark.skip(reason="Not implemented")
def test_to_string_array_value(source: acvi.IVariableValue,
                               expected_result: acvi.StringArrayValue):
    assert convert.to_string_array_value(source) == expected_result
# endregion
