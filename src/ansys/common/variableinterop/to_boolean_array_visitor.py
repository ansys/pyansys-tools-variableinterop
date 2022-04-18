"""Definition of ToBooleanArrayVisitor."""
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


class ToBooleanArrayVisitor(ivariable_visitor.
                            IVariableValueVisitor[BooleanArrayValue]):
    """Visitor pattern to call conversion methods to BooleanArrayValue"""

    def visit_integer(self, value: IntegerValue) \
            -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY)

    def visit_real(self, value: RealValue) \
            -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY)

    def visit_boolean(self, value: BooleanValue) \
            -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY)

    def visit_string(self, value: StringValue) \
            -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY)

    def visit_integer_array(self, value: IntegerArrayValue) \
            -> BooleanArrayValue:
        return value.to_boolean_array_value()

    def visit_real_array(self, value: RealArrayValue) \
            -> BooleanArrayValue:
        return value.to_boolean_array_value()

    def visit_boolean_array(self, value: BooleanArrayValue) \
            -> BooleanArrayValue:
        return np.copy(value).view(BooleanArrayValue)

    def visit_string_array(self, value: StringArrayValue) \
            -> BooleanArrayValue:
        return value.to_boolean_array_value()
