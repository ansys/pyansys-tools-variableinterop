from __future__ import annotations

from typing import TypeVar

import numpy as np
from numpy.typing import ArrayLike, NDArray
from overrides import overrides

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.real_array_value as real_array_value
import ansys.common.variableinterop.variable_value as variable_value

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.real_array_value as real_array_value
from .variable_type import VariableType
from .variable_value import CommonArrayValue

T = TypeVar("T")


class BooleanArrayValue(CommonArrayValue[np.bool_]):
    """Array of boolean values.

    In Python BooleanArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.bool_).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.bool_)

    def __eq__(self, other) -> bool:
        return np.array_equal(self, other)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY

    def to_real_array_value(self) -> real_array_value.RealArrayValue:
        return self.astype(np.float64).view(real_array_value.RealArrayValue)

    # TODO: full implementation

    @overrides
    def to_api_string(self) -> str:
        raise NotImplementedError

    @staticmethod
    def from_api_string(value: str) -> None:
        raise NotImplementedError

    @overrides
    def to_formatted_string(self, locale_name: str) -> str:
        raise NotImplementedError

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
