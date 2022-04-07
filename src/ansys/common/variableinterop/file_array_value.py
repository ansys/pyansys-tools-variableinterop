from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType


class FileArrayValue(np.ndarray, variable_value.IVariableValue):
    """
    In Python FileArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    # TODO: __new__() implementation (what will the data type be?)

    def accept(
        self,
        visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_file_array(self)

    def variable_type(self) -> VariableType:
        return VariableType.FILE_ARRAY

    # TODO: full implementation

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
