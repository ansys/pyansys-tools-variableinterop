"""Defines the ``VariableType`` type."""
from typing import Dict, Type

from ..array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from ..scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from ..variable_type import VariableType


def to_type(var_type: VariableType):
    """Get the associated ``IVariableValue`` type."""
    __class_map: Dict[VariableType, Type] = {
        VariableType.STRING: StringValue,
        VariableType.REAL: RealValue,
        VariableType.INTEGER: IntegerValue,
        VariableType.BOOLEAN: BooleanValue,
        VariableType.STRING_ARRAY: StringArrayValue,
        VariableType.REAL_ARRAY: RealArrayValue,
        VariableType.INTEGER_ARRAY: IntegerArrayValue,
        VariableType.BOOLEAN_ARRAY: BooleanArrayValue,
    }
    return __class_map[var_type]


def to_type_name(var_type: VariableType):
    """Get the name of the associated ``IVariableValue`` type."""
    return to_type(var_type).__name__
