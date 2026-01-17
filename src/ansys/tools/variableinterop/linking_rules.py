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

from typing import Tuple

from ansys.tools.variableinterop.api import INCOMPATIBLE, TypeCompatibility

from .var_type_array_check import var_type_is_array
from .variable_type import VariableType
from .vartype_arrays_and_elements import get_element_type

_rules: dict[Tuple[VariableType, VariableType], TypeCompatibility] = {
    (VariableType.BOOLEAN, VariableType.INTEGER): TypeCompatibility(True, False, False),
    (VariableType.BOOLEAN, VariableType.REAL): TypeCompatibility(True, False, False),
    (VariableType.BOOLEAN, VariableType.STRING): TypeCompatibility(True, False, False),
    (VariableType.INTEGER, VariableType.BOOLEAN): TypeCompatibility(True, True, False),
    (VariableType.INTEGER, VariableType.REAL): TypeCompatibility(True, True, False),
    (VariableType.INTEGER, VariableType.STRING): TypeCompatibility(True, False, False),
    (VariableType.REAL, VariableType.BOOLEAN): TypeCompatibility(True, True, False),
    (VariableType.REAL, VariableType.INTEGER): TypeCompatibility(True, True, True),
    (VariableType.REAL, VariableType.STRING): TypeCompatibility(True, False, False),
    (VariableType.STRING, VariableType.BOOLEAN): TypeCompatibility(True, False, True),
    (VariableType.STRING, VariableType.INTEGER): TypeCompatibility(True, False, True),
    (VariableType.STRING, VariableType.REAL): TypeCompatibility(True, False, True),
    # Is there a possible case that because of encodings, these conversions are lossy?
    (VariableType.STRING, VariableType.FILE): TypeCompatibility(True, False, False),
    (VariableType.FILE, VariableType.STRING): TypeCompatibility(True, False, True),
}

# TODO: Unit test this function


def is_linking_allowed(source: VariableType, dest: VariableType) -> TypeCompatibility:
    """
    Is linking allowed from the source to the destination type?

    Parameters
    ----------
    source: VariableType
        Type of variable that is the source (the right-hand side of the equation)
    dest: VariableType
        Type of variable that is the destination (the left-hand side of the equation)

    Returns
    -------
    TypeCompatibility
        TypeCompatibility instance that describes whether the linking is allowed
    """
    # If the types are the same, it is allowed
    if source == dest:
        return TypeCompatibility(True, False, False)

    # The source and destination must be both arrays or both scalars
    if var_type_is_array(source) != var_type_is_array(dest):
        return INCOMPATIBLE

    # If handling arrays, test the base type
    if var_type_is_array(source):
        source = get_element_type(source)
        dest = get_element_type(dest)

    # Read the answer from the table, or assume incompatible
    return _rules.get((source, dest), INCOMPATIBLE)
