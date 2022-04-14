"""Definition of IntegerValue."""
from __future__ import annotations

import locale
from typing import TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.locale_utils as local_utils
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


class IntegerValue(np.int64, variable_value.IVariableValue):
    """
    Wrapper around an integer value.

    In Python IntegerValue is implemented by extending NumPy's int64 type. This means that
    they will decay naturally into numpy.int64 objects when using numpy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards. For
    example, when converting from real to integer, the value will be floored instead of
    rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

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

    def to_formatted_string(self, locale_name: str) -> str:
        result: np.str_ = local_utils.LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%G", self))
        return result

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
