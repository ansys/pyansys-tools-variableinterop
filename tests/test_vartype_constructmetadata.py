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
"""Tests for VariableFactory.construct_variable_metadata."""
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
    None
    """
    with _create_exception_context(expect_exception):
        result: interop.CommonVariableMetadata = VariableFactory.construct_variable_metadata(source)
        assert type(expect) == type(result)
        assert expect == result
