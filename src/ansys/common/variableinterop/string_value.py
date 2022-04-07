"""Definition of StringValue."""
from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType


class StringValue(np.str_, variable_value.IVariableValue):
    """
    Wrapper around a string value.

    If you want the variable interop standard conversions, use xxxx (TODO)
    """

    # equality definition here

    # hashcode definition here

    def accept(
            self, visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        raise NotImplementedError

    def variable_type(self) -> VariableType:
        return VariableType.STRING

    def to_api_string(self) -> str:
        raise NotImplementedError

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

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
