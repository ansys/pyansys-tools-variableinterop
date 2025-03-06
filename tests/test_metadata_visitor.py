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
"""Unit tests of IVariableMetadataVisitor, and accept methods of metadata types."""

from typing import Any, TypeVar

from overrides import overrides
import pytest

import ansys.tools.variableinterop as acvi


class TestVisitor(acvi.IVariableMetadataVisitor[str]):
    """
    Implementation of IVariableValueVisitor for testing.

    Simply returns the metadata variable type when visited.
    """

    T = TypeVar("T")

    @overrides
    def visit_integer(self, metadata: acvi.IntegerMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_real(self, metadata: acvi.RealMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_boolean(self, metadata: acvi.BooleanMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_string(self, metadata: acvi.StringMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_integer_array(self, metadata: acvi.IntegerArrayMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_real_array(self, metadata: acvi.RealArrayMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_boolean_array(self, metadata: acvi.BooleanArrayMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_file(self, metadata: acvi.FileMetadata):
        return metadata.variable_type.name

    @overrides
    def visit_string_array(self, metadata: acvi.StringArrayMetadata) -> str:
        return metadata.variable_type.name

    @overrides
    def visit_file_array(self, metadata: acvi.FileArrayMetadata):
        return metadata.variable_type.name


@pytest.mark.parametrize(
    "metadata,expected",
    [
        pytest.param(acvi.RealMetadata(), "REAL", id="Real"),
        pytest.param(acvi.IntegerMetadata(), "INTEGER", id="Integer"),
        pytest.param(acvi.BooleanMetadata(), "BOOLEAN", id="Boolean"),
        pytest.param(acvi.StringMetadata(), "STRING", id="String"),
        pytest.param(acvi.FileMetadata(), "FILE", id="File"),
        pytest.param(acvi.RealArrayMetadata(), "REAL_ARRAY", id="RealArray"),
        pytest.param(acvi.IntegerArrayMetadata(), "INTEGER_ARRAY", id="IntegerArray"),
        pytest.param(acvi.BooleanArrayMetadata(), "BOOLEAN_ARRAY", id="BooleanArray"),
        pytest.param(acvi.StringArrayMetadata(), "STRING_ARRAY", id="StringArray"),
        pytest.param(acvi.FileArrayMetadata(), "FILE_ARRAY", id="FileArray"),
    ],
)
def test_visiting_a_metadata_should_work(
    metadata: acvi.CommonVariableMetadata, expected: Any
) -> None:
    """
    Verifies that the visitor pattern is working for CommonVariableMetadata.

    Parameters
    ----------
    metadata The CommonVariableMetadata to visit.
    expected The string representation of the variable type.
    """
    # Setup
    visitor = TestVisitor()

    # SUT
    result = metadata.accept(visitor)

    # Verification
    assert result == expected
