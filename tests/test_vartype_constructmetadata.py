"""Tests for VarType.get_default_value."""
from typing import Type

import pytest
from test_utils import _create_exception_context

import ansys.common.variableinterop as interop


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(interop.VariableType.UNKNOWN, None, TypeError, id="Unknown"),
        pytest.param(interop.VariableType.INTEGER, interop.IntegerMetadata(), None, id="Integer"),
        pytest.param(interop.VariableType.REAL, interop.RealMetadata(), None, id="Real"),
        pytest.param(interop.VariableType.BOOLEAN, interop.BooleanMetadata(), None, id="Boolean"),
        pytest.param(interop.VariableType.STRING, interop.StringMetadata(), None, id="String"),
        # pytest.param(interop.VariableType.FILE, interop.FileMetadata(), None, id="File"),
        pytest.param(
            interop.VariableType.INTEGER_ARRAY,
            interop.IntegerArrayMetadata(),
            None,
            id="Integer Array",
        ),
        pytest.param(
            interop.VariableType.REAL_ARRAY, interop.RealArrayMetadata(), None, id="Real Array"
        ),
        pytest.param(
            interop.VariableType.BOOLEAN_ARRAY,
            interop.BooleanArrayMetadata(),
            None,
            id="Boolean Array",
        ),
        pytest.param(
            interop.VariableType.STRING_ARRAY,
            interop.StringArrayMetadata(),
            None,
            id="String Array",
        ),
        # pytest.param(interop.VariableType.FILE_ARRAY, interop.FileArrayMetadata(), None,
        #             id="File Array"),
    ],
)
def test_construct_variable_metadata(
    source: interop.VariableType,
    expect: interop.CommonVariableMetadata,
    expect_exception: Type[BaseException],
) -> None:
    """
    Verify that the correct metadata is returned for each type.

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
        result: interop.CommonVariableMetadata = source.construct_variable_metadata()
        assert type(expect) == type(result)
        assert expect == result
