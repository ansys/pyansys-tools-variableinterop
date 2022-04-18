"""Definition of ToIntegerArrayVisitor."""
import numpy as np

from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
import ansys.common.variableinterop.exceptions as exceptions
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
import ansys.common.variableinterop.variable_type as variable_type


class ToIntegerArrayVisitor(ivariable_visitor
                            .IVariableValueVisitor[IntegerArrayValue]):
    """Visitor pattern to call conversion methods to IntegerArrayValue"""

    def visit_integer(self, value: IntegerValue) \
            -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_real(self, value: RealValue) \
            -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_boolean(self, value: BooleanValue) \
            -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_string(self, value: StringValue) \
            -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY)

    def visit_integer_array(self, value: IntegerArrayValue) \
            -> IntegerArrayValue:
        return np.copy(value).view(IntegerArrayValue)

    def visit_real_array(self, value: RealArrayValue) \
            -> IntegerArrayValue:
        return value.to_integer_array_value()

    def visit_boolean_array(self, value: BooleanArrayValue) \
            -> IntegerArrayValue:
        return value.to_integer_array_value()

    def visit_string_array(self, value: StringArrayValue) \
            -> IntegerArrayValue:
        return value.to_integer_array_value()
