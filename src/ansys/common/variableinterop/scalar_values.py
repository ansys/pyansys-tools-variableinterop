"""Definition of all scalar value implementations of IVariableValue."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
import locale
from typing import Any, Dict, TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.exceptions as exceptions
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.utils.locale_utils as locale_utils
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
        """Convert a numpy int64 to a bool value per interchange \
        specifications."""
        return bool(val != 0)

    @staticmethod
    def int_to_bool(val: int) -> bool:
        """Convert an int to a bool value per interchange \
        specifications."""
        return bool(val != 0)

    @staticmethod
    def float_to_bool(val: float) -> bool:
        """Convert a float value to a bool per interchange \
        specifications."""
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
        """Convert a str to a bool per interchange specifications."""
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
        Construct a BooleanValue from various source types.

        Supported types include:
        None: Constructs a False BooleanValue
        bool or numpy.bool_: Constructs a BooleanValue with the given
            Boolean value.
        IVariableValue: Constructs a BooleanValue per the specification
        Others: raises an exception
        """
        self.__value: np.bool_
        if source is None:
            self.__value = np.False_
        elif isinstance(source, (bool, np.bool_)):
            self.__value = np.bool_(source)
        elif isinstance(source, variable_value.IVariableValue):
            from ansys.common.variableinterop.scalar_value_conversion import to_boolean_value
            self.__value = np.bool_(to_boolean_value(source))
        elif isinstance(
                source,
                (
                        int, np.byte, np.ubyte, np.short, np.ushort, np.intc,
                        np.uintc, np.int_, np.uint, np.longlong, np.ulonglong
                )):
            self.__value = np.bool_(source != 0)
        elif isinstance(
                source, (float, np.half, np.float16, np.single, np.double, np.longdouble)):
            self.__value = np.bool_(source != 0.0)
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

    @overrides
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

    @overrides
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

    @overrides
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

    @overrides
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

    def to_real_value(self) -> RealValue:
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
            return RealValue(1.0)
        else:
            return RealValue(0.0)

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

    def to_integer_value(self) -> IntegerValue:
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
            return IntegerValue(1)
        else:
            return IntegerValue(0)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%s", self))
        return result


