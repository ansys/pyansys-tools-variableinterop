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
"""Provides a method for converting a formatted string to a value."""
from numpy import unicode_

from .from_formatted_string_visitor import FromFormattedStringVisitor
from .ivariable_type_pseudovisitor import vartype_accept
from .variable_type import VariableType
from .variable_value import IVariableValue


def from_formatted_string(var_type: VariableType, source: str, locale_name: str) -> IVariableValue:
    """
    Convert a value formatted to a specific locale back into an IVariableValue.

    Parameters
    ----------
    var_type : VariableType
        The type of variable to convert to.
    source : str
        The string to convert.
    locale_name : str
        The locale the string was formatted in.

    Returns
    -------
    IVariableValue
        An IVariableValue of the specified type whose value matches the given string.
    """
    generator: FromFormattedStringVisitor = FromFormattedStringVisitor(
        unicode_(source), locale_name
    )
    result: IVariableValue = vartype_accept(generator, var_type)
    return result
