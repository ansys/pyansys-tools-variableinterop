# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Defines visitors for translating variable types and values to/from JSON."""
from typing import Any

import numpy
from overrides import overrides

from . import (
    BooleanArrayMetadata,
    BooleanArrayValue,
    BooleanMetadata,
    BooleanValue,
    FileArrayMetadata,
    FileArrayValue,
    FileMetadata,
    FileValue,
    IntegerArrayMetadata,
    IntegerArrayValue,
    IntegerMetadata,
    IntegerValue,
    IVariableMetadataVisitor,
    IVariableTypePseudoVisitor,
    IVariableValue,
    IVariableValueVisitor,
    RealArrayMetadata,
    RealArrayValue,
    RealMetadata,
    RealValue,
    StringArrayMetadata,
    StringArrayValue,
    StringMetadata,
    StringValue,
)


class VariableValueToJsonVisitor(IVariableValueVisitor):
    """Visitor that returns a JSON serializable representation of an IVariableValue."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> Any:
        return int(value)

    @overrides
    def visit_real(self, value: RealValue) -> Any:
        return float(value)

    @overrides
    def visit_boolean(self, value: BooleanValue) -> Any:
        return bool(value)

    @overrides
    def visit_string(self, value: StringValue) -> Any:
        return str(value)

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> Any:
        return value.to_api_string()

    @overrides
    def visit_file(self, value: FileValue) -> Any:
        raise NotImplementedError  # pragma: nocover

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> Any:
        return value.to_api_string()

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> Any:
        np_list: list[numpy.bool] = value.tolist()  # here just so mpy can figure this out
        return value.to_api_string()

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> Any:
        np_list: list[numpy.str_] = value.tolist()  # here just so mpy can figure this out
        return value.to_api_string()

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> Any:
        raise NotImplementedError  # pragma: nocover


class JsonToVariableValueVisitor(IVariableMetadataVisitor[IVariableValue]):
    """Visitor that takes a JSON serializable representation of an IVariableValue and
    returns an IVariableValue with that value."""

    def __init__(self, value: Any):
        """
        Initialize the visitor.

        Parameters
        ----------
        value : Any
            The value from the JSON deserialization.
        """
        self._value = value

    @overrides
    def visit_integer(self, metadata: IntegerMetadata) -> IVariableValue:
        return IntegerValue(self._value)

    @overrides
    def visit_real(self, metadata: RealMetadata) -> IVariableValue:
        return RealValue(self._value)

    @overrides
    def visit_boolean(self, metadata: BooleanMetadata) -> IVariableValue:
        return BooleanValue(self._value)

    @overrides
    def visit_string(self, metadata: StringMetadata) -> IVariableValue:
        return StringValue(self._value)

    @overrides
    def visit_file(self, metadata: FileMetadata) -> IVariableValue:
        raise NotImplementedError  # pragma: nocover

    @overrides
    def visit_integer_array(self, metadata: IntegerArrayMetadata) -> IVariableValue:
        return IntegerArrayValue.from_api_string(self._value)

    @overrides
    def visit_real_array(self, metadata: RealArrayMetadata) -> IVariableValue:
        return RealArrayValue.from_api_string(self._value)

    @overrides
    def visit_boolean_array(self, metadata: BooleanArrayMetadata) -> IVariableValue:
        return BooleanArrayValue.from_api_string(self._value)

    @overrides
    def visit_string_array(self, metadata: StringArrayMetadata) -> IVariableValue:
        return StringArrayValue.from_api_string(self._value)

    @overrides
    def visit_file_array(self, metadata: FileArrayMetadata) -> IVariableValue:
        raise NotImplementedError  # pragma: nocover


class VariableTypeToJsonVisitor(IVariableTypePseudoVisitor[str]):
    """Visitor that returns a JSON serializable representation of an VariableType."""

    @overrides
    def visit_unknown(self) -> str:
        return "Unknown"

    @overrides
    def visit_int(self) -> str:
        return "Integer"

    @overrides
    def visit_real(self) -> str:
        return "Double"

    @overrides
    def visit_boolean(self) -> str:
        return "Boolean"

    @overrides
    def visit_string(self) -> str:
        return "String"

    @overrides
    def visit_file(self) -> str:
        return "File"

    @overrides
    def visit_int_array(self) -> str:
        return "IntegerArray"

    @overrides
    def visit_real_array(self) -> str:
        return "DoubleArray"

    @overrides
    def visit_bool_array(self) -> str:
        return "BooleanArray"

    @overrides
    def visit_string_array(self) -> str:
        return "StringArray"

    @overrides
    def visit_file_array(self) -> str:
        return "FileArray"
