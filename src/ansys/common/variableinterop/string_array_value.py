from __future__ import annotations

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType

class StringArrayValue(np.ndarray, variable_value.IVariableValue):

    def accept(
        self,
        visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_string_array(self)

    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY