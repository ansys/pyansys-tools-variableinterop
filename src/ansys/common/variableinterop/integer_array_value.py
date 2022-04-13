from __future__ import annotations

from typing import TypeVar

import numpy as np
from numpy.typing import ArrayLike, NDArray
from overrides import overrides

from ansys.common.variableinterop.array_to_from_string_util import ArrayToFromStringUtil
import ansys.common.variableinterop.boolean_array_value as boolean_array_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.real_array_value as real_array_value
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


class IntegerArrayValue(NDArray[np.int64], variable_value.IVariableValue):
    """Array of integer values.

    In Python IntegerArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.int64).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.int64)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.INTEGER_ARRAY

    def to_boolean_array_value(self):
        return np.vectorize(np.bool_)(self).view(boolean_array_value.BooleanArrayValue)

    def to_real_array_value(self) -> real_array_value.RealArrayValue:
        return self.astype(np.float64).view(real_array_value.RealArrayValue)

    # TODO: full implementation

    @overrides
    def to_api_string(self) -> str:
        raise NotImplementedError

    @staticmethod
    def from_api_string(value: str) -> None:
        raise NotImplementedError

    # TODO: overrides when right branch merged over
    def to_formatted_string(self, locale_name: str) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem: integer_value.IntegerValue(elem).to_formatted_string(locale_name))
        return api_string

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
