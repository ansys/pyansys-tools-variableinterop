from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType


class BooleanArrayValue(np.ndarray, variable_value.BooleanValue):
    """
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

    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY
