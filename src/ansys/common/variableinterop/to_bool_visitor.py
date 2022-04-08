from ansys.common.variableinterop.boolean_value import BooleanValue
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.integer_value import IntegerValue
from ansys.common.variableinterop.real_value import RealValue
from ansys.common.variableinterop.string_value import StringValue


class ToBoolVisitor(IVariableValueVisitor[bool]):
    """
    An IVariableValueVisitor which returns a bool equivalent of the object visited
    """

    def visit_boolean(self, value: BooleanValue) -> bool:
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
        return value != 0

    def visit_real(self, value: RealValue) -> bool:
        """
        Visit a RealValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        return value != 0.0

    def visit_string(self, value: StringValue) -> bool:
        """
        Visit a StringValue
        :param value: The value being visited
        :return: A bool equivalent
        """
        _value: str = value.strip().lower()
        if _value == "true":
            return True
        elif _value == "false":
            return False
        elif _value == "yes":
            return True
        elif _value == "no":
            return False
        elif _value == "y":
            return True
        elif _value == "n":
            return False
        else:
            try:
                _f_value: float = float(_value)
                return _f_value != 0.0
            except ValueError:
                pass
            try:
                _i_value: int = int(_value)
                return _i_value != 0
            except ValueError:
                pass
            raise ValueError

# TODO: Uncomment when we have BooleanArrayValue
#   def visit_bool_array(self, value: BooleanArrayValue) -> bool:
#       """
#       Visit a BooleanArrayValue
#       :param value: The value being visited
#       :return: A bool equivalent
#       """
#       raise ValueError

# TODO: Uncomment when we have IntegerArrayValue
#   def visit_integer_array(self, value: IntegerArrayValue) -> bool:
#       """
#       Visit an IntegerArrayValue
#       :param value: The value being visited
#       :return: A bool equivalent
#       """
#       raise ValueError

# TODO: Uncomment when we have RealArrayValue
#   def visit_real_array(self, value: RealArrayValue) -> bool:
#       """
#       Visit a RealArrayValue
#       :param value: The value being visited
#       :return: A bool equivalent
#       """
#       raise ValueError

# TODO: Uncomment when we have StringArrayValue
#   def visit_string_array(self, value: StringArrayValue) -> bool:
#       """
#       Visit a StringArrayValue
#       :param value: The value being visited
#       :return: A bool equivalent
#       """
#       raise ValueError
