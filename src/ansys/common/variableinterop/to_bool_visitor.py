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


class ToBoolVisitor(ivariable_visitor.IVariableValueVisitor[bool]):
    """
    An IVariableValueVisitor which returns a bool equivalent of the object visited
    """

    def visit_boolean(self, value: boolean_value.BooleanValue) -> bool:
        """
        Visit a BooleanValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return bool(value)

    def visit_integer(self, value: integer_value.IntegerValue) -> bool:
        """
        Visit an IntegerValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return boolean_value.int64_to_bool(value)

    def visit_real(self, value: real_value.RealValue) -> bool:
        """
        Visit a RealValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return boolean_value.float_to_bool(value)

    def visit_string(self, value: string_value.StringValue) -> bool:
        """
        Visit a StringValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return boolean_value.str_to_bool(value)

    def visit_boolean_array(self, value: boolean_array_value.BooleanArrayValue) -> bool:
        """
        Visit a BooleanArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")

    def visit_integer_array(self, value: integer_array_value.IntegerArrayValue) -> bool:
        """
        Visit an IntegerArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")

    def visit_real_array(self, value: real_array_value.RealArrayValue) -> bool:
        """
        Visit a RealArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")

    def visit_string_array(self, value: string_array_value.StringArrayValue) -> bool:
        """
        Visit a StringArrayValue
        :param value: The value being visited
        :raise IncompatibleTypesException
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), "bool")
