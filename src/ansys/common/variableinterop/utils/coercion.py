"""This module contains utilities for coercing arbitrary Python objects \
into the appropriate IVariableValue type."""
from __future__ import annotations

import functools
import inspect
import typing
from typing import Any, Dict, List, Optional

import numpy as np

import ansys.common.variableinterop.array_values as array_values
import ansys.common.variableinterop.scalar_values as scalar_values
import ansys.common.variableinterop.variable_value as variable_value

__TYPE_MAPPINGS = {
    int: scalar_values.IntegerValue,
    np.integer: scalar_values.IntegerValue,
    float: scalar_values.RealValue,
    np.float16: scalar_values.RealValue,
    np.float32: scalar_values.RealValue,
    np.float64: scalar_values.RealValue,
    bool: scalar_values.BooleanValue,
    np.bool_: scalar_values.BooleanValue,
    str: scalar_values.StringValue,
    np.str_: scalar_values.StringValue
}
"""
This map applies when coercing a non-IVariableValue type to a method argument that converts an
IVariableValue. The type of the actual runtime argument value is the key in the dictionary,
and the value is the specific IVariableValue implementation that should be used.
"""

__ARR_TYPE_MAPPINGS = {
    np.integer: array_values.IntegerArrayValue,
    np.float16: array_values.RealArrayValue,
    np.float32: array_values.RealArrayValue,
    np.float64: array_values.RealArrayValue,
    np.bool_: array_values.BooleanArrayValue,
    np.str_: array_values.StringArrayValue
}
"""
This map applies when coercing a non-IVariableValue type to a method argument that converts an
IVariableValue. The type of the actual runtime argument value is the key in the dictionary,
and the value is the specific IVariableValue implementation that should be used.
"""

__ALLOWED_SPECIFIC_IMPLICIT_COERCE = {
    scalar_values.IntegerValue: [int, np.integer, bool, np.bool_, scalar_values.BooleanValue],
    scalar_values.RealValue: [float, np.float16, np.float32, np.float64,
                              bool, np.bool_, scalar_values.BooleanValue],
    scalar_values.BooleanValue: [bool, np.bool_],
    scalar_values.StringValue: [int, np.integer, scalar_values.IntegerValue,
                                bool, np.bool_, scalar_values.BooleanValue,
                                float, np.inexact, scalar_values.RealValue,
                                str, np.str_, scalar_values.StringValue],
    }
"""
This map applies when coercing any value to a specific IVariableValue implementation.
The type declared in the method definition is the key in the dictionary,
and the values are the allowable runtime types that may be converted implicitly to that type.
"""

__ALLOWED_SPECIFIC_IMPLICIT_COERCE_ARR = {
    array_values.IntegerArrayValue: [np.integer, np.bool_],
    array_values.RealArrayValue: [np.float16, np.float32, np.float64, np.bool_],
    array_values.BooleanArrayValue: [np.bool_],
    array_values.StringArrayValue: [np.integer, np.inexact, np.bool_, np.str_]
}


def _is_optional(arg_type: type) -> bool:
    """
    Determine if a type object refers to an Optional[x].

    Parameters
    ----------
    arg_type The type to check for optional

    Returns
    -------
    True if the argument passed in is Optional[x] for some x.
    """
    return (
            hasattr(arg_type, "__origin__")
            and arg_type.__origin__ == typing.Union  # type: ignore
            and len(arg_type.__args__) == 2  # type: ignore
            and arg_type.__args__[1] == type(None)  # type: ignore
    )


def _get_optional_type(arg_type: type) -> type:
    """
    If _is_optional(arg_type) returns true, this function will return \
    the type argument to Optional[x]. If _is_optional(arg_type) returns \
    false, this function's behavior is undeclared.

    Parameters
    ----------
    arg_type The Optional[x] type. Only valid if _is_optional(arg_type) returns true

    Returns
    -------
    The 'x' from Optional[x].
    """
    return arg_type.__args__[0]  # type: ignore


def _specific_implicit_coerce_allowed(target_arg_type: type,
                                      actual_arg_type: type,
                                      ruleset: Dict[type, List[type]]) -> bool:
    """
    Check whether implicit coercion from a given type to a given type is allowed or not.

    Parameters
    ----------
    target_arg_type the target type of the argument (the type declared on the method)
    actual_arg_type the actual type of the argument (the type of the actual object being passed)

    Returns
    -------
    True if implicit coercion to the target type from the actual type is allowed,
    False otherwise.
    """
    if issubclass(actual_arg_type, target_arg_type):
        return True

    if target_arg_type in ruleset:
        return any(issubclass(actual_arg_type, allowed_coerce_type)
                   for allowed_coerce_type in ruleset[target_arg_type])
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
    # TODO: Consider passing in more context for the exception
    # TODO: types come out to
    #  <class 'ansys.common.variableinterop.variable_value.IVariableValue'>.
    #  Can that be simplified?
    raise TypeError(f"Type {type(arg)} cannot be converted to {variable_value.IVariableValue}")


def __implicit_coerce_single_array_free(arg: Any, arr_type: type) -> variable_value.IVariableValue:
    for cls in arr_type.__mro__:
        if cls in __ARR_TYPE_MAPPINGS:
            return __ARR_TYPE_MAPPINGS[cls](values=arg)
    raise TypeError(f"Type {type(arg)} cannot be converted to {variable_value.IVariableValue}")


def __implicit_coerce_single_array_specific(arg: Any, target_type: type):
    maybe_arr_type: Optional[type] = __numpy_array_dtype(arg)
    if maybe_arr_type is not None:
        if _specific_implicit_coerce_allowed(target_type, maybe_arr_type,
                                             __ALLOWED_SPECIFIC_IMPLICIT_COERCE_ARR):
            return target_type(values=arg)
    raise TypeError(f"Type {type(arg)} cannot be converted to {target_type}")


def __implicit_coerce_single_scalar_specific(arg: Any, target_type: type):
    if _specific_implicit_coerce_allowed(target_type, type(arg),
                                         __ALLOWED_SPECIFIC_IMPLICIT_COERCE):
        return target_type(arg)
    raise TypeError(f"Type {type(arg)} cannot be converted to {target_type}")

def implicit_coerce_single(arg: Any, arg_type: type) -> Any:
    """
    Attempt to coerce the argument into the given type.

    This function uses implicit semantics in that lossy conversions are
    not considered (such as int64->real64 since precision may be lost).

    Parameters
    ----------
    arg The object to attempt to convert
    arg_type The type of object to convert to. Must be IVariableValue \
        or something derived from it.

    Returns
    -------
    The converted object

    Throws
    ------
    TypeError if the argument cannot be converted to the supplied type
    """
    if _is_optional(arg_type):
        if arg is None:
            return None
        # TODO: Lots of diminutive cases. This currently just handles Optional[T]
        arg_type = _get_optional_type(arg_type)

    if issubclass(type(arg), arg_type):
        # No type coercion necessary. Pass through the original argument.
        return arg

    if arg_type == variable_value.IVariableValue:
        maybe_np_array_type: Optional[type] = __numpy_array_dtype(arg)
        if maybe_np_array_type is None:
            return __implicit_coerce_single_scalar_free(arg)
        else:
            return __implicit_coerce_single_array_free(arg, maybe_np_array_type)

    # TODO: This probably doesn't have all the right semantics for our set of implicit
    #  type conversions
    if issubclass(arg_type, variable_value.IVariableValue):
        if arg is None:
            raise TypeError(f"Type {type(arg)} cannot be converted to {arg_type}")
        # Check if the proposed conversion is even allowed:
        if issubclass(arg_type, variable_value.CommonArrayValue):
            return __implicit_coerce_single_array_specific(arg, arg_type)
        else:
            return __implicit_coerce_single_scalar_specific(arg, arg_type)

    # TODO: More types and other error conditions

    # If we don't understand the type, ignore it and just pass through
    return arg


def implicit_coerce(func):
    """
    Use to decorate functions that use the PEP 484 typing system to try \
    and coerce any arguments that accept IVariableValue or any derived \
    type into an acceptable value.

    Parameters
    ----------
    func The function to decorate

    Returns
    -------
    The wrapper function
    """
    assert inspect.isfunction(func), "Decorator must be used on functions"
    signature = inspect.signature(func)
    type_hints = typing.get_type_hints(func)

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
