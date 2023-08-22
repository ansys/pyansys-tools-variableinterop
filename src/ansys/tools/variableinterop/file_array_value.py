"""Definition of FileArrayValue."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional, TypeVar, cast

import numpy
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
    Array of file values.

    In Python FileArrayValue is implemented by extending NumPy's ndarray type. This
    means that they will decay naturally into numpy.ndarray objects when using numpy's
    array operators. It also means that they inherit many of the numpy behaviors, which
    may be slightly different from the behaviors specified in the variable interop
    standards. For example, when converting from real to integer, the value will be
    floored instead of rounded. If you want the variable interop standard conversions,
    use xxxx (TODO)
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return numpy.array(values, dtype=FileValue).view(cls)
        return super().__new__(cls, shape=shape_, dtype=FileValue).view(cls)

    @overrides
    def __eq__(self, other):
        return numpy.array_equal(self, other)

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
            The context used for saving.

        Returns
        -------
        str
            A string appropriate for use in files and APIs.
        """
        if context is None:
            raise ValueError(_error("ERROR_FILE_NO_CONTEXT"))

        def elem_to_api_obj(item: FileValue) -> Dict[str, Optional[str]]:
            return item.to_api_object(cast(ISaveContext, context))

        return json.dumps(numpy.vectorize(elem_to_api_obj)(self).tolist())

    @staticmethod
    def from_api_object(value: Any, context: ILoadContext, scope: FileScope) -> FileArrayValue:
        """
        Initialize a new FileArrayValue from a list of api strings.

        Parameters
        ----------
        value The value to use.
        context The load context to initialize the value with.
        scope The scope to initialize the value in.

        Returns
        -------
        A new FileArrayValue initialized from value.
        """
        if isinstance(value, list):
            # Define a function for transforming individual API objects to elements.
            def api_obj_to_elem(item: Any) -> FileValue:
                if isinstance(item, dict):
                    return scope.from_api_object(item, context)
                else:
                    raise TypeError(_error("ERROR_JAGGED_FILE_ARRAY", type(item)))

            # Construct the item.
            return FileArrayValue(values=numpy.vectorize(api_obj_to_elem)(numpy.asarray(value)))
        else:
            raise ValueError("The serialized value was not deserialized as a list.")

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        disp_str: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: numpy.ndarray.item(elem).to_display_string(locale_name)
        )
        return disp_str
