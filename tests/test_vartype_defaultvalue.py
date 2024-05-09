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
"""Tests for VariableFactory.get_default_value."""
from typing import Type

import pytest

import ansys.tools.variableinterop as interop
from ansys.tools.variableinterop.exceptions import VariableTypeUnknownError
from ansys.tools.variableinterop.variable_factory import VariableFactory
from test_utils import _create_exception_context


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        pytest.param(interop.VariableType.UNKNOWN, None, VariableTypeUnknownError, id="Unknown"),
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
    None
    """
    with _create_exception_context(expect_exception):
        result: interop.IVariableValue = VariableFactory.get_default_value(source)
        assert type(expect) == type(result)
        assert expect == result
