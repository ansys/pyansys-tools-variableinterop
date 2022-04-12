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
        import ansys.common.variableinterop.boolean_array_value as boolean_array_value
        import ansys.common.variableinterop.boolean_value as boolean_value
        import ansys.common.variableinterop.integer_array_value as integer_array_value
        import ansys.common.variableinterop.integer_value as integer_value
        import ansys.common.variableinterop.real_array_value as real_array_value
        import ansys.common.variableinterop.real_value as real_value
        import ansys.common.variableinterop.string_array_value as string_array_value
        import ansys.common.variableinterop.string_value as string_value

        class_map: Dict[VariableType, str] = {
            VariableType.STRING: string_value.StringValue.__name__,
            VariableType.REAL: real_value.RealValue.__name__,
            VariableType.INTEGER: integer_value.IntegerValue.__name__,
            VariableType.BOOLEAN: boolean_value.BooleanValue.__name__,
            VariableType.STRING_ARRAY: string_array_value.StringArrayValue.__name__,
            VariableType.REAL_ARRAY: real_array_value.RealArrayValue.__name__,
            VariableType.INTEGER_ARRAY: integer_array_value.IntegerArrayValue.__name__,
            VariableType.BOOLEAN_ARRAY: boolean_array_value.BooleanArrayValue.__name__
        }
        return class_map[self]
