# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pytest

import ansys.tools.variableinterop as acvi
from test_utils import _create_exception_context


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
