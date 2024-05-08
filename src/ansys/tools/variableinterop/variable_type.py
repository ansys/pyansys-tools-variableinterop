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
"""Defines the ``VariableType`` class."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Iterable, Optional, Type, Union

from .exceptions import IncompatibleTypesException, VariableTypeUnknownError

from .utils.locale_utils import Strings
from .variable_value import IVariableValue

def create_incompatible_types_exception(from_type: Union[VariableType, str], to_type: Union[VariableType, str]) -> IncompatibleTypesException:
    """
    Construct exception.

    Parameters
    ----------
    from_type : Union[VariableType, str]
        ``VariableType`` or string identifying the type to convert from.
    to_type : Union[VariableType, str]
        ``VariableType`` or string identifying the type to convert to.

    Returns
    -------
    Newly created ``IncompatibleTypesException``
    """
    actual_from_type: Optional[VariableType]
    actual_from_type_str: str
    actual_to_type: Optional[VariableType]
    actual_to_type_str: str

    if isinstance(from_type, VariableType):
        actual_from_type = from_type
        actual_from_type_str = from_type.associated_type_name
    else:
        actual_from_type = None
        actual_from_type_str = from_type
    if isinstance(to_type, VariableType):
        actual_to_type = to_type
        actual_to_type_str = to_type.associated_type_name
    else:
        actual_to_type = None
        actual_to_type_str = to_type
    message: str = Strings.get("Errors", "ERROR_INCOMPATIBLE_TYPES", actual_from_type_str, actual_to_type_str)
    result = IncompatibleTypesException(message)
    # Monkey patch with these attributes since due to circular dependency they can't be declared.
    result.from_type = actual_from_type
    result.from_type_str = actual_from_type_str
    result.to_type = actual_to_type
    result.to_type_str = actual_to_type_str
    return result

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
        if self == VariableType.UNKNOWN:
            return "unknown"
        return self.associated_type.__name__

    @property
    def associated_type(self) -> Type:
        """Get the associated ``IVariableValue`` type."""
        from .array_values import (
            BooleanArrayValue,
            IntegerArrayValue,
            RealArrayValue,
            StringArrayValue,
        )
        from .file_array_value import FileArrayValue
        from .file_value import FileValue
        from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue

        if self == VariableType.UNKNOWN:
            raise VariableTypeUnknownError()

        class_map: Dict[VariableType, Type] = {
            VariableType.STRING: StringValue,
            VariableType.REAL: RealValue,
            VariableType.INTEGER: IntegerValue,
            VariableType.BOOLEAN: BooleanValue,
            VariableType.FILE: FileValue,
            VariableType.STRING_ARRAY: StringArrayValue,
            VariableType.REAL_ARRAY: RealArrayValue,
            VariableType.INTEGER_ARRAY: IntegerArrayValue,
            VariableType.BOOLEAN_ARRAY: BooleanArrayValue,
            VariableType.FILE_ARRAY: FileArrayValue,
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
