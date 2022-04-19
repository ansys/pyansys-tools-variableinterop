"""This module contains utilities for coercing arbitrary Python objects \
into the appropriate IVariableValue type."""
from __future__ import annotations

import functools
import inspect
import typing
from typing import Any

import numpy as np

import ansys.common.variableinterop.scalar_values as scalar_values
import ansys.common.variableinterop.variable_value as variable_value

# A dictionary that maps source types to what variableinterop type it should be mapped to
TYPE_MAPPINGS = {
    int: scalar_values.IntegerValue,
    np.integer: scalar_values.IntegerValue,
    float: scalar_values.RealValue,
    np.inexact: scalar_values.RealValue,
    bool: scalar_values.BooleanValue,
    np.bool_: scalar_values.BooleanValue,
    str: scalar_values.StringValue,
    np.str_: scalar_values.StringValue
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

    if arg_type == variable_value.IVariableValue:
        for cls in type(arg).__mro__:
            if cls in TYPE_MAPPINGS:
                return TYPE_MAPPINGS[cls](arg)
        # TODO: Consider passing in more context for the exception
        # TODO: types come out to
        #  <class 'ansys.common.variableinterop.variable_value.IVariableValue'>.
        #  Can that be simplified?
        raise TypeError(f"Type {type(arg)} cannot be converted to {variable_value.IVariableValue}")

    # TODO: This probably doesn't have all the right semantics for our set of implicit
    #  type conversions
    if issubclass(arg_type, variable_value.IVariableValue):
        if arg is None:
            raise TypeError(f"Type {type(arg)} cannot be converted to {arg_type}")
        # ignore because mypy does not know about subclass constructors
        return arg_type(arg)  # type: ignore

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
