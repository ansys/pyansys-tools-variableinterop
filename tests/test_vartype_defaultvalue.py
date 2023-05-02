"""Tests for VarType.get_default_value."""
from typing import Type

import pytest
from test_utils import _create_exception_context

import ansys.tools.variableinterop as interop


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(interop.VariableType.UNKNOWN, None, TypeError, id="Unknown"),
        pytest.param(interop.VariableType.INTEGER, interop.IntegerValue(0), None, id="Integer"),
        pytest.param(interop.VariableType.REAL, interop.RealValue(), None, id="Real"),
        pytest.param(interop.VariableType.BOOLEAN, interop.BooleanValue(), None, id="Boolean"),
        pytest.param(interop.VariableType.STRING, interop.StringValue(), None, id="String"),
        # pytest.param(interop.VariableType.FILE, interop.FileValue(), None, id="File"),
        pytest.param(
            interop.VariableType.INTEGER_ARRAY,
            interop.IntegerArrayValue(),
            None,
            id="Integer Array",
        ),
        pytest.param(
            interop.VariableType.REAL_ARRAY, interop.RealArrayValue(), None, id="Real Array"
        ),
        pytest.param(
            interop.VariableType.BOOLEAN_ARRAY,
            interop.BooleanArrayValue(),
            None,
            id="Boolean Array",
        ),
        pytest.param(
            interop.VariableType.STRING_ARRAY, interop.StringArrayValue(), None, id="String Array"
        ),
        # pytest.param(interop.VariableType.FILE_ARRAY, interop.FileArrayValue(), None,
        #             id="File Array"),
    ],
)
def test_default_value(
    source: interop.VariableType,
    expect: interop.IVariableValue,
    expect_exception: Type[BaseException],
) -> None:
    """
    Verify that the correct default value is returned for each type.

    Parameters
    ----------
    source The VariableType to use.
    expect The expected result.
    expect_exception The exception to expect, or None.

    Returns
    -------
    nothing
    """
    with _create_exception_context(expect_exception):
        result: interop.IVariableValue = source.get_default_value()
        assert type(expect) == type(result)
        assert expect == result
