from __future__ import annotations

from typing import TypeVar

import numpy as np
from numpy.typing import ArrayLike, NDArray
from overrides import overrides

import ansys.common.variableinterop.boolean_array_value as boolean_array_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.real_array_value as real_array_value
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


class StringArrayValue(NDArray[np.str_], variable_value.IVariableValue):
    """Array of string values.

    In Python StringArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.str_).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.str_)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.STRING_ARRAY

    def to_real_array_value(self) -> real_array_value.RealArrayValue:
        return self.astype(np.float64).view(real_array_value.RealArrayValue)

    def to_boolean_array_value(self) -> boolean_array_value.BooleanArrayValue:
        # TODO: use BooleanValue.to_api_string() when that is available
        def as_bool(value: str):
            normalized: str = str.lower(str.strip(value))
            if normalized in ("yes", "y", "true"):
                return np.bool_(True)
            elif normalized in ("no", "n", "false"):
                return np.bool_(False)
            else:
                # Try to parse as real then convert to boolean
                return np.bool_(np.float64(value))

        return np.vectorize(as_bool)(self).view(boolean_array_value.BooleanArrayValue)

    # TODO: full implementation

    def to_api_string(self) -> str:
        raise NotImplementedError

    @staticmethod
    def from_api_string(value: str) -> None:
        raise NotImplementedError

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
