"""Definition of IntegerValue."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
import locale
from typing import Any, TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.locale_utils as local_utils
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


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

    def __new__(cls, arg: Any):
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
                return cls.__new__(cls, real_value.RealValue.from_api_string(arg))
            elif arg.variable_type == variable_type.VariableType.BOOLEAN:
                return super().__new__(cls, bool(arg))
            else:
                # For other IVariableValues, attempt to use the default conversions.
                return super().__new__(cls, arg)
        else:
            # For non-IVariableValues, use the superclass behavior.
            return super().__new__(cls, arg)

    # hashcode definition here

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

    def to_real_value(self) -> real_value.RealValue:
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
        return real_value.RealValue(self)

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
            return real_value.RealValue(value).to_int_value()
        else:
            # Otherwise, parse as an int.
            return IntegerValue(value)

    @overrides
    def to_formatted_string(self, locale_name: str) -> str:
        result: np.str_ = local_utils.LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%G", self))
        return result
