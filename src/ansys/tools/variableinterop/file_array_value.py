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
"""Defines the ``FileArrayValue`` class."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional, TypeVar, cast

import numpy as np
from numpy.typing import ArrayLike
from overrides import overrides

from .exceptions import _error
from .file_scope import FileScope
from .file_value import FileValue
from .isave_context import ILoadContext, ISaveContext
from .ivariable_visitor import IVariableValueVisitor
from .utils.array_to_from_string_util import ArrayToFromStringUtil
from .variable_type import VariableType
from .variable_value import CommonArrayValue

T = TypeVar("T")


class FileArrayValue(CommonArrayValue[FileValue]):
    """
    Stores a value for the ``FileArrayValue`` variable type.

    In Python, the ``FileArrayValue`` type is implemented by extending NumPy's ``ndarray`` type.
    This means that they decay naturally into ``numpy.ndarray`` objects when using NumPy's
    array operators.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = (), values: ArrayLike = None):
        if values is not None:
            return np.array(values, dtype=FileValue).view(cls)
        return super().__new__(cls, shape=shape_, dtype=FileValue).view(cls)

    @overrides
    def __eq__(self, other):
        return np.array_equal(self, other)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_file_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.FILE_ARRAY

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        """
        Convert this value to an API string.

        Parameters
        ----------
        context : ISaveContext
            Context used for saving.

        Returns
        -------
        str
            String appropriate for use in files and APIs.
        """
        if context is None:
            raise ValueError(_error("ERROR_FILE_NO_CONTEXT"))

        def elem_to_api_obj(item: FileValue) -> Dict[str, Optional[str]]:
            return item.to_api_object(cast(ISaveContext, context))

        return json.dumps(np.vectorize(elem_to_api_obj)(self).tolist())

    @staticmethod
    def from_api_object(value: Any, context: ILoadContext, scope: FileScope) -> FileArrayValue:
        """
        Initialize a new ``FileArrayValue`` type from a list of API strings.

        Parameters
        ----------
        value : Any
            Value to use.
        context : ILoadContext
            Load context to initialize the value with.
        scope : FileScope
            Scope to initialize the value in.

        Returns
        -------
        FileArrayValue
            New ``FileArrayValue`` type initialized from the value.
        """
        if isinstance(value, list):
            # Define a function for transforming individual API objects to elements.
            def api_obj_to_elem(item: Any) -> FileValue:
                if isinstance(item, dict):
                    return scope.from_api_object(item, context)
                else:
                    raise TypeError(_error("ERROR_JAGGED_FILE_ARRAY", type(item)))

            # Construct the item.
            return FileArrayValue(
                values=np.vectorize(api_obj_to_elem)(np.asarray(value, dtype="object"))
            )
        else:
            raise ValueError("The serialized value was not deserialized as a list.")

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        disp_str: str = ArrayToFromStringUtil.value_to_string(
            # TODO: asscalar was deprecated, item breaks the jagged array test
            self,
            lambda elem: np.ndarray.item(elem).to_display_string(locale_name),
        )
        return disp_str
