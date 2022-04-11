"""Definition of IntegerValue."""
from __future__ import annotations

from typing import TypeVar

import numpy as np

import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value


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

    # equality definition here

    # hashcode definition here

    T = TypeVar("T")

    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_integer(self)

    @property
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.INTEGER

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
