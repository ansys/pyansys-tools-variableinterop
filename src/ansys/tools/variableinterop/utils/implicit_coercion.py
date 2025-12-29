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
"""Provides utilities for implicitly coercing arbitrary Python objects \ into the
appropriate ``IVariableValue`` type."""
from __future__ import annotations

from decimal import Decimal
import functools
import inspect
from typing import Any, Dict, List, Optional, Union, get_type_hints

import numpy as np

from ..array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from ..exceptions import _error
from ..scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from ..variable_value import CommonArrayValue, IVariableValue

__TYPE_MAPPINGS = {
    int: IntegerValue,
    np.int8: IntegerValue,
    np.int16: IntegerValue,
    np.int32: IntegerValue,
    np.int64: IntegerValue,
    float: RealValue,
    np.float16: RealValue,
    np.float32: RealValue,
    np.float64: RealValue,
    bool: BooleanValue,
    np.bool_: BooleanValue,
    str: StringValue,
    np.str_: StringValue,
}
"""
This map applies when coercing scalar values to a method argument type hinted as
``IVariableValue``.

It is used to determine the specific ``IVariableValue`` implementation that should be
generated from the argument's actual runtime value. The type of the actual runtime
argument value is the key in the dictionary, and the value is the specific
``IVariableValue`` implementation that should be used.
"""

__ARR_TYPE_MAPPINGS = {
    np.int8: IntegerArrayValue,
    np.int16: IntegerArrayValue,
    np.int32: IntegerArrayValue,
    np.int64: IntegerArrayValue,
    np.float16: RealArrayValue,
    np.float32: RealArrayValue,
    np.float64: RealArrayValue,
    np.bool_: BooleanArrayValue,
    np.str_: StringArrayValue,
}
"""
This map applies when coercing ndarray values to a method argument type hinted as
``IVariableValue``.

It is used to determine the specific ``IVariableValue`` implementation that should be
generated from the argument's actual runtime value. The dtype of the actual ndarray
value at runtime is the key in the dictionary, and the value is the specific
``IVariableValue`` implementation that should be used.
"""

__ALLOWED_SPECIFIC_IMPLICIT_COERCE = {
    IntegerValue: [
        int,
        Decimal,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        bool,
        np.bool_,
        BooleanValue,
    ],
    RealValue: [
        float,
        np.float16,
        np.float32,
        np.float64,
        bool,
        np.bool_,
        BooleanValue,
    ],
    BooleanValue: [bool, np.bool_],
    StringValue: [
        int,
        np.integer,
        IntegerValue,
        bool,
        np.bool_,
        BooleanValue,
        float,
        np.inexact,
        RealValue,
        str,
        np.str_,
        StringValue,
    ],
}
"""
Rules for implicitly coercing scalar values to a specific ``IVariableValue``
implementation.

This map is used to determine whether the coercion is allowed. The ``IVariableValue``
implementation type is the key. The value is a list of all types that may be implicitly
coerced to that type.
"""

__ALLOWED_SPECIFIC_IMPLICIT_COERCE_ARR = {
    IntegerArrayValue: [np.int8, np.int16, np.int32, np.int64, np.bool_],
    RealArrayValue: [np.float16, np.float32, np.float64, np.bool_],
    BooleanArrayValue: [np.bool_],
    StringArrayValue: [np.integer, np.inexact, np.bool_, np.str_],
}
"""
Rules for implicitly coercing array values to a specific ``IVariableValue``
implementation.

The map is used to determine whether the coercion is allowed. The ``IVariableValue``
implementation type is the key. NumPy ndarrays with their dtype set to any of the items
in the value list are allowed to be implicitly coerced to the type represented by the
key.
"""


def _is_optional(arg_type: type) -> bool:
    """
    Determine if a type object refers to an ``Optional[x]``.

    Parameters
    ----------
    arg_type : type
        Type to check for optional.

    Returns
    -------
    bool
        ``True`` if the argument passed is ``Optional[x]`` for some x.
    """
    return (
        hasattr(arg_type, "__origin__")
        and arg_type.__origin__ == Union  # type: ignore
        and len(arg_type.__args__) == 2  # type: ignore
        and arg_type.__args__[1] == type(None)  # type: ignore
    )


def _get_optional_type(arg_type: type) -> type:
    """
    Get "x" from "Optional[x]".

        Parameters
    ----------
    arg_type : type
        "Optional[x]" type. This parameter is only valid if the ``_is_optional`` argument
        returns ``True``.

    Returns
    -------
    type
        If the ``_is_optional`` argument returns ``True``, the "x" from ``Optional[x]``
        is returned.
        If the ``_is_optional`` argument returns ``False``, the behavior is undeclared.
    """
    return arg_type.__args__[0]  # type: ignore


