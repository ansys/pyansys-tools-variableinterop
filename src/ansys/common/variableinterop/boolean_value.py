"""Definition of BooleanValue."""
from __future__ import annotations

import copy
from typing import Dict, TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


class BooleanValue(np.bool_, variable_value.IVariableValue):
    """
    Wrapper around a boolean value.

    If you want the variable interop standard conversions, use xxxx (TODO)
    """

    # equality definition here

    # hashcode definition here

    @overrides
    def clone(self) -> BooleanValue:
        return copy.deepcopy(self)

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

    __api_str_values: Dict[str, bool] = {
        'yes': True,
        'y': True,
        'true': True,
        'no': False,
        'n': False,
        'false': False
    }
    """
    Defines acceptable normalized values for API string conversion.
    """

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
        normalized: str = str.lower(str.strip(value))
        if (normalized in BooleanValue.__api_str_values):
            return BooleanValue(BooleanValue.__api_str_values[normalized])
        else:
            # Try to parse as real, allow exception to bubble up
            real_equiv: real_value.RealValue = real_value.RealValue.from_api_string(normalized)
            return real_equiv.to_boolean_value()

    # to_formatted_string here

    # from_formatted_string here

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
