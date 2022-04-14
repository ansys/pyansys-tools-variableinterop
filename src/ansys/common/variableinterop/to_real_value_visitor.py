"""Provides a visitor implementation that converts the visited value to a RealValue."""
from ansys.common.variableinterop.boolean_array_value import BooleanArrayValue
from ansys.common.variableinterop.boolean_value import BooleanValue
from ansys.common.variableinterop.exceptions import IncompatibleTypesException
from ansys.common.variableinterop.integer_array_value import IntegerArrayValue
from ansys.common.variableinterop.integer_value import IntegerValue
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.real_array_value import RealArrayValue
from ansys.common.variableinterop.real_value import RealValue
from ansys.common.variableinterop.string_array_value import StringArrayValue
from ansys.common.variableinterop.string_value import StringValue
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.variable_value import IVariableValue


class ToRealVisitor(IVariableValueVisitor[RealValue]):
    """This visitor implementation converts the visited value to a RealValue."""

    def visit_integer(self, value: IntegerValue) -> RealValue:
        return value.to_real_value()

    def visit_real(self, value: RealValue) -> RealValue:
        return value

    def visit_boolean(self, value: BooleanValue) -> RealValue:
        return value.to_real_value()

    def visit_string(self, value: StringValue) -> RealValue:
        return RealValue.from_api_string(value.to_api_string())

    def visit_integer_array(self, value: IntegerArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.INTEGER_ARRAY, VariableType.REAL)

    def visit_real_array(self, value: RealArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.REAL_ARRAY, VariableType.REAL)

    def visit_boolean_array(self, value: BooleanArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.BOOLEAN_ARRAY, VariableType.REAL)

    def visit_string_array(self, value: StringArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.STRING_ARRAY, VariableType.REAL)


def to_real_value(other: IVariableValue) -> RealValue:
    """
    Convert the given value to a RealValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other the other value to convert to a RealValue.

    Returns
    -------
    The value as a RealValue.

    """
    return other.accept(ToRealVisitor())
