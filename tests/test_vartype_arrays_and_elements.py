import pytest
from test_utils import _create_exception_context

import ansys.common.variableinterop as acvi


@pytest.mark.parametrize(
    "vartype,expected_result",
    [
        (acvi.VariableType.REAL, acvi.VariableType.REAL_ARRAY),
        (acvi.VariableType.INTEGER, acvi.VariableType.INTEGER_ARRAY),
        (acvi.VariableType.BOOLEAN, acvi.VariableType.BOOLEAN_ARRAY),
        (acvi.VariableType.STRING, acvi.VariableType.STRING_ARRAY),
        (acvi.VariableType.FILE, acvi.VariableType.FILE_ARRAY),
    ],
)
def test_to_array_type(vartype: acvi.VariableType, expected_result: acvi.VariableType) -> None:
    """
    Verify that to_array_type works correctly for valid cases.

    Parameters
    ----------
    vartype the variable type to submit
    expected_result the expected result

    """
    # Execute
    result: acvi.VariableType = acvi.to_array_type(vartype)

    # Verify
    assert type(result) is acvi.VariableType
    assert result == expected_result


@pytest.mark.parametrize(
    "vartype",
    [
        acvi.VariableType.REAL_ARRAY,
        acvi.VariableType.INTEGER_ARRAY,
        acvi.VariableType.BOOLEAN_ARRAY,
        acvi.VariableType.STRING_ARRAY,
        acvi.VariableType.FILE_ARRAY,
        acvi.VariableType.UNKNOWN,
    ],
)
def test_to_array_type_invalid(vartype: acvi.VariableType) -> None:
    """
    Verify that to_array_type works correctly for invalid cases.

    Parameters
    ----------
    vartype the variable type to submit
    expected_exception the expected exception

    """
    with _create_exception_context(ValueError):
        acvi.to_array_type(vartype)


@pytest.mark.parametrize(
    "vartype,expected_result",
    [
        (acvi.VariableType.REAL_ARRAY, acvi.VariableType.REAL),
        (acvi.VariableType.INTEGER_ARRAY, acvi.VariableType.INTEGER),
        (acvi.VariableType.BOOLEAN_ARRAY, acvi.VariableType.BOOLEAN),
        (acvi.VariableType.STRING_ARRAY, acvi.VariableType.STRING),
        (acvi.VariableType.FILE_ARRAY, acvi.VariableType.FILE),
    ],
)
def test_get_element_type(vartype: acvi.VariableType, expected_result: acvi.VariableType) -> None:
    """
    Verify that get_element_type works correctly for valid cases.

    Parameters
    ----------
    vartype the variable type to submit
    expected_result the expected result

    """
    # Execute
    result: acvi.VariableType = acvi.get_element_type(vartype)

    # Verify
    assert type(result) is acvi.VariableType
    assert result == expected_result


@pytest.mark.parametrize(
    "vartype",
    [
        acvi.VariableType.REAL,
        acvi.VariableType.INTEGER,
        acvi.VariableType.BOOLEAN,
        acvi.VariableType.STRING,
        acvi.VariableType.FILE,
        acvi.VariableType.UNKNOWN,
    ],
)
def test_get_element_type_invalid(vartype: acvi.VariableType) -> None:
    """
    Verify that get_element_type works correctly for invalid cases.

    Parameters
    ----------
    vartype the variable type to submit
    expected_exception the expected exception

    """
    with _create_exception_context(ValueError):
        acvi.get_element_type(vartype)
