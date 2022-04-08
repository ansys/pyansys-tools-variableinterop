from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.boolean_value import BooleanValue
from ansys.common.variableinterop.integer_value import IntegerValue
from ansys.common.variableinterop.real_value import RealValue
from ansys.common.variableinterop.string_value import StringValue


class ToBooleanVisitor(IVariableValueVisitor[BooleanValue]):
    """
    An IVariableValueVisitor which returns a BooleanValue equivalent of the object visited
    """

    def visit_boolean(self, value: BooleanValue) -> BooleanValue:
        """
        Visit a BooleanValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return BooleanValue(value)

    def visit_integer(self, value: IntegerValue) -> BooleanValue:
        """
        Visit an IntegerValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return BooleanValue(value != 0)

    def visit_real(self, value: RealValue) -> BooleanValue:
        """
        Visit a RealValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        return BooleanValue(value != 0.0)

    def visit_string(self, value: StringValue) -> BooleanValue:
        """
        Visit a StringValue
        :param value: The value being visited
        :return: A BooleanValue equivalent
        """
        _value: str = value.strip().lower()
        if _value == "true":
            return BooleanValue(True)
        elif _value == "false":
            return BooleanValue(False)
        elif _value == "yes":
            return BooleanValue(True)
        elif _value == "no":
            return BooleanValue(False)
        elif _value == "y":
            return BooleanValue(True)
        elif _value == "n":
            return BooleanValue(False)
        else:
            try:
                _f_value: float = float(_value)
                return BooleanValue(_f_value != 0.0)
            except ValueError:
                pass
            try:
                _i_value: int = int(_value)
                return BooleanValue(_i_value != 0)
            except ValueError:
                pass
            raise ValueError

# TODO: Uncomment when we have BooleanArrayValue
#   def visit_bool_array(self, value: BooleanArrayValue) -> BooleanValue:
#       """
#       Visit a BooleanArrayValue
#       :param value: The value being visited
#       :return: A BooleanValue equivalent
#       """
#       raise ValueError

# TODO: Uncomment when we have IntegerArrayValue
#   def visit_integer_array(self, value: IntegerArrayValue) -> BooleanValue:
#       """
#       Visit an IntegerArrayValue
#       :param value: The value being visited
#       :return: A BooleanValue equivalent
#       """
#       raise ValueError

# TODO: Uncomment when we have RealArrayValue
#   def visit_real_array(self, value: RealArrayValue) -> BooleanValue:
#       """
#       Visit a RealArrayValue
#       :param value: The value being visited
#       :return: A BooleanValue equivalent
#       """
#       raise ValueError

# TODO: Uncomment when we have StringArrayValue
#   def visit_string_array(self, value: StringArrayValue) -> BooleanValue:
#       """
#       Visit a StringArrayValue
#       :param value: The value being visited
#       :return: A BooleanValue equivalent
#       """
#       raise ValueError
