"""Definition of VariableType."""
from enum import Enum
from typing import Dict

from ansys.common.variableinterop import variable_type
from ansys.common.variableinterop import boolean_array_value
from ansys.common.variableinterop import boolean_value
from ansys.common.variableinterop import integer_array_value
from ansys.common.variableinterop import integer_value
from ansys.common.variableinterop import real_array_value
from ansys.common.variableinterop import real_value
from ansys.common.variableinterop import string_array_value
from ansys.common.variableinterop import string_value


def to_type(var_type: variable_type.VariableType):
    """
    Get the associated IVariableValue type.
    """
    __class_map: Dict[variable_type.VariableType, str] = {
        variable_type.VariableType.STRING: string_value.StringValue,
        variable_type.VariableType.REAL: real_value.RealValue,
        variable_type.VariableType.INTEGER: integer_value.IntegerValue,
        variable_type.VariableType.BOOLEAN: boolean_value.BooleanValue,
        variable_type.VariableType.STRING_ARRAY: string_array_value.StringArrayValue,
        variable_type.VariableType.REAL_ARRAY: real_array_value.RealArrayValue,
        variable_type.VariableType.INTEGER_ARRAY: integer_array_value.IntegerArrayValue,
        variable_type.VariableType.BOOLEAN_ARRAY: boolean_array_value.BooleanArrayValue
    }
    return __class_map[var_type]


def to_type_name(var_type: variable_type.VariableType):
    """
    Get the name of the associated IVariableValue type.
    """
    return to_type(var_type).__name__
