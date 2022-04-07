from src.ansys.common.variableinterop import IVariableValueVisitor, BooleanValue, boolean_value, \
    integer_value, real_value, string_value


class ToBooleanVisitor(IVariableValueVisitor[BooleanValue]):
    """

    """

    def visit_boolean(self, value: boolean_value.BooleanValue) -> BooleanValue:
        pass

    def visit_integer(self, value: integer_value.IntegerValue) -> BooleanValue:
        return BooleanValue(value != 0)

    def visit_real(self, value: real_value.RealValue) -> BooleanValue:
        return BooleanValue(value != 0.0)

    def visit_string(self, value: string_value.StringValue) -> BooleanValue:
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

    # visit_bool_array
    # visit_integer_array
    # visit_real_array
    # visit_string_array
