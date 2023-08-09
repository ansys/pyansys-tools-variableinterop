import pytest

import ansys.tools.variableinterop as acvi


@pytest.mark.parametrize(
    "vartype,expected_result",
    [
        (acvi.VariableType.UNKNOWN, False),
        (acvi.VariableType.INTEGER, False),
        (acvi.VariableType.REAL, False),
        (acvi.VariableType.BOOLEAN, False),
        (acvi.VariableType.STRING, False),
        (acvi.VariableType.FILE, False),
        (acvi.VariableType.INTEGER_ARRAY, True),
        (acvi.VariableType.REAL_ARRAY, True),
        (acvi.VariableType.BOOLEAN_ARRAY, True),
        (acvi.VariableType.STRING_ARRAY, True),
        (acvi.VariableType.FILE_ARRAY, True),
    ],
)
def test_var_type_is_array(vartype: acvi.VariableType, expected_result: bool) -> None:
    """
    Test whether the var_type_is_array method actually works.

    Parameters
    ----------
    vartype the variable type to test
    expected_result the expected result for that variable type
    """
    # Execute
    result: bool = acvi.var_type_is_array(vartype)

    # Verify
    assert type(result) is bool
    assert result == expected_result
