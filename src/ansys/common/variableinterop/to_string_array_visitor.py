"""Definition of ToStringArrayVisitor."""
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


class ToStringArrayVisitor(ivariable_visitor.
                           IVariableValueVisitor[StringArrayValue]):
    """Visitor pattern to call conversion methods to StringArrayValue"""

    def visit_integer(self, value: IntegerValue) \
            -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_real(self, value: RealValue) \
            -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_boolean(self, value: BooleanValue) \
            -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_string(self, value: StringValue) \
            -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY)

    def visit_integer_array(self, value: IntegerArrayValue) \
            -> StringArrayValue:
        return value.to_string_array_value()

    def visit_real_array(self, value: RealArrayValue) \
            -> StringArrayValue:
        return value.to_string_array_value()

    def visit_boolean_array(self, value: BooleanArrayValue) \
            -> StringArrayValue:
        return value.to_string_array_value()

    def visit_string_array(self, value: StringArrayValue) \
            -> StringArrayValue:
        return np.copy(value).view(StringArrayValue)
