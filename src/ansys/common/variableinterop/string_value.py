"""Definition of StringValue."""
from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value


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
        return visitor.visit_string(self)

    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.STRING

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
