"""Definition of VariableType."""
from __future__ import annotations

from enum import Enum
from typing import Dict

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
    INTEGER_ARRAY = 6
    """An array of integer values. These are stored as 64 bit signed integers. Multidimensional
    arrays are supported."""
    REAL_ARRAY = 7
    """An array of real values. These are stored as 64 bit floating point numbers. Multidimensional
        arrays are supported."""
    BOOLEAN_ARRAY = 8
    """An array of boolean values. Multidimensional arrays are supported."""
    STRING_ARRAY = 9
    """An array of string values. Multidimensional arrays are supported."""
    FILE_ARRAY = 10
    """An array of file values. Multidimensional arrays are supported."""

    @property
    def associated_type_name(self) -> str:
        """Get the name of the associated IVariableValue type."""
        from ansys.common.variableinterop.array_values import (
            BooleanArrayValue,
            IntegerArrayValue,
            RealArrayValue,
            StringArrayValue,
        )
        from ansys.common.variableinterop.scalar_values import (
            BooleanValue,
            IntegerValue,
            RealValue,
            StringValue,
        )

        # TODO: Update with file type names when available.
        class_map: Dict[VariableType, str] = {
            VariableType.UNKNOWN: "unknown",
            VariableType.STRING: StringValue.__name__,
            VariableType.REAL: RealValue.__name__,
            VariableType.INTEGER: IntegerValue.__name__,
            VariableType.BOOLEAN: BooleanValue.__name__,
            VariableType.FILE: "file",
            VariableType.STRING_ARRAY: StringArrayValue.__name__,
            VariableType.REAL_ARRAY: RealArrayValue.__name__,
            VariableType.INTEGER_ARRAY: IntegerArrayValue.__name__,
            VariableType.BOOLEAN_ARRAY: BooleanArrayValue.__name__,
            VariableType.FILE_ARRAY: "fileArray",
        }
        return class_map[self]

    @staticmethod
    def from_string(s: str) -> Enum:
        inp = s.strip()
        try:
            return VariableType[inp.upper()]
        except KeyError:
            inp = inp.lower().replace('_', '').replace('value', '')
            str_to_vartype_map: Dict[str, VariableType] = {
                'unknown': VariableType.UNKNOWN,
                'integer': VariableType.INTEGER,
                'real': VariableType.REAL,
                'boolean': VariableType.BOOLEAN,
                'string': VariableType.STRING,
                'file': VariableType.FILE,
                'integerarray': VariableType.INTEGER_ARRAY,
                'realarray': VariableType.REAL_ARRAY,
                'booleanarray': VariableType.BOOLEAN_ARRAY,
                'stringarray': VariableType.STRING_ARRAY,
                'filearray': VariableType.FILE_ARRAY
            }

            inp = inp.lower()
            if inp not in str_to_vartype_map.keys():
                inp = 'unknown'
            return str_to_vartype_map[inp]
            
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
        )
        from .file_array_value import FileArrayValue
        from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
        from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue

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
                # TODO: impl when file branch merged
                pass

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
        A new metadata object whose type matches this type.
        """
        from .array_metadata import (
            BooleanArrayMetadata,
            IntegerArrayMetadata,
            RealArrayMetadata,
            StringArrayMetadata,
        )
        from .common_variable_metadata import CommonVariableMetadata

        # from .file_array_metadata import FileArrayMetadata
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
                # TODO: impl when file branch merged
                pass

            def visit_int_array(self) -> CommonVariableMetadata:
                return IntegerArrayMetadata()

            def visit_real_array(self) -> CommonVariableMetadata:
                return RealArrayMetadata()

            def visit_bool_array(self) -> CommonVariableMetadata:
                return BooleanArrayMetadata()

            def visit_string_array(self) -> CommonVariableMetadata:
                return StringArrayMetadata()

            def visit_file_array(self) -> CommonVariableMetadata:
                # return FileArrayMetadata()
                pass

        visitor = __DefaultMetadataVisitor()
        return vartype_accept(visitor, self)
