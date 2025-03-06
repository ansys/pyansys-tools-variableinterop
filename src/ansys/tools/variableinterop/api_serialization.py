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
"""Defines the ``ToAPIStringVisitor`` class."""
from typing import Optional

from overrides import overrides

from .api_string_to_value_visitor import APIStringToValueVisitor
from .array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from .file_array_value import FileArrayValue
from .file_scope import FileScope
from .file_value import FileValue
from .isave_context import ILoadContext, ISaveContext
from .ivariable_type_pseudovisitor import vartype_accept
from .ivariable_visitor import IVariableValueVisitor
from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from .variable_type import VariableType
from .variable_value import IVariableValue


class ToAPIStringVisitor(IVariableValueVisitor[str]):
    """Visits values and converts them to an API string."""

    def __init__(self, save_context: Optional[ISaveContext]):
        """
        Initialize the visitor.

        Parameters
        ----------
        save_context : Optional[ISaveContext], optional
            Save context to use for conversion. The default value is ``None``, which indicates
            that you do not want to support file values.
        """
        self._save_context = save_context

    @overrides
    def visit_integer(self, value: IntegerValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_real(self, value: RealValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_boolean(self, value: BooleanValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_string(self, value: StringValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_file(self, value: FileValue) -> str:
        return value.to_api_string(self._save_context)

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> str:
        return value.to_api_string(self._save_context)


def to_api_string(value: IVariableValue, save_context: Optional[ISaveContext] = None) -> str:
    """
    Convert a variable value to an API string.

    Parameters
    ----------
    value : IVariableValue
        Value to convert to an API string.
    save_context : Optional[ISaveContext], optional
        Save context to use for conversion. The default value is ``None``, which indicates
        that you do not want to support file values.

    Returns
    -------
    str
        Serialized form of the value.
    """
    return value.accept(ToAPIStringVisitor(save_context))


def from_api_string(
    var_type: VariableType,
    source: str,
    fscope: Optional[FileScope] = None,
    load_context: Optional[ILoadContext] = None,
) -> IVariableValue:
    """
    Generate a value from an API string.

    Parameters
    ----------
    var_type : VariableType
        Variable type to generate.
    source : str
       Source string.
    fscope : Optional[FileScope], optional
        File scope to use to deserialize file variables. The default is ``None``,
        which indictates that file variables are not needed.
    load_context : Optional[ILoadContext], optional
        Load context to read file contents from. The default is ``None``, which
        indicates file variables are not needed.

    Returns
    -------
    IVariableValue
        Implementation of ``IVariableValue`` of the correct type with a value parsed from the
        specified string.
    """
    generator: APIStringToValueVisitor = APIStringToValueVisitor(source, fscope, load_context)
    result: IVariableValue = vartype_accept(generator, var_type)
    return result
