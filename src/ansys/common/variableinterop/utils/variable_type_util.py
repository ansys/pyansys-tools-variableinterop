"""Definition of VariableType."""
from typing import Dict

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
import ansys.common.variableinterop.variable_type as variable_type


def to_type(var_type: variable_type.VariableType):
    """Get the associated IVariableValue type."""
    __class_map: Dict[variable_type.VariableType, str] = {
        variable_type.VariableType.STRING: StringValue,
        variable_type.VariableType.REAL: RealValue,
        variable_type.VariableType.INTEGER: IntegerValue,
        variable_type.VariableType.BOOLEAN: BooleanValue,
        variable_type.VariableType.STRING_ARRAY: StringArrayValue,
        variable_type.VariableType.REAL_ARRAY: RealArrayValue,
        variable_type.VariableType.INTEGER_ARRAY: IntegerArrayValue,
        variable_type.VariableType.BOOLEAN_ARRAY: BooleanArrayValue
    }
    return __class_map[var_type]


def to_type_name(var_type: variable_type.VariableType):
    """Get the name of the associated IVariableValue type."""
    return to_type(var_type).__name__
