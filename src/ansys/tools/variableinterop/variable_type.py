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
"""Defines the ``VariableType`` class."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Iterable, Union

from .utils.locale_utils import Strings
from .variable_value import IVariableValue


class VariableType(Enum):
    """Provides an enumeration of the possible variable types."""

    # When editing this enumeration,
    # be sure to also update ``IVariableTypePseudoVisitor``
    # and its implementation of the pseudo-visitor pattern
    # appropriately.
    UNKNOWN = 0
    """Type is unknown."""
    INTEGER = 1
    """
    Integer values.

    These are stored as 64-bit signed integers
    """
    REAL = 2
    """
    Real values.

    These are stored as 64-bit floating point numbers
    """
    BOOLEAN = 3
    """Boolean values."""
    STRING = 4
    """String values."""
    FILE = 5
    """File values."""
    INTEGER_ARRAY = 6
    """
    Array of integer values.

    These are stored as 64-bit signed integers. Multidimensional arrays are supported.
    """
    REAL_ARRAY = 7
    """
    Array of real values.

    These are stored as 64-bit floating point numbers. Multidimensional arrays are
    supported.
    """
    BOOLEAN_ARRAY = 8
    """
    Array of Boolean values.

    Multidimensional arrays are supported.
    """
    STRING_ARRAY = 9
    """
    Array of string values.

    Multidimensional arrays are supported.
    """
    FILE_ARRAY = 10
    """
    Array of file values.

    Multidimensional arrays are supported.
    """

    @property
    def associated_type_name(self) -> str:
        """Get the name of the associated ``IVariableValue`` type."""
        from .array_values import (
            BooleanArrayValue,
            IntegerArrayValue,
            RealArrayValue,
            StringArrayValue,
        )
        from .file_array_value import FileArrayValue
        from .file_value import FileValue
        from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue

        class_map: Dict[VariableType, str] = {
            VariableType.UNKNOWN: "unknown",
            VariableType.STRING: StringValue.__name__,
            VariableType.REAL: RealValue.__name__,
            VariableType.INTEGER: IntegerValue.__name__,
            VariableType.BOOLEAN: BooleanValue.__name__,
            VariableType.FILE: FileValue.__name__,
            VariableType.STRING_ARRAY: StringArrayValue.__name__,
            VariableType.REAL_ARRAY: RealArrayValue.__name__,
            VariableType.INTEGER_ARRAY: IntegerArrayValue.__name__,
            VariableType.BOOLEAN_ARRAY: BooleanArrayValue.__name__,
            VariableType.FILE_ARRAY: FileArrayValue.__name__,
        }
        return class_map[self]

    @staticmethod
    def from_string(s: str) -> VariableType:
        """
        Get the ``VariableType`` value from a string.

        Parameters
        ----------
        s : str
            String to convert to a ``VariableType`` value.

        Returns
        -------
        VariableType
            Result.
        """

        class __IterableKeyDict(Dict[Union[Iterable, str], Any]):
            """Provides a dictionary that can initialize with iterable keys and give
            each value its own entry."""

            def __init__(self, d_: Dict[Union[Iterable, str], VariableType]):
                def __br():
                    """Break down initializer dictionary to tuple subkeys."""
                    for k, v in d_.items():
                        if isinstance(k, str):
                            yield k, v
                        else:
                            for subkey in k:
                                yield subkey, v

                super().__init__(__br())

        __valtype_strings: Dict[Union[Iterable, str], VariableType] = __IterableKeyDict(
            {
                ("int", "integer", "long"): VariableType.INTEGER,
                ("real", "double", "float"): VariableType.REAL,
                ("bool", "boolean"): VariableType.BOOLEAN,
                ("str", "string"): VariableType.STRING,
                "file": VariableType.FILE,
                ("int[]", "integer[]", "long[]"): VariableType.INTEGER_ARRAY,
                ("real[]", "double[]", "float[]"): VariableType.REAL_ARRAY,
                ("bool[]", "boolean[]"): VariableType.BOOLEAN_ARRAY,
                ("str[]", "string[]"): VariableType.STRING_ARRAY,
                "file[]": VariableType.FILE_ARRAY,
            }
        )

        try:
            return __valtype_strings[s.strip().lower()]
        except KeyError:
            return VariableType.UNKNOWN

    def to_display_string(self) -> str:
        """
        Get the display string for the ``VariableType`` value.

        Returns
        -------
        str
            Display string.
        """
        __valtype_display_string: Dict[VariableType, str] = {
            VariableType.REAL: "DISPLAY_STRING_REAL",
            VariableType.INTEGER: "DISPLAY_STRING_INTEGER",
            VariableType.BOOLEAN: "DISPLAY_STRING_BOOL",
            VariableType.STRING: "DISPLAY_STRING_STRING",
            VariableType.FILE: "DISPLAY_STRING_FILE",
            VariableType.REAL_ARRAY: "DISPLAY_STRING_REAL_ARRAY",
            VariableType.INTEGER_ARRAY: "DISPLAY_STRING_INTEGER_ARRAY",
            VariableType.BOOLEAN_ARRAY: "DISPLAY_STRING_BOOL_ARRAY",
            VariableType.STRING_ARRAY: "DISPLAY_STRING_STRING_ARRAY",
            VariableType.FILE_ARRAY: "DISPLAY_STRING_FILE_ARRAY",
            VariableType.UNKNOWN: "DISPLAY_STRING_UNKNOWN",
        }

        return Strings.get("DisplayStrings", __valtype_display_string[self])

    def get_default_value(self) -> IVariableValue:
        """
        Construct the default value for this type.

        Returns
        -------
        IVariableValue
            New value object whose type matches this type.
        """
        from .array_values import (
            BooleanArrayValue,
            IntegerArrayValue,
            RealArrayValue,
            StringArrayValue,
        )
        from .file_array_value import FileArrayValue
        from .file_value import EMPTY_FILE
        from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
        from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue

        class __DefaultValueVisitor(IVariableTypePseudoVisitor[IVariableValue]):
            """Provides the visitor that returns a default value for each type."""

            def visit_unknown(self) -> IVariableValue:
                raise TypeError

            def visit_int(self) -> IVariableValue:
                return IntegerValue(0)

            def visit_real(self) -> IVariableValue:
                return RealValue()

            def visit_boolean(self) -> IVariableValue:
                return BooleanValue()

            def visit_string(self) -> IVariableValue:
                return StringValue()

            def visit_file(self) -> IVariableValue:
                return EMPTY_FILE

            def visit_int_array(self) -> IVariableValue:
                return IntegerArrayValue()

            def visit_real_array(self) -> IVariableValue:
                return RealArrayValue()

            def visit_bool_array(self) -> IVariableValue:
                return BooleanArrayValue()

            def visit_string_array(self) -> IVariableValue:
                return StringArrayValue()

            def visit_file_array(self) -> IVariableValue:
                return FileArrayValue()

        visitor = __DefaultValueVisitor()
        return vartype_accept(visitor, self)

    from .common_variable_metadata import CommonVariableMetadata

    def construct_variable_metadata(self) -> CommonVariableMetadata:
        """
        Construct the default metadata for this type.

        Returns
        -------
        CommonVariableMetadata
            New metadata object whose type matches this type.
        """
        from .array_metadata import (
            BooleanArrayMetadata,
            IntegerArrayMetadata,
            RealArrayMetadata,
            StringArrayMetadata,
        )
        from .common_variable_metadata import CommonVariableMetadata
        from .file_array_metadata import FileArrayMetadata
        from .file_metadata import FileMetadata
        from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
        from .scalar_metadata import BooleanMetadata, IntegerMetadata, RealMetadata, StringMetadata

        class __DefaultMetadataVisitor(IVariableTypePseudoVisitor[CommonVariableMetadata]):
            """Provides the visitor that returns a default metadata for each type."""

            def visit_unknown(self) -> CommonVariableMetadata:
                raise TypeError

            def visit_int(self) -> CommonVariableMetadata:
                return IntegerMetadata()

            def visit_real(self) -> CommonVariableMetadata:
                return RealMetadata()

            def visit_boolean(self) -> CommonVariableMetadata:
                return BooleanMetadata()

            def visit_string(self) -> CommonVariableMetadata:
                return StringMetadata()

            def visit_file(self) -> CommonVariableMetadata:
                return FileMetadata()

            def visit_int_array(self) -> CommonVariableMetadata:
                return IntegerArrayMetadata()

            def visit_real_array(self) -> CommonVariableMetadata:
                return RealArrayMetadata()

            def visit_bool_array(self) -> CommonVariableMetadata:
                return BooleanArrayMetadata()

            def visit_string_array(self) -> CommonVariableMetadata:
                return StringArrayMetadata()

            def visit_file_array(self) -> CommonVariableMetadata:
                return FileArrayMetadata()

        visitor = __DefaultMetadataVisitor()
        return vartype_accept(visitor, self)
