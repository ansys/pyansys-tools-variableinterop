"""Definition of VariableType."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Iterable, Union

from .utils.locale_utils import Strings
from .variable_value import IVariableValue


class VariableType(Enum):
    """Enumeration listing the possible variable types."""

    # When editing this enumeration,
    # be sure to also update the IVariableTypePseudoVisitor
    # and its implementation of the pseudo-visitor pattern
    # appropriately.
    UNKNOWN = 0
    """If the type is unknown."""
    INTEGER = 1
    """Integer values. These are stored as 64 bit signed integers"""
    REAL = 2
    """Real values. These are stored as 64 bit floating point numbers"""
    BOOLEAN = 3
    """Boolean values."""
    STRING = 4
    """String values."""
    FILE = 5
    """File values."""
    STRUCT = 6
    """Struct values."""
    INTEGER_ARRAY = 7
    """An array of integer values. These are stored as 64 bit signed integers. Multidimensional
    arrays are supported."""
    REAL_ARRAY = 8
    """An array of real values. These are stored as 64 bit floating point numbers. Multidimensional
        arrays are supported."""
    BOOLEAN_ARRAY = 9
    """An array of boolean values. Multidimensional arrays are supported."""
    STRING_ARRAY = 10
    """An array of string values. Multidimensional arrays are supported."""
    FILE_ARRAY = 11
    """An array of file values. Multidimensional arrays are supported."""
    STRUCT_ARRAY = 12
    """An array of struct values. Multidimensional arrays are supported"""

    @property
    def associated_type_name(self) -> str:
        """Get the name of the associated IVariableValue type."""
        from .array_values import (
            BooleanArrayValue,
            IntegerArrayValue,
            RealArrayValue,
            StringArrayValue,
            StructArrayValue,
        )
        from .file_array_value import FileArrayValue
        from .file_value import FileValue
        from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue, StructValue

        class_map: Dict[VariableType, str] = {
            VariableType.UNKNOWN: "unknown",
            VariableType.STRING: StringValue.__name__,
            VariableType.REAL: RealValue.__name__,
            VariableType.INTEGER: IntegerValue.__name__,
            VariableType.BOOLEAN: BooleanValue.__name__,
            VariableType.FILE: FileValue.__name__,
            VariableType.STRUCT: StructValue.__name__,
            VariableType.STRING_ARRAY: StringArrayValue.__name__,
            VariableType.REAL_ARRAY: RealArrayValue.__name__,
            VariableType.INTEGER_ARRAY: IntegerArrayValue.__name__,
            VariableType.BOOLEAN_ARRAY: BooleanArrayValue.__name__,
            VariableType.FILE_ARRAY: FileArrayValue.__name__,
            VariableType.STRUCT_ARRAY: StructArrayValue.__name__,
        }
        return class_map[self]

    @staticmethod
    def from_string(s: str) -> VariableType:
        """
        Get VariableType from string.

        Parameters
        ----------
        s : str
            String to convert to a VariableType.

        Returns
        -------
        VariableType
            The result.
        """

        class __IterableKeyDict(Dict[Union[Iterable, str], Any]):
            """Dict that can initialize with iterable keys and give each value its own entry."""

            def __init__(self, d_: Dict[Union[Iterable, str], VariableType]):
                def __br():
                    """Break down initializer dict to tuple subkeys."""
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
                "struct": VariableType.STRUCT,
                ("int[]", "integer[]", "long[]"): VariableType.INTEGER_ARRAY,
                ("real[]", "double[]", "float[]"): VariableType.REAL_ARRAY,
                ("bool[]", "boolean[]"): VariableType.BOOLEAN_ARRAY,
                ("str[]", "string[]"): VariableType.STRING_ARRAY,
                "file[]": VariableType.FILE_ARRAY,
                "struct[]": VariableType.STRUCT_ARRAY,
            }
        )

        try:
            return __valtype_strings[s.strip().lower()]
        except KeyError:
            return VariableType.UNKNOWN

    def to_display_string(self) -> str:
        """
        Get the VariableType's display string.

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
            VariableType.STRUCT: "DISPLAY_STRING_STRUCT",
            VariableType.REAL_ARRAY: "DISPLAY_STRING_REAL_ARRAY",
            VariableType.INTEGER_ARRAY: "DISPLAY_STRING_INTEGER_ARRAY",
            VariableType.BOOLEAN_ARRAY: "DISPLAY_STRING_BOOL_ARRAY",
            VariableType.STRING_ARRAY: "DISPLAY_STRING_STRING_ARRAY",
            VariableType.FILE_ARRAY: "DISPLAY_STRING_FILE_ARRAY",
            VariableType.STRUCT_ARRAY: "DISPLAY_STRING_STRUCT_ARRAY",
            VariableType.UNKNOWN: "DISPLAY_STRING_UNKNOWN",
        }

        return Strings.get("DisplayStrings", __valtype_display_string[self])

    def get_default_value(self) -> IVariableValue:
        """
        Construct the default value for this type.

        Returns
        -------
        A new value object whose type matches this type.
        """
        from .array_values import (
            BooleanArrayValue,
            IntegerArrayValue,
            RealArrayValue,
            StringArrayValue,
            StructArrayValue,
        )
        from .file_array_value import FileArrayValue
        from .file_value import EMPTY_FILE
        from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
        from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue, StructValue

        class __DefaultValueVisitor(IVariableTypePseudoVisitor[IVariableValue]):
            """Visitor that returns a default value for each type."""

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

            def visit_struct(self) -> IVariableValue:
                return StructValue()

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

            def visit_struct_array(self) -> IVariableValue:
                return StructArrayValue()

        visitor = __DefaultValueVisitor()
        return vartype_accept(visitor, self)

    from .common_variable_metadata import CommonVariableMetadata

    def construct_variable_metadata(self) -> CommonVariableMetadata:
        """
        Construct the default metadata for this type.

        Returns
        -------
        A new metadata object whose type matches this type.
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
            """Visitor that returns a default metadata for each type."""

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

            def visit_struct(self) -> CommonVariableMetadata:
                raise NotImplemented

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

            def visit_struct_array(self) -> CommonVariableMetadata:
                raise NotImplemented

        visitor = __DefaultMetadataVisitor()
        return vartype_accept(visitor, self)
