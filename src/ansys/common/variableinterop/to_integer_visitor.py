"""Provides a visitor implementation that converts the visited value to a RealValue."""
from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
from ansys.common.variableinterop.exceptions import IncompatibleTypesException
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.variable_value import IVariableValue


class ToIntegerVisitor(IVariableValueVisitor[IntegerValue]):
    """This visitor implementation converts the visited value to a RealValue."""

    def visit_integer(self, value: IntegerValue) -> IntegerValue:
        return value

    def visit_real(self, value: RealValue) -> IntegerValue:
        return value.to_int_value()

    def visit_boolean(self, value: BooleanValue) -> IntegerValue:
        return value.to_integer_value()

    def visit_string(self, value: StringValue) -> IntegerValue:
        return IntegerValue.from_api_string(value.to_api_string())

    def visit_integer_array(self, value: IntegerArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.INTEGER_ARRAY, VariableType.INTEGER)

    def visit_real_array(self, value: RealArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.REAL_ARRAY, VariableType.INTEGER)

    def visit_boolean_array(self, value: BooleanArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.BOOLEAN_ARRAY, VariableType.INTEGER)

    def visit_string_array(self, value: StringArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.STRING_ARRAY, VariableType.INTEGER)


def to_integer_value(other: IVariableValue) -> IntegerValue:
    """
    Convert the given value to an IntegerValue.

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
    return other.accept(ToIntegerVisitor())
