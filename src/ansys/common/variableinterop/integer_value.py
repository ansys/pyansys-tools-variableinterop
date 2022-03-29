from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType


class IntegerValue(np.int64, variable_value.IVariableValue):
    """
    In Python IntegerValue is implemented by extending NumPy's int64 type. This means that
    they will decay naturally into numpy.int64 objects when using numpy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards. For
    example, when converting from real to integer, the value will be floored instead of
    rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def accept(
        self, visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        # inheritdoc (What is the correct way to do this?)
        return visitor.visit_int(self)

    def variable_type(self) -> VariableType:
        # inheritdoc (What is the correct way to do this?)
        return VariableType.INTEGER
