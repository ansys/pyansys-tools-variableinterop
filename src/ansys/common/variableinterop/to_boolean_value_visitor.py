from ansys.common.variableinterop import (
    boolean_array_value, boolean_value, exceptions, integer_array_value, integer_value,
    ivariable_visitor, real_array_value, real_value, string_array_value, string_value,
    to_bool_visitor, variable_value
)


class ToBooleanValueVisitor(ivariable_visitor.IVariableValueVisitor[boolean_value.BooleanValue]):
    """
    An IVariableValueVisitor which returns a BooleanValue equivalent of the object visited
    """

    __to_bool_visitor = to_bool_visitor.ToBoolVisitor()

    def visit_boolean(self, value: boolean_value.BooleanValue) -> boolean_value.BooleanValue:
        """
        Visit a BooleanValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return boolean_value.BooleanValue(bool(value))

    def visit_integer(self, value: integer_value.IntegerValue) -> boolean_value.BooleanValue:
        """
        Visit an IntegerValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return boolean_value.BooleanValue(
            boolean_value.int64_to_bool(value))

    def visit_real(self, value: real_value.RealValue) -> boolean_value.BooleanValue:
        """
        Visit a RealValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return boolean_value.BooleanValue(
            boolean_value.float_to_bool(value))

    def visit_string(self, value: string_value.StringValue) -> boolean_value.BooleanValue:
        """
        Visit a StringValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return boolean_value.BooleanValue(
            boolean_value.str_to_bool(value))

    def visit_boolean_array(
            self, value: boolean_array_value.BooleanArrayValue) -> boolean_value.BooleanValue:
        """
        Visit a BooleanArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), variable_value.BOOLEAN)

    def visit_integer_array(
            self, value: integer_array_value.IntegerArrayValue) -> boolean_value.BooleanValue:
        """
        Visit an IntegerArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), variable_value.BOOLEAN)

    def visit_real_array(
            self, value: real_array_value.RealArrayValue) -> boolean_value.BooleanValue:
        """
        Visit a RealArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), variable_value.BOOLEAN)

    def visit_string_array(
            self, value: string_array_value.StringArrayValue) -> boolean_value.BooleanValue:
        """
        Visit a StringArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise exceptions.IncompatibleTypesException(value.variable_type(), variable_value.BOOLEAN)
