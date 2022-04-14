"""Definition of FromFormattedStringVisitor."""
from __future__ import annotations

import distutils.util
import locale
from typing import List

import numpy as np

from ansys.common.variableinterop.array_to_from_string_util import ArrayToFromStringUtil
import ansys.common.variableinterop.boolean_value as boolean_value
from ansys.common.variableinterop.integer_array_value import IntegerArrayValue
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_type_pseudovisitor as pseudo_visitor
import ansys.common.variableinterop.locale_utils as locale_utils
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.variable_value as variable_value


class FromFormattedStringVisitor(pseudo_visitor.IVariableTypePseudoVisitor[
                                     variable_value.IVariableValue]):
    """Converts a string formatted for a locale to a IVariableValue."""

    def __init__(self, value: np.str_, locale_name: str):
        """Initialize the object."""
        self._value = value
        self._locale_name = locale_name

    def visit_unknown(self) -> variable_value.IVariableValue:
        raise

    def visit_int(self) -> integer_value.IntegerValue:
        # We need to use atof and then convert to int, as atoi does not support scientific notation
        result: integer_value.IntegerValue = locale_utils.LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: np.int64(locale.atof(self._value)))
        return result

    def visit_real(self) -> real_value.RealValue:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: locale.atof(self._value))
        return result

    def visit_boolean(self) -> boolean_value.BooleanValue:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: bool(distutils.util.strtobool(self._value)))
        return result

    def visit_string(self) -> string_value.StringValue:
        return self._value

    def visit_file(self) -> variable_value.IVariableValue:
        raise NotImplementedError

    def visit_int_array(self) -> variable_value.IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda shape_or_val: IntegerArrayValue(values=shape_or_val) if isinstance(shape_or_val, List) \
                else IntegerArrayValue(shape_=shape_or_val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_int())

    def visit_real_array(self) -> variable_value.IVariableValue:
        raise

    def visit_bool_array(self) -> variable_value.IVariableValue:
        raise

    def visit_string_array(self) -> variable_value.IVariableValue:
        raise

    def visit_file_array(self) -> variable_value.IVariableValue:
        raise NotImplementedError
