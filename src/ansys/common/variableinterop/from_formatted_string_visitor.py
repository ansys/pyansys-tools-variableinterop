"""Definition of FromFormattedStringVisitor."""
from __future__ import annotations

import distutils.util
import locale
from typing import List

import numpy as np
from overrides import overrides

from ansys.common.variableinterop.array_to_from_string_util import ArrayToFromStringUtil
from ansys.common.variableinterop.boolean_array_value import BooleanArrayValue
import ansys.common.variableinterop.boolean_value as boolean_value
from ansys.common.variableinterop.integer_array_value import IntegerArrayValue
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_type_pseudovisitor as pseudo_visitor
import ansys.common.variableinterop.locale_utils as locale_utils
from ansys.common.variableinterop.real_array_value import RealArrayValue
import ansys.common.variableinterop.real_value as real_value
from ansys.common.variableinterop.string_array_value import StringArrayValue
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.variable_value as variable_value


class FromFormattedStringVisitor(pseudo_visitor.IVariableTypePseudoVisitor[
                                     variable_value.IVariableValue]):
    """Converts a string formatted for a locale to a IVariableValue."""

    def __init__(self, value: np.str_, locale_name: str):
        """Initialize the object."""
        self._value = value
        self._locale_name = locale_name

    @overrides
    def visit_unknown(self) -> variable_value.IVariableValue:
        raise

    @overrides
    def visit_int(self) -> integer_value.IntegerValue:
        # We need to use atof and then convert to int, as atoi does not support scientific notation
        result: integer_value.IntegerValue = locale_utils.LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: np.int64(locale.atof(self._value)))
        return result

    @overrides
    def visit_real(self) -> real_value.RealValue:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: locale.atof(self._value))
        return result

    @overrides
    def visit_boolean(self) -> boolean_value.BooleanValue:
        result: np.str_ = locale_utils.LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: bool(distutils.util.strtobool(self._value)))
        return result

    @overrides
    def visit_string(self) -> string_value.StringValue:
        return self._value

    @overrides
    def visit_file(self) -> variable_value.IVariableValue:
        raise NotImplementedError

    @overrides
    def visit_int_array(self) -> variable_value.IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: IntegerArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_int())

    @overrides
    def visit_real_array(self) -> variable_value.IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: RealArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_real())

    @overrides
    def visit_bool_array(self) -> variable_value.IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: BooleanArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_boolean())

    @overrides
    def visit_string_array(self) -> variable_value.IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: StringArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_string())

    @overrides
    def visit_file_array(self) -> variable_value.IVariableValue:
        raise NotImplementedError
