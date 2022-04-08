"""Definition of BooleanValue."""
from __future__ import annotations

import locale

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.locale_utils as local_utils
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value


class BooleanValue(np.bool_, variable_value.IVariableValue):
    """
    Wrapper around a boolean value.

    If you want the variable interop standard conversions, use xxxx (TODO)
    """

    # hashcode definition here

    def accept(
            self, visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_boolean(self)

    @property
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    def to_formatted_string(self, locale_name: str) -> str:
        result: np.str_ = local_utils.LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%s", self))
        return result

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
