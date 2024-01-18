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
