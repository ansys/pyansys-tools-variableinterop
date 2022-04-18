"""Definition of ToBoolVisitor."""
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


class ToBoolVisitor(ivariable_visitor.IVariableValueVisitor[bool]):
    """
    An IVariableValueVisitor which returns a bool equivalent of the object visited
    """

    def visit_boolean(self, value: "BooleanValue") -> bool:
        """
        Visit a BooleanValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return bool(value)

    def visit_integer(self, value: IntegerValue) -> bool:
        """
        Visit an IntegerValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return BooleanValue.int64_to_bool(value)

    def visit_real(self, value: RealValue) -> bool:
        """
        Visit a RealValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return BooleanValue.float_to_bool(value)

    def visit_string(self, value: StringValue) -> bool:
        """
        Visit a StringValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return BooleanValue.str_to_bool(value)

    def visit_boolean_array(self, value: BooleanArrayValue) -> bool:
        """
        Visit a BooleanArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")

    def visit_integer_array(self, value: IntegerArrayValue) -> bool:
        """
        Visit an IntegerArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")

    def visit_real_array(self, value: RealArrayValue) -> bool:
        """
        Visit a RealArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")

    def visit_string_array(self, value: StringArrayValue) -> bool:
        """
        Visit a StringArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")
