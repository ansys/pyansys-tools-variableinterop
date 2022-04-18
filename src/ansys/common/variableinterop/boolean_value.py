"""Definition of BooleanValue."""
from __future__ import annotations

import locale
from typing import Dict, TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.exceptions as exceptions
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.locale_utils as locale_utils
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.to_bool_visitor as to_bool_visitor
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


class BooleanValue(variable_value.IVariableValue):
    """
    Wrapper around a boolean value.

    This type is treated by Python as if it were any other boolean type such as numpy.bool_
    or builtins.bool.
    """

    @staticmethod
    def int64_to_bool(val: np.int64) -> bool:
        """
        Convert a numpy int64 to a bool value per interchange
        specifications.
        """
        return bool(val != 0)

    @staticmethod
    def int_to_bool(val: int) -> bool:
        """
        Convert an int to a bool value per interchange specifications.
        """
        return bool(val != 0)

    @staticmethod
    def float_to_bool(val: float) -> bool:
        """
        Convert a float value to a bool per interchange specifications.
        """
        return bool(val != 0.0)

    api_str_to_bool: Dict[str, bool] = {
        'yes': True,
        'y': True,
        'true': True,
        'no': False,
        'n': False,
        'false': False
    }
    """
    A mapping of acceptable normalized values for API string conversion
    to their corresponding bool value.
    """

    @staticmethod
    def str_to_bool(val: str) -> bool:
        """
        Convert a str to a bool per interchange specifications.
        """
        _value: str = str.lower(str.strip(val))
        if _value in BooleanValue.api_str_to_bool:
            return BooleanValue.api_str_to_bool[_value]
        else:
            try:
                _f_value: float = float(_value)
                return BooleanValue.float_to_bool(_f_value)
            except ValueError:
                pass
            raise ValueError

    def __init__(self, source: object = None):
        """
        Construct a BooleanValue from various source types. Supported
        types include:
        None: Constructs a False BooleanValue
        bool or numpy.bool_: Constructs a BooleanValue with the given
            Boolean value.
        IVariableValue: Constructs a BooleanValue per the specification
        Others: raises an exception
        """
        if source is None:
            self.__value: np.bool_ = np.False_
        elif isinstance(source, (bool, np.bool_)):
            self.__value: np.bool_ = np.bool_(source)
        elif isinstance(source, variable_value.IVariableValue):
            self.__value: np.bool_ = np.bool_(source.accept(to_bool_visitor.ToBoolVisitor()))
        elif isinstance(
                source,
                (
                    int, np.byte, np.ubyte, np.short, np.ushort, np.intc,
                    np.uintc, np.int_, np.uint, np.longlong, np.ulonglong
                )):
            self.__value: np.bool_ = np.bool_(source != 0)
        elif isinstance(
                source, (float, np.half, np.float16, np.single, np.double, np.longdouble)):
            self.__value: np.bool_ = np.bool_(source != 0.0)
        else:
            raise exceptions.IncompatibleTypesException(
                type(source).__name__, variable_type.VariableType.BOOLEAN)

    def __add__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__add__(other.__value)
        else:
            return self.__value.__add__(other)

    def __and__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__and__(other.__value)
        else:
            return self.__value.__and__(other)

    def __bool__(self):
        return self.__value.__bool__()

    def __eq__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__eq__(other.__value)
        else:
            return self.__value.__eq__(other)

    def __floordiv__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__floordiv__(other.__value)
        else:
            return self.__value.__floordiv__(other)

    def __gt__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__gt__(other.__value)
        else:
            return self.__value.__gt__(other)

    def __ge__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__ge__(other.__value)
        else:
            return self.__value.__ge__(other)

    def __hash__(self):
        return self.__value.__hash__()

    def __lshift__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__lshift__(other.__value)
        else:
            return self.__value.__lshift__(other)

    def __mod__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__mod__(other.__value)
        else:
            return self.__value.__mod__(other)

    def __mul__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__mul__(other.__value)
        else:
            return self.__value.__mul__(other)

    def __ne__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__ne__(other.__value)
        else:
            return self.__value.__ne__(other)

    def __or__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__or__(other.__value)
        else:
            return self.__value.__or__(other)

    def __pow__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__pow__(other.__value)
        else:
            return self.__value.__pow__(other)

    def __rshift__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__rshift__(other.__value)
        else:
            return self.__value.__rshift__(other)

    def __str__(self):
        return self.__value.__str__()

    def __truediv__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__truediv__(other.__value)
        else:
            return self.__value.__truediv__(other)

    def __xor__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__xor__(other.__value)
        else:
            return self.__value.__xor__(other)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    @overrides
    def to_api_string(self) -> str:
        return str(self)

    def to_real_value(self) -> real_value.RealValue:
        """
        Convert a given BooleanValue to a RealValue.

        True is converted to 1.0 and False is converted to 0.0
        (Note: this is temporarily a static until we can get the
        non-numpy64-bool derived version working, since there's currently no way to actually have
        a BooleanValue instance at the moment).

        Parameters
        ----------
        orig the original BooleanValue

        Returns
        -------
        A RealValue with value representing the original BooleanValue.
        """
        if self:
            return real_value.RealValue(1.0)
        else:
            return real_value.RealValue(0.0)

    @staticmethod
    def from_api_string(value: str) -> BooleanValue:
        """
        Convert an API string back into a value.

        The conversion is performed according to the type
        interoperability specifications.

        Values which are parseable as floating-point numbers
        are parsed in that manner, then converted to boolean.

        Values which are non-numeric are checked to see if they match
        the following values for True: "true", "yes", or "y"; or the
        following values for False: "false", "no", or "n". The
        comparison is case-insensitive.

        Values not otherwise interpretable result in a ValueError.

        Parameters
        ----------
        value
        The string to convert.
        """
        return BooleanValue(BooleanValue.str_to_bool(value))

    def to_integer_value(self) -> integer_value.IntegerValue:
        """
        Convert a given BooleanValue to an IntegerValue.

        True is converted to 1 and False is converted to 0.

        Parameters
        ----------
        orig the original BooleanValue
        Returns
        -------
        A RealValue with value representing the original BooleanValue.
        """
        if self:
            return integer_value.IntegerValue(1)
        else:
            return integer_value.IntegerValue(0)

    @overrides
    def to_formatted_string(self, locale_name: str) -> str:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%s", self))
        return result
