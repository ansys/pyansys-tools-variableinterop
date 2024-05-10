# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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
"""Defines the ``VariableType`` class."""
from __future__ import annotations

from enum import Enum
from typing import Dict

from .utils.locale_utils import Strings


class VariableType(Enum):
    """Provides an enumeration of the possible variable types."""

    # When editing this enumeration,
    # be sure to also update ``IVariableTypePseudoVisitor``
    # and its implementation of the pseudo-visitor pattern
    # appropriately.
    UNKNOWN = 0
    """Type is unknown."""
    INTEGER = 1
    """
    Integer values.

    These are stored as 64-bit signed integers
    """
    REAL = 2
    """
    Real values.

    These are stored as 64-bit floating point numbers
    """
    BOOLEAN = 3
    """Boolean values."""
    STRING = 4
    """String values."""
    FILE = 5
    """File values."""
    INTEGER_ARRAY = 6
    """
    Array of integer values.

    These are stored as 64-bit signed integers. Multidimensional arrays are supported.
    """
    REAL_ARRAY = 7
    """
    Array of real values.

    These are stored as 64-bit floating point numbers. Multidimensional arrays are
    supported.
    """
    BOOLEAN_ARRAY = 8
    """
    Array of Boolean values.

    Multidimensional arrays are supported.
    """
    STRING_ARRAY = 9
    """
    Array of string values.

    Multidimensional arrays are supported.
    """
    FILE_ARRAY = 10
    """
    Array of file values.

    Multidimensional arrays are supported.
    """

    def to_display_string(self) -> str:
        """
        Get the display string for the ``VariableType`` value.

        Returns
        -------
        str
            Display string.
        """
        __valtype_display_string: Dict[VariableType, str] = {
            VariableType.REAL: "DISPLAY_STRING_REAL",
            VariableType.INTEGER: "DISPLAY_STRING_INTEGER",
            VariableType.BOOLEAN: "DISPLAY_STRING_BOOL",
            VariableType.STRING: "DISPLAY_STRING_STRING",
            VariableType.FILE: "DISPLAY_STRING_FILE",
            VariableType.REAL_ARRAY: "DISPLAY_STRING_REAL_ARRAY",
            VariableType.INTEGER_ARRAY: "DISPLAY_STRING_INTEGER_ARRAY",
            VariableType.BOOLEAN_ARRAY: "DISPLAY_STRING_BOOL_ARRAY",
            VariableType.STRING_ARRAY: "DISPLAY_STRING_STRING_ARRAY",
            VariableType.FILE_ARRAY: "DISPLAY_STRING_FILE_ARRAY",
            VariableType.UNKNOWN: "DISPLAY_STRING_UNKNOWN",
        }

        return Strings.get("DisplayStrings", __valtype_display_string[self])
