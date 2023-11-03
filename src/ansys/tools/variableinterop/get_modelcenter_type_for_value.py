# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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
"""Defines the ``GetModelCenterTypeForValue`` class."""
from overrides import overrides

from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from .variable_value import IVariableValue


class GetModelCenterTypeForValue:
    """Provides a static method for getting the model center for an ``IVariableValue``
    type."""

    @staticmethod
    def get_modelcenter_type(value: IVariableValue) -> str:
        """
        Get the model center type for an ``IVariableValue`` variable.

        Parameters
        ----------
        value : IVariableValue
            ``IVariableValue`` variable to get the model center type for.

        Returns
        -------
        str
            Model center type.
        """
        generator = GetModelCenterTypeForValue._GetModelCenterTypeVisitor()
        result: str = vartype_accept(generator, value.variable_type)
        return result

    class _GetModelCenterTypeVisitor(IVariableTypePseudoVisitor[str]):
        """Provides the helper visitor used by the ``GetModelCenterTypeForValue``
        class."""

        @overrides
        def visit_unknown(self) -> str:
            return "none"

        @overrides
        def visit_int(self) -> str:
            return "int"

        @overrides
        def visit_real(self) -> str:
            return "double"

        @overrides
        def visit_boolean(self) -> str:
            return "bool"

        @overrides
        def visit_string(self) -> str:
            return "string"

        @overrides
        def visit_file(self) -> str:
            return "file"

        @overrides
        def visit_int_array(self) -> str:
            return "int[]"

        @overrides
        def visit_real_array(self) -> str:
            return "double[]"

        @overrides
        def visit_bool_array(self) -> str:
            return "bool[]"

        @overrides
        def visit_string_array(self) -> str:
            return "string[]"

        @overrides
        def visit_file_array(self) -> str:
            return "file[]"
