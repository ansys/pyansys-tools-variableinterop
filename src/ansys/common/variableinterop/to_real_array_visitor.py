"""Definition of ToRealArrayVisitor."""
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


class ToRealArrayVisitor(ivariable_visitor.IVariableValueVisitor[RealArrayValue]):
    """Visitor pattern to call conversion methods to RealArrayValue"""

    def visit_integer(self, value: IntegerValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(value.variable_type,
                                                    variable_type.VariableType.REAL_ARRAY)

    def visit_real(self, value: RealValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(value.variable_type,
                                                    variable_type.VariableType.REAL_ARRAY)

    def visit_boolean(self, value: BooleanValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(value.variable_type,
                                                    variable_type.VariableType.REAL_ARRAY)

    def visit_string(self, value: StringValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(value.variable_type,
                                                    variable_type.VariableType.REAL_ARRAY)

    def visit_integer_array(self, value: IntegerArrayValue) \
            -> RealArrayValue:
        return value.to_real_array_value()

    def visit_real_array(self, value: RealArrayValue) \
            -> RealArrayValue:
        return np.copy(value).view(RealArrayValue)

    def visit_boolean_array(self, value: BooleanArrayValue) \
            -> RealArrayValue:
        return value.to_real_array_value()

    def visit_string_array(self, value: StringArrayValue) \
            -> RealArrayValue:
        return value.to_real_array_value()