class IntegerValue(np.int64, variable_value.IVariableValue):
    """
    Wrapper around an integer value.

    In Python IntegerValue is implemented by extending NumPy's int64 type. This means that
    they will decay naturally into numpy.int64 objects when using NumPy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards. For
    example, when converting from real to integer, the value will be floored instead of
    rounded. If you want the variable interop standard conversions, use the to_real_value
    function on this class to get a RealValue, which will be rounded according to the
    variable interop standards and decomposes naturally into a numpy.float64. Other conversions
    to analogous Python or NumPy types are identical between the variable interop standards
    and the default Python / NumPy behavior.
    """

    @overrides
    def __new__(cls, arg: Any = 0):
        """
        Create a new instance.

        Construction behaves differently for floating-point numbers and strings depending on
        whether the argument is an IVariableValue or not.

        IVariableValue instances are converted according to the standard interop rules.
        Reals are rounded. Values with a .5 in the tenths place are rounded away from zero.
        Strings are converted to reals, then rounded according to those rules.

        Parameters
        ----------
        arg the argument from which to construct this instance
        """

        if isinstance(arg, variable_value.IVariableValue):
            # Constructing from an IVariableValue is handled specially.
            if arg.variable_type == variable_type.VariableType.REAL:
                # For IVariableValues representing a real, use a different rounding strategy.
                return super().__new__(cls, Decimal(arg).to_integral(ROUND_HALF_UP))
            elif arg.variable_type == variable_type.VariableType.STRING:
                # For IVariableValues representing a string, convert to RealValue to use
                # the alternate rounding strategy.
                return cls.__new__(cls, RealValue.from_api_string(arg))
            else:
                # For other IVariableValues, attempt to use the default conversions.
                return super().__new__(cls, arg)
        else:
            # For non-IVariableValues, use the superclass behavior.
            return super().__new__(cls, arg)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_integer(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.INTEGER

    @overrides
    def to_api_string(self) -> str:
        return str(self)

    def to_real_value(self) -> RealValue:
        """
        Convert this IntegerValue to a RealValue.

        Note that since a RealValue is a 64-bit floating point number, it has a 52-bit mantissa.
        That means that a portion of the range of 64-bit IntegerValues cannot be completely
        accurately represented by RealValues; this conversion is sometimes lossy for IntegerValues
        of sufficient magnitude.

        Returns
        -------
        A RealValue with the same numeric value as this IntegerValue.
        """
        return RealValue(self)

    @staticmethod
    def from_api_string(value: str) -> IntegerValue:
        """
        Create an integer value from an API string.

        Leading and trailing whitespace is ignored.
        Values which can be correctly parsed as floating-point numbers
        are parsed in that manner, then rounded to integers. When rounding,
        values with a 5 in the tenths place are rounded away from zero.
        Parameters
        ----------
        value the string to parse
        Returns
        -------
        An integer value parsed from the API string.
        """
        if value is None:
            raise TypeError("Cannot create integer values from NoneType")

        # Check to see if this looks like a float.
        if any(char == "E" or char == "e" or char == "." for char in value):
            # If so, convert it according to those rules.
            return RealValue(value).to_int_value()
        else:
            # Otherwise, parse as an int.
            return IntegerValue(value)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%G", self))
        return result


class RealValue(np.float64, variable_value.IVariableValue):
    """
    Wrapper around a real value.

    In Python RealValue is implemented by extending NumPy's float64 type. This means that
    they will decay naturally into numpy.float64 objects when using NumPy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use to_int_value() to get
    an IntegerValue with variable interop standard rounding (away from zero). IntegerValue
    decomposes naturally to numpy.int64.
    """

    __CANONICAL_INF = "Infinity"
    """
    This is the canonical API string representation for infinity.

    from_api_string will accept other values provided they are
    unambiguously infinity.
    """

    __CANONICAL_NEG_INF = "-Infinity"
    """
    This is the canonical API string representation for negative infinity.

    from_api_string will accept other values provided they are
    unambiguously negative infinity.
    """

    __CANONICAL_NAN = "NaN"
    """
    This is the canonical API string representation for NaN.

    from_api_string will accept other values provided they are
    unambiguously NaN.
    """

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_real(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.REAL

    @overrides
    def to_api_string(self) -> str:
        return str(self)

    @overrides
    def __str__(self) -> str:
        if np.isnan(self):
            return RealValue.__CANONICAL_NAN
        if np.isposinf(self):
            return RealValue.__CANONICAL_INF
        if np.isneginf(self):
            return RealValue.__CANONICAL_NEG_INF
        return np.float64.__str__(self)

    @staticmethod
    def from_api_string(value: str) -> RealValue:
        """
        Convert an API string back into a value.

        Parameters
        ----------
        value
        The string to convert.
        """
        return RealValue(float(value))

    def to_int_value(self) -> IntegerValue:
        """
        Convert this RealValue to an IntegerValue.

        The conversion is performed according to the type
        interoperability specifications. The value is rounded to the
        nearest integer, where values with a 5 in the tenths place are
        always rounded away from zero. (Note that this is different
        from the "default" Python rounding behavior.)

        Returns
        -------
        An IntegerValue that is the result of rounding this value
        to the nearest integer (values with a 5 in the tenths place
        are rounded away from zero).
        """
        return IntegerValue(self)

    def to_boolean_value(self) -> BooleanValue:
        """
        Convert this RealValue to a BooleanValue.

        The conversion is performed according to the type
        interoperability specifications. Any value other than exactly 0
        is considered to be 'True'.
        Returns
        -------
        A BooleanValue that is the result of converting this RealValue.
        """
        return BooleanValue(self != 0)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%.15G", self))
        return result


class StringValue(np.str_, variable_value.IVariableValue):
    """
    Wrapper around a string value.

    In Python IntegerValue is implemented by extending NumPy's str_ type. This means that
    they will decay naturally into numpy.str_ objects when used with other types
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards. For
    example, when converting from string to integer, values parseable as a floating-point number
    are rejected instead of parsed as such and rounded.
    If you want the variable interop standard conversions, use the from_api_string method
    on any given variable interop type to get an instance of that type, which should decompose
    naturally to the analogous NumPy type.
    """

    import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_string(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.STRING

    @overrides
    def to_api_string(self) -> str:
        return str(self)

    @staticmethod
    def from_api_string(value: str) -> StringValue:
        """
        Convert an API string back to a string value.

        The string is stored exactly as specified; no escaping is performed
        as with from_formatted string.
        Parameters
        ----------
        value
        The string to convert.
        """
        if value is None:
            raise TypeError("Cannot create a StringValue from None.")

        # No conversion / escaping when coming from API string
        return StringValue(value)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        return self
