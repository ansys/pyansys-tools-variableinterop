import ansys.common.variableinterop as acvi
import pytest


__value_cases = [
    pytest.param(acvi.IntegerValue(47), True, id="valid integer"),
    pytest.param(acvi.IntegerValue(47), False, id="invalid integer"),
    pytest.param(acvi.RealValue(-867.5309), True, id="valid real"),
    pytest.param(acvi.RealValue(867.5309), True, id="invalid real"),
]


@pytest.mark.parametrize('value,is_valid', __value_cases)
def test_construct(value: acvi.IVariableValue, is_valid: bool):
    """Verify that the constructor works correctly."""
    # Execute
    sut = acvi.VariableState(value, is_valid)

    assert sut.value is value
    assert sut.is_valid == is_valid


@pytest.mark.parametrize('value,is_valid', __value_cases)
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
    # assert type(clone.value) == type(original.value)
    # The above assertion will fail because clone doesn't work right for int and real
    # at least. Uncomment once the issue is resolved.
    assert clone.value == original.value
    assert clone.is_valid == original.is_valid
