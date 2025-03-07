# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Defines the ``FromFormattedStringVisitor`` class."""
from __future__ import annotations

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


def strtobool(val):
    """
    Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values are 'n', 'no',
    'f', 'false', 'off', and '0'.  Raises ValueError if 'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


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
            self._locale_name, lambda: bool(strtobool(self._value))
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
