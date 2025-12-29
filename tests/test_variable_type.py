# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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

from typing import Iterable, Tuple

import pytest

from ansys.tools.variableinterop import VariableType


@pytest.mark.parametrize(
    "inp,expected_result",
    [
        # Scalars
        pytest.param("int,integer,long", VariableType.INTEGER, id="valid INTEGER strings"),
        pytest.param("real,double,float", VariableType.REAL, id="valid REAL strings"),
        pytest.param("bool,boolean", VariableType.BOOLEAN, id="valid BOOLEAN strings"),
        pytest.param("str,string", VariableType.STRING, id="valid STRING strings"),
        pytest.param("file", VariableType.FILE, id="valid FILE strings"),
        # Arrays
        pytest.param(
            "int[],integer[],long[]", VariableType.INTEGER_ARRAY, id="valid INTEGER_ARRAY strings"
        ),
        pytest.param(
            "real[],double[],float[]", VariableType.REAL_ARRAY, id="valid REAL_ARRAY strings"
        ),
        pytest.param(
            "bool[],boolean[]", VariableType.BOOLEAN_ARRAY, id="valid BOOLEAN_ARRAY strings"
        ),
        pytest.param("str[],string[]", VariableType.STRING_ARRAY, id="valid STRING_ARRAY strings"),
        pytest.param("file[]", VariableType.FILE_ARRAY, id="valid FILE_ARRAY strings"),
        # Some unknown examples
        pytest.param("ints,unknown,garbage[]", VariableType.UNKNOWN, id="unknown"),
    ],
)
def test_var_type_from_string(inp: str, expected_result: VariableType):
    """
    Tests that VariableType.from_string() returns the correct type.

    Parameters
    ----------
    inp : str
        Input string. Can be a comma separated list to test multiple strings against the same
        expected result.
    expected_result : VariableType
        The expected resulting VariableType.
    """
    # Setup
    inputs = inp.split(",")

    # SUT
    # Store results as a tuple where [0]=the input string and [1]=the actual result of the SUT.
    results: Iterable[Tuple[str, VariableType]] = ((i, VariableType.from_string(i)) for i in inputs)

    # Verify
    for result in results:
        input_string: str = result[0]
        actual_result: VariableType = result[1]
        assert actual_result == expected_result, (
            f"\nInput string causing failure: '{input_string}'"
            f"\nExpected: {expected_result}"
            f"\nActual: {actual_result}"
        )


@pytest.mark.parametrize(
    "inp,expected_result",
    [
        pytest.param(VariableType.REAL, "Real", id="REAL"),
        pytest.param(VariableType.INTEGER, "Integer", id="INTEGER"),
        pytest.param(VariableType.BOOLEAN, "Boolean", id="BOOLEAN"),
        pytest.param(VariableType.STRING, "String", id="STRING"),
        pytest.param(VariableType.FILE, "File", id="File"),
        pytest.param(VariableType.REAL_ARRAY, "Real Array", id="REAL_ARRAY"),
        pytest.param(VariableType.INTEGER_ARRAY, "Integer Array", id="INTEGER_ARRAY"),
        pytest.param(VariableType.BOOLEAN_ARRAY, "Boolean Array", id="BOOLEAN_ARRAY"),
        pytest.param(VariableType.STRING_ARRAY, "String Array", id="STRING_ARRAY"),
        pytest.param(VariableType.FILE_ARRAY, "File Array", id="FILE_ARRAY"),
        pytest.param(VariableType.UNKNOWN, "Unknown", id="UNKNOWN"),
    ],
)
def test_var_type_to_display_string(inp: VariableType, expected_result: str):
    """
    Tests that VariableType.to_display_string() returns the correct string.

    Parameters
    ----------
    inp : VariableType
        Type to be tested.
    expected_result : str
        The expected display string.
    """
    # SUT
    result = inp.to_display_string()

    # Verify
    assert result == expected_result