def _specific_implicit_coerce_allowed(
    target_arg_type: type, actual_arg_type: type, ruleset: Dict[type, List[type]]
) -> bool:
    """
    Check whether implicit coercion from a given type to a given type is allowed.

    Parameters
    ----------
    target_arg_type : type
        Target type of the argument (type declared on the method).
    actual_arg_type : type
        Actual type of the argument (type of the actual object being passed).
    ruleset : Dict[type, List[type]]
        Map of types to allowed coercion types.

    Returns
    -------
    bool
        ``True`` if implicit coercion to the target type from the actual type is allowed,
        ``False`` otherwise.
    """
    if issubclass(actual_arg_type, target_arg_type):
        return True

    if target_arg_type in ruleset:
        return any(
            issubclass(actual_arg_type, allowed_coerce_type)
            for allowed_coerce_type in ruleset[target_arg_type]
        )
    else:
        return False


def __numpy_array_dtype(arg: Any) -> Optional[type]:
    if isinstance(arg, np.ndarray):
        return arg.dtype.type
    else:
        return None


def __implicit_coerce_single_scalar_free(arg: Any):
    for cls in type(arg).__mro__:
        if cls in __TYPE_MAPPINGS:
            return __TYPE_MAPPINGS[cls](arg)
    raise TypeError(_error("ERROR_IMPLICIT_COERCE_NOT_ALLOWED", type(arg), IVariableValue))


def __implicit_coerce_single_array_free(arg: Any, arr_type: type) -> IVariableValue:
    for cls in arr_type.__mro__:
        if cls in __ARR_TYPE_MAPPINGS:
            return __ARR_TYPE_MAPPINGS[cls](values=arg)
    raise TypeError(
        _error(
            "ERROR_IMPLICIT_COERCE_NOT_ALLOWED",
            " with dtype ".join([str(type(arg)), str(arr_type)]),
            IVariableValue,
        )
    )


def __implicit_coerce_single_array_specific(arg: Any, target_type: type):
    maybe_arr_type: Optional[type] = __numpy_array_dtype(arg)
    if maybe_arr_type is not None:
        if _specific_implicit_coerce_allowed(
            target_type, maybe_arr_type, __ALLOWED_SPECIFIC_IMPLICIT_COERCE_ARR
        ):
            return target_type(values=arg)

    from_type_str: str = str(type(arg))
    if maybe_arr_type is not None:
        from_type_str = " with dtype ".join([str(type(arg)), str(maybe_arr_type)])
    raise TypeError(_error("ERROR_IMPLICIT_COERCE_NOT_ALLOWED", from_type_str, target_type))


def __implicit_coerce_single_scalar_specific(arg: Any, target_type: type):
    if _specific_implicit_coerce_allowed(
        target_type, type(arg), __ALLOWED_SPECIFIC_IMPLICIT_COERCE
    ):
        return target_type(arg)
    raise TypeError(_error("ERROR_IMPLICIT_COERCE_NOT_ALLOWED", type(arg), target_type))


def implicit_coerce_single(arg: Any, arg_type: type) -> Any:
    """
    Attempt to coerce the argument into the given type.

    This function uses implicit semantics in that lossy conversions are
    not considered (such as int64->real64 because precision may be lost).

    Parameters
    ----------
    arg : Any
        Object to attempt to convert.
    arg_type : type
        Type of object to convert to. The type must be ``IVariableValue`` or
        something derived from it.

    Returns
    -------
    Any
        Converted object

    Raises
    ------
    TypeError
        If the argument cannot be converted to the supplied type.
    """
    if _is_optional(arg_type):
        if arg is None:
            return None
        # TODO: Lots of diminutive cases. This currently just handles Optional[T]
        arg_type = _get_optional_type(arg_type)

    if issubclass(type(arg), arg_type):
        # No type coercion necessary. Pass through the original argument.
        return arg

    if arg_type == IVariableValue:
        maybe_np_array_type: Optional[type] = __numpy_array_dtype(arg)
        if maybe_np_array_type is None:
            return __implicit_coerce_single_scalar_free(arg)
        else:
            return __implicit_coerce_single_array_free(arg, maybe_np_array_type)

    # TODO: This probably doesn't have all the right semantics for our set of implicit
    #  type conversions
    if issubclass(arg_type, IVariableValue):
        if arg is None:
            raise TypeError(f"Type {type(arg)} cannot be converted to {arg_type}")
        # Check if the proposed conversion is even allowed:
        if issubclass(arg_type, CommonArrayValue):
            return __implicit_coerce_single_array_specific(arg, arg_type)
        else:
            return __implicit_coerce_single_scalar_specific(arg, arg_type)

    # TODO: More types and other error conditions

    # If we don't understand the type, ignore it and just pass through
    return arg


def implicit_coerce(func: Any) -> Any:
    """
    Use to decorate functions using the PEP 484 typing system to try and coerce any
    arguments that accept the ``IVariableValue`` type or any derived type into an
    acceptable value.

    Parameters
    ----------
    func : Any
        Function to decorate.

    Returns
    -------
    Any
        Wrapper function.
    """
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound_sig = signature.bind(*args, **kwargs)
        bound_sig.apply_defaults()
        for key in bound_sig.arguments:
            if key in type_hints:
                bound_sig.arguments[key] = implicit_coerce_single(
                    bound_sig.arguments[key], type_hints[key]
                )

        return func(*bound_sig.args, **bound_sig.kwargs)

    return wrapper
