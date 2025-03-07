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
"""Provides a method for checking whether a variable type is an array type."""
from overrides import overrides

from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from .variable_type import VariableType


class _VarTypeIsArrayVisitor(IVariableTypePseudoVisitor[bool]):
    """
    Determines whether the visited variable type is an array.

    ``True`` is returned if the visited type is an array type, and ``False`` is returned
    otherwise.
    """

    @overrides
    def visit_unknown(self) -> bool:
        return False

    @overrides
    def visit_int(self) -> bool:
        return False

    @overrides
    def visit_real(self) -> bool:
        return False

    @overrides
    def visit_boolean(self) -> bool:
        return False

    @overrides
    def visit_string(self) -> bool:
        return False

    @overrides
    def visit_file(self) -> bool:
        return False

    @overrides
    def visit_int_array(self) -> bool:
        return True

    @overrides
    def visit_real_array(self) -> bool:
        return True

    @overrides
    def visit_bool_array(self) -> bool:
        return True

    @overrides
    def visit_string_array(self) -> bool:
        return True

    @overrides
    def visit_file_array(self) -> bool:
        return True


def var_type_is_array(vartype: VariableType) -> bool:
    """
    Check whether the provided variable type is an array type.

    Parameters
    ----------
    vartype : VariableType
        Variable type of interest.

    Returns
    -------
    bool
        ``True`` if the specified variable type is an array type, ``False`` otherwise.
    """
    return vartype_accept(_VarTypeIsArrayVisitor(), vartype)
