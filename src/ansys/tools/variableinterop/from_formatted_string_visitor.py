"""Defines the ``FromFormattedStringVisitor`` class."""
from __future__ import annotations

import distutils.util
import locale

import numpy as np
from overrides import overrides

from .array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from .exceptions import ValueDeserializationUnsupportedException, _error
from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor
from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from .utils.array_to_from_string_util import ArrayToFromStringUtil
from .utils.locale_utils import LocaleUtils
from .variable_value import IVariableValue


class FromFormattedStringVisitor(IVariableTypePseudoVisitor[IVariableValue]):
    """Converts a string formatted for a locale to the ``IVariableValue`` variable
    type."""

    def __init__(self, value: np.str_, locale_name: str):
        """Initialize a new instance."""
        self._value = value
        self._locale_name = locale_name

    @overrides
    def visit_unknown(self) -> IVariableValue:
        raise

    @overrides
    def visit_int(self) -> IntegerValue:
        # We need to use atof and then convert to int, as atoi does not support scientific notation
        result: IntegerValue = LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: np.int64(locale.atof(self._value))
        )
        return result

    @overrides
    def visit_real(self) -> RealValue:
        result: np.str_ = LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: locale.atof(self._value)
        )
        return result

    @overrides
    def visit_boolean(self) -> BooleanValue:
        result: np.str_ = LocaleUtils.perform_safe_locale_action(
            self._locale_name, lambda: bool(distutils.util.strtobool(self._value))
        )
        return result

    @overrides
    def visit_string(self) -> StringValue:
        return self._value

    @overrides
    def visit_file(self) -> IVariableValue:
        raise ValueDeserializationUnsupportedException(_error("ERROR_FILE_FROM_DISPLAY_STR"))

    @overrides
    def visit_int_array(self) -> IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: IntegerArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_int(),
        )

    @overrides
    def visit_real_array(self) -> IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: RealArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_real(),
        )

    @overrides
    def visit_bool_array(self) -> IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: BooleanArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_boolean(),
        )

    @overrides
    def visit_string_array(self) -> IVariableValue:
        return ArrayToFromStringUtil.string_to_value(
            self._value,
            lambda val: StringArrayValue(values=val),
            lambda val: FromFormattedStringVisitor(val, self._locale_name).visit_string(),
        )

    @overrides
    def visit_file_array(self) -> IVariableValue:
        raise ValueDeserializationUnsupportedException(_error("ERROR_FILE_FROM_DISPLAY_STR"))
