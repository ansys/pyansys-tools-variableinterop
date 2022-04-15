import numpy as np

import ansys.common.variableinterop.boolean_array_value as boolean_array_value
import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.exceptions as exceptions
import ansys.common.variableinterop.integer_array_value as integer_array_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.real_array_value as real_array_value
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_array_value as string_array_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.variable_type as variable_type


class ToStringArrayVisitor(ivariable_visitor.
                           IVariableValueVisitor[string_array_value.StringArrayValue]):
    """Visitor pattern to call conversion methods to StringArrayValue"""

    def visit_integer(self, value: integer_value.IntegerValue) \
            -> string_array_value.StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_real(self, value: real_value.RealValue) \
            -> string_array_value.StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_boolean(self, value: boolean_value.BooleanValue) \
            -> string_array_value.StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_string(self, value: string_value.StringValue) \
            -> string_array_value.StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_integer_array(self, value: integer_array_value.IntegerArrayValue) \
            -> string_array_value.StringArrayValue:
        return value.to_string_array_value()

    def visit_real_array(self, value: real_array_value.RealArrayValue) \
            -> string_array_value.StringArrayValue:
        return value.to_string_array_value()

    def visit_boolean_array(self, value: boolean_array_value.BooleanArrayValue) \
            -> string_array_value.StringArrayValue:
        return value.to_string_array_value()

    def visit_string_array(self, value: string_array_value.StringArrayValue) \
            -> string_array_value.StringArrayValue:
        return np.copy(value).view(string_array_value.StringArrayValue)
