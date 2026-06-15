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
"""Defines array metadata types."""
from overrides import overrides

from .ivariablemetadata_visitor import IVariableMetadataVisitor, T
from .numeric_metadata import NumericMetadata
from .scalar_metadata import BooleanMetadata, IntegerMetadata, RealMetadata, StringMetadata
from .variable_type import VariableType


class BooleanArrayMetadata(BooleanMetadata):
    """Provides metadata for the ``BooleanArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY

    @classmethod
    @overrides
    def from_dict(cls, data) -> "BooleanArrayMetadata":
        description, custom_metadata = super()._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata
        return result


class IntegerArrayMetadata(IntegerMetadata):
    """Provides metadata for the ``IntegerArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY

    @classmethod
    @overrides
    def from_dict(cls, data) -> "IntegerArrayMetadata":
        from . import CommonVariableMetadata, IntegerValue

        description, custom_metadata = CommonVariableMetadata._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata

        units, display_format = NumericMetadata._from_dict(data)
        result.units = units
        result.display_format = display_format

        result.lower_bound = data.get(IntegerMetadata._lower_bound_json_key)
        result.upper_bound = data.get(IntegerMetadata._upper_bound_json_key)
        result.enumerated_values = [
            IntegerValue(val) for val in data.get(IntegerMetadata._enumerated_values_json_key, [])
        ]
        result.enumerated_aliases = data.get(IntegerMetadata._enumerated_aliases_json_key, [])

        return result


class RealArrayMetadata(RealMetadata):
    """Provides metadata for the ``RealArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY

    @classmethod
    @overrides
    def from_dict(cls, data) -> "RealArrayMetadata":
        from . import CommonVariableMetadata, RealValue

        description, custom_metadata = CommonVariableMetadata._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata

        units, display_format = NumericMetadata._from_dict(data)
        result.units = units
        result.display_format = display_format

        result.lower_bound = data.get(RealMetadata._lower_bound_json_key)
        result.upper_bound = data.get(RealMetadata._upper_bound_json_key)
        result.enumerated_values = [
            RealValue(val) for val in data.get(RealMetadata._enumerated_values_json_key, [])
        ]
        result.enumerated_aliases = data.get(RealMetadata._enumerated_aliases_json_key, [])

        return result


class StringArrayMetadata(StringMetadata):
    """Provides metadata for the ``StringArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY

    @classmethod
    @overrides
    def from_dict(cls, data) -> "StringArrayMetadata":
        from . import StringValue

        description, custom_metadata = super()._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata

        result.enumerated_values = [
            StringValue(val) for val in data.get(StringMetadata._enumerated_values_json_key, [])
        ]
        result.enumerated_aliases = data.get(StringMetadata._enumerated_aliases_json_key, [])

        return result
