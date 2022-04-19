"""Functions to convert between different variable types."""

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
import ansys.common.variableinterop.variable_value as variable_value


# region Scalars
def to_real_value(value: variable_value.IVariableValue) -> RealValue:
    raise NotImplementedError


def to_integer_value(value: variable_value.IVariableValue) -> IntegerValue:
    raise NotImplementedError


def to_boolean_value(value: variable_value.IVariableValue) -> BooleanValue:
    raise NotImplementedError


def to_string_value(value: variable_value.IVariableValue) -> StringValue:
    raise NotImplementedError
# endregion


# region Arrays
def to_real_array_value(value: variable_value.IVariableValue) \
        -> RealArrayValue:
    raise NotImplementedError


def to_integer_array_value(value: variable_value.IVariableValue) \
        -> IntegerArrayValue:
    raise NotImplementedError


def to_boolean_array_value(value: variable_value.IVariableValue) \
        -> BooleanArrayValue:
    raise NotImplementedError


def to_string_array_value(value: variable_value.IVariableValue) \
        -> StringArrayValue:
    raise NotImplementedError
# endregion
