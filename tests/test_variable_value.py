from typing import Any

import pytest

import ansys.tools.variableinterop as acvi

__value_cases = [
    pytest.param(acvi.IntegerValue(47), True, id="valid integer"),
    pytest.param(acvi.IntegerValue(47), False, id="invalid integer"),
    pytest.param(acvi.RealValue(-867.5309), True, id="valid real"),
    pytest.param(acvi.RealValue(867.5309), True, id="invalid real"),
]

__coerce_cases = [
    pytest.param(47, acvi.IntegerValue(47), id="integer"),
    pytest.param(-867.5309, acvi.RealValue(-867.5309), id="real"),
    pytest.param(True, acvi.BooleanValue(True), id="bool"),
    pytest.param("word", acvi.StringValue("word"), id="string"),
]


@pytest.mark.parametrize("value,is_valid", __value_cases)
def test_construct(value: acvi.IVariableValue, is_valid: bool):
    """Verify that the constructor works correctly."""
    # Execute
    sut = acvi.VariableState(value, is_valid)

    assert sut.value is value
    assert sut.is_valid == is_valid


@pytest.mark.parametrize("value,is_valid", __value_cases)
def test_clone(value: acvi.IVariableValue, is_valid: bool):
    """Verify that cloning works correctly."""
    # Setup
    original = acvi.VariableState(value, is_valid)

    # Execute
    clone = original.clone()

    # Verify
    assert isinstance(clone, acvi.VariableState)
    assert clone is not original
    assert clone.value is not original.value
    assert type(clone.value) == type(original.value)
    assert clone.value == original.value
    assert clone.is_valid == original.is_valid
    assert clone == original


@pytest.mark.parametrize("value,expected_value", __coerce_cases)
def test_implicit_coerce(value: Any, expected_value: acvi.IVariableValue):
    """Verify that the constructor implicitly coerces values."""
    # Execute
    sut = acvi.VariableState(value, True)

    assert isinstance(sut.value, acvi.IVariableValue)
    assert sut.value == expected_value
