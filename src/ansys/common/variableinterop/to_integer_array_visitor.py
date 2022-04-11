import numpy as np

import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.integer_array_value as integer_array_value
import ansys.common.variableinterop.real_array_value as real_array_value
import ansys.common.variableinterop.boolean_array_value as boolean_array_value
import ansys.common.variableinterop.string_array_value as string_array_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.exceptions as exceptions


class ToIntegerArrayVisitor(ivariable_visitor
                            .IVariableValueVisitor[integer_array_value.IntegerArrayValue]):
    """Visitor pattern to call conversion methods to IntegerArrayValue"""

    def visit_integer(self, value: integer_value.IntegerValue) \
            -> integer_array_value.IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_real(self, value: real_value.RealValue) \
            -> integer_array_value.IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_boolean(self, value: boolean_value.BooleanValue) \
            -> integer_array_value.IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_string(self, value: string_value.StringValue) \
            -> integer_array_value.IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_integer_array(self, value: integer_array_value.IntegerArrayValue) \
            -> integer_array_value.IntegerArrayValue:
        return np.copy(value).view(integer_array_value.IntegerArrayValue)

    def visit_real_array(self, value: real_array_value.RealArrayValue) \
            -> integer_array_value.IntegerArrayValue:
        return value.to_integer_array_value()

    def visit_boolean_array(self, value: boolean_array_value.BooleanArrayValue) \
            -> integer_array_value.IntegerArrayValue:
        return value.to_integer_array_value()

    def visit_string_array(self, value: string_array_value.StringArrayValue) \
            -> integer_array_value.IntegerArrayValue:
        return value.to_integer_array_value()
