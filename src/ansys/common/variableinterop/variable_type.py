"""Definition of VariableType."""
from enum import Enum
from typing import Dict


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
        """
        Get the name of the associated IVariableValue type.
        """
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
