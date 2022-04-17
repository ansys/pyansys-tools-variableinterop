"""This module contains utilities for coercing arbitrary Python objects \
into the appropriate IVariableValue type."""
from __future__ import annotations

import functools
import inspect
import typing
from typing import Any

import numpy as np

from .boolean_value import BooleanValue
from .integer_value import IntegerValue
from .real_value import RealValue
from .string_value import StringValue
from .variable_value import IVariableValue

# A dictionary that maps source types to what variableinterop type it should be mapped to
TYPE_MAPPINGS = {
    int: IntegerValue,
    np.integer: IntegerValue,
    float: RealValue,
    np.inexact: RealValue,
    bool: BooleanValue,
    np.bool_: BooleanValue,
    str: StringValue,
    np.str_: StringValue
}
_ALLOWED_SPECIFIC_IMPLICIT_COERCE = {
    IntegerValue: [int, np.integer, bool, np.bool_, BooleanValue],
    RealValue: [float, np.inexact, bool, np.bool_, BooleanValue],
    BooleanValue: [bool, np.bool_,
                   float, np.inexact, RealValue,
                   int, np.integer, IntegerValue],
    StringValue: [int, np.integer, IntegerValue,
                  bool, np.bool_, BooleanValue,
                  float, np.inexact, RealValue,
                  str, np.str_, StringValue],
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


def _specific_implicit_coerce_allowed(target_arg_type: type, actual_arg_type: type) -> bool:
    """
    Check whether implicit coercion from a given type
    to a given type is allowed or not.

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

    if target_arg_type in _ALLOWED_SPECIFIC_IMPLICIT_COERCE:
        return any(issubclass(actual_arg_type, allowed_coerce_type)
                   for allowed_coerce_type in _ALLOWED_SPECIFIC_IMPLICIT_COERCE[target_arg_type])
    else:
        return False


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

    if arg_type == IVariableValue:
        for cls in type(arg).__mro__:
            if cls in TYPE_MAPPINGS:
                return TYPE_MAPPINGS[cls](arg)
        # TODO: Consider passing in more context for the exception
        # TODO: types come out to
        #  <class 'ansys.common.variableinterop.variable_value.IVariableValue'>.
        #  Can that be simplified?
        raise TypeError(f"Type {type(arg)} cannot be converted to {IVariableValue}")

    # TODO: This probably doesn't have all the right semantics for our set of implicit
    #  type conversions
    if issubclass(arg_type, IVariableValue):
        if arg is None:
            raise TypeError(f"Type {type(arg)} cannot be converted to {arg_type}")
        # Check if the proposed conversion is even allowed:
        if _specific_implicit_coerce_allowed(arg_type, type(arg)):
            return arg_type(arg)
        else:
            raise TypeError(f"Type {type(arg)} cannot be implicitly converted to {arg_type}.")

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
