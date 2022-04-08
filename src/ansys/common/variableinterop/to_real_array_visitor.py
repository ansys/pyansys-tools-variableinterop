from ansys.common.variableinterop.integer_value import IntegerValue
from ansys.common.variableinterop.real_value import RealValue
from ansys.common.variableinterop.boolean_value import BooleanValue
from ansys.common.variableinterop.string_value import StringValue
from ansys.common.variableinterop.integer_array_value import IntegerArrayValue
from ansys.common.variableinterop.real_array_value import RealArrayValue
from ansys.common.variableinterop.boolean_array_value import BooleanArrayValue
from ansys.common.variableinterop.string_array_value import StringArrayValue
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.exceptions import IncompatibleTypesException


class ToRealArrayVisitor(IVariableValueVisitor[RealArrayValue]):
    """Visitor pattern to call conversion methods to RealArrayValue"""

    def visit_integer(self, value: IntegerValue) -> RealArrayValue:
        raise IncompatibleTypesException(value.variable_type, VariableType.REAL_ARRAY)

    def visit_real(self, value: RealValue) -> RealArrayValue:
        raise IncompatibleTypesException(value.variable_type, VariableType.REAL_ARRAY)

    def visit_boolean(self, value: BooleanValue) -> RealArrayValue:
        raise IncompatibleTypesException(value.variable_type, VariableType.REAL_ARRAY)

    def visit_string(self, value: StringValue) -> RealArrayValue:
        raise IncompatibleTypesException(value.variable_type, VariableType.REAL_ARRAY)

    def visit_integer_array(self, value: IntegerArrayValue) -> RealArrayValue:
        return value.to_real_array_value()

    def visit_real_array(self, value: RealArrayValue) -> RealArrayValue:
        return value

    def visit_boolean_array(self, value: BooleanArrayValue) -> RealArrayValue:
        return value.to_real_array_value()

    def visit_string_array(self, value: StringArrayValue) -> RealArrayValue:
        return value.to_real_array_value()
