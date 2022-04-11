"""Definition of BooleanValue."""
from __future__ import annotations

from typing import TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
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
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    @overrides
    def to_api_string(self) -> str:
        raise NotImplementedError

    @overrides
    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    # to_formatted_string here

    # from_formatted_string here

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
