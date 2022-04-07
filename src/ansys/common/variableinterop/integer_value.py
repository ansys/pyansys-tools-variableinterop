"""Definition of IntegerValue."""
from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .real_value import RealValue
from .variable_type import VariableType


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

    # equality definition here

    # hashcode definition here

    def accept(
        self, visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_int(self)

    def variable_type(self) -> VariableType:
        return VariableType.INTEGER

    def to_api_string(self) -> str:
        raise NotImplementedError

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

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
