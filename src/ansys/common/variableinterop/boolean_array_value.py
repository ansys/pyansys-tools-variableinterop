from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from ansys.common.variableinterop import ivariable_visitor
from ansys.common.variableinterop import variable_type
from ansys.common.variableinterop import variable_value


class BooleanArrayValue(NDArray[np.bool_], variable_value.IVariableValue):
    """Array of boolean values.

    In Python BooleanArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def __new__(cls, shape_):
        return super().__new__(cls, shape=shape_, dtype=np.bool_)

    def accept(
            self,
            visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_boolean_array(self)

    def variable_type(self) -> variable_type.VariableType:
        return VariableType.BOOLEAN_ARRAY

    # TODO: full implementation

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
