from __future__ import annotations

from typing import TypeVar

import numpy as np
from numpy.typing import NDArray
from overrides import overrides

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType

T = TypeVar("T")


class StringArrayValue(NDArray[np.str_], variable_value.IVariableValue):
    """Array of string values.

    In Python StringArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)

    TODO: ndarray cannot hold string values; question as to what approach we should
          take here instead of deriving from that.
    """

    def __new__(cls, shape_):
        return super().__new__(cls, shape=shape_, dtype=np.str_)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY

    # TODO: full implementation

    @overrides
    def to_api_string(self) -> str:
        raise NotImplementedError

    @overrides
    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
