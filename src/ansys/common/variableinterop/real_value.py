"""Definition of RealValue."""
from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value


class RealValue(np.float64, variable_value.IVariableValue):
    """
    Wrapper around a real value.

    In Python RealValue is implemented by extending NumPy's float64 type. This means that
    they will decay naturally into numpy.float64 objects when using numpy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def accept(
            self, visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_real(self)

    @property
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.REAL

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
