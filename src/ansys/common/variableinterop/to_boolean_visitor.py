import ansys.common.variableinterop.boolean_array_value as boolean_array_value
import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.integer_array_value as integer_array_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.real_array_value as real_array_value
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_array_value as string_array_value
import ansys.common.variableinterop.string_value as string_value


class ToBooleanVisitor(ivariable_visitor.IVariableValueVisitor[boolean_value.BooleanValue]):
    """
    An IVariableValueVisitor which returns a BooleanValue equivalent of the object visited
    """

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
        return boolean_value.BooleanValue(value != 0)

    def visit_real(self, value: real_value.RealValue) -> boolean_value.BooleanValue:
        """
        Visit a RealValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return boolean_value.BooleanValue(value != 0.0)

    def visit_string(self, value: string_value.StringValue) -> boolean_value.BooleanValue:
        """
        Visit a StringValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        _value: str = value.strip().lower()
        if _value == "true":
            return boolean_value.BooleanValue(True)
        elif _value == "false":
            return boolean_value.BooleanValue(False)
        elif _value == "yes":
            return boolean_value.BooleanValue(True)
        elif _value == "no":
            return boolean_value.BooleanValue(False)
        elif _value == "y":
            return boolean_value.BooleanValue(True)
        elif _value == "n":
            return boolean_value.BooleanValue(False)
        else:
            try:
                _f_value: float = float(_value)
                return boolean_value.BooleanValue(_f_value != 0.0)
            except ValueError:
                pass
            try:
                _i_value: int = int(_value)
                return boolean_value.BooleanValue(_i_value != 0)
            except ValueError:
                pass
            raise ValueError

    def visit_boolean_array(
            self, value: boolean_array_value.BooleanArrayValue) -> boolean_value.BooleanValue:
        """
        Visit a BooleanArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise ValueError

    def visit_integer_array(
            self, value: integer_array_value.IntegerArrayValue) -> boolean_value.BooleanValue:
        """
        Visit an IntegerArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise ValueError

    def visit_real_array(
            self, value: real_array_value.RealArrayValue) -> boolean_value.BooleanValue:
        """
        Visit a RealArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise ValueError

    def visit_string_array(
            self, value: string_array_value.StringArrayValue) -> boolean_value.BooleanValue:
        """
        Visit a StringArrayValue
        :param value: The value being visited
        :raise ValueError
        """
        raise ValueError
