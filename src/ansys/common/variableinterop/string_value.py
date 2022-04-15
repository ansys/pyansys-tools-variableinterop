"""Definition of StringValue."""
from __future__ import annotations

from typing import TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


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

    # hashcode definition here

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
    def to_formatted_string(self, locale_name: str) -> str:
        return self
