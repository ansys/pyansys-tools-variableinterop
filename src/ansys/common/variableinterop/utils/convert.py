"""
Functions to convert between different variable types.
"""

import ansys.common.variableinterop.variable_value as variable_value
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.real_array_value as real_array_value
import ansys.common.variableinterop.integer_array_value as integer_array_value
import ansys.common.variableinterop.string_array_value as string_array_value
import ansys.common.variableinterop.boolean_array_value as boolean_array_value


# region Scalars
def to_real_value(value: variable_value.IVariableValue) -> real_value.RealValue:
    raise NotImplementedError


def to_integer_value(value: variable_value.IVariableValue) -> integer_value.IntegerValue:
    raise NotImplementedError


def to_boolean_value(value: variable_value.IVariableValue) -> boolean_value.BooleanValue:
    raise NotImplementedError


def to_string_value(value: variable_value.IVariableValue) -> string_value.StringValue:
    raise NotImplementedError
# endregion


# region Arrays
def to_real_array_value(value: variable_value.IVariableValue) \
        -> real_array_value.RealArrayValue:
    raise NotImplementedError


def to_integer_array_value(value: variable_value.IVariableValue) \
        -> integer_array_value.IntegerArrayValue:
    raise NotImplementedError


def to_boolean_array_value(value: variable_value.IVariableValue) \
        -> boolean_array_value.BooleanArrayValue:
    raise NotImplementedError


def to_string_array_value(value: variable_value.IVariableValue) \
        -> string_array_value.StringArrayValue:
    raise NotImplementedError
# endregion
