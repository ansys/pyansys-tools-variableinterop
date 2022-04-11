from __future__ import annotations

import numpy as np
from numpy.typing import NDArray, ArrayLike

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType


class RealArrayValue(NDArray[np.float64], variable_value.IVariableValue):
    """Array of real values.

    In Python RealArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.float64).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.float64)

    def __eq__(self, other: RealArrayValue) -> bool:
        return np.array_equal(self, other)

    def accept(
            self,
            visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_real_array(self)

    @property
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY

    # TODO: full implementation

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
