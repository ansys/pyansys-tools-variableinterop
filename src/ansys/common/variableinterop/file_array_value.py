"""Definition of FileArrayValue."""
from __future__ import annotations

import json
from typing import Any, TypeVar

import numpy as np
from numpy.typing import ArrayLike
from overrides import overrides

import ansys.common.variableinterop.file_scope as file_scope
import ansys.common.variableinterop.file_value as file_value
import ansys.common.variableinterop.isave_context as isave_context
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .utils.array_to_from_string_util import ArrayToFromStringUtil
from .variable_type import VariableType

T = TypeVar("T")


class FileArrayValue(variable_value.CommonArrayValue[file_value.FileValue]):
    """Array of file values.

    In Python FileArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return np.array(values, dtype=file_value.FileValue).view(cls)
        return super().__new__(cls, shape=shape_, dtype=file_value.FileValue)

    @overrides
    def __eq__(self, other):
        return np.array_equal(self, other)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_file_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.FILE_ARRAY

    def to_api_string(self, context: isave_context.ISaveContext) -> str:
        def elem_to_api_obj(item: file_value.FileValue) -> str:
            return item.to_api_object(context)
        return json.dumps(np.vectorize(elem_to_api_obj)(self).tolist())

    @staticmethod
    def from_api_object(value: Any, context: isave_context.ILoadContext,
                        scope: file_scope.FileScope) -> FileArrayValue:
        if isinstance(value, list):

            # Define a function for transforming individual API objects to elements.
            def api_obj_to_elem(item: Any) -> file_value.FileValue:
                if isinstance(item, dict):
                    return scope.from_api_object(item, context)
                else:
                    raise TypeError(f"Encountered a {type(item)} when attempting to deserialize "
                                    f"a file value element. Is the serialized array rectangular?")

            # Construct the item.
            return FileArrayValue(values=np.vectorize(api_obj_to_elem)(np.asarray(value)))
        else:
            raise ValueError("The serialized value was not deserialized as a list.")

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        disp_str: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: np.asscalar(elem).to_display_string(locale_name))
        return disp_str
