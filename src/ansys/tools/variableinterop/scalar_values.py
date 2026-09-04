# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Defines all scalar value implementations of the ``IVariableValue`` variable type."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
import locale
from typing import Any, Dict, Optional, Tuple, cast

import numpy as np
from overrides import overrides

from .exceptions import IncompatibleTypesException
from .isave_context import ISaveContext
from .ivariable_visitor import IVariableValueVisitor, T
from .utils.locale_utils import LocaleUtils
from .variable_type import VariableType
from .variable_value import IVariableValue


class BooleanValue(IVariableValue):
    """
    Stores a value as a ``BooleanValue`` variable type.

    This type is treated by Python as if it were any other Boolean type, such as
    ``numpy.bool\_`` or a built-in Boolean.
    """

    __slots__ = ("__value",)
    """
    Makes this type immutable.

    Unlike the other scalar types, this one is not a NumPy scalar subclass and keeps its
    payload in a Python attribute. Suppressing the ``__dict__`` is therefore not enough
    on its own, because a slot is still reassignable, so :meth:`__setattr__` and
    :meth:`__delattr__` are overridden to reject writes after construction.
    """

    @staticmethod
    def int64_to_bool(val: np.int64) -> bool:
        """Convert a NumPy int64 type to a Boolean value per interchange
        specifications."""
        return bool(val != 0)

    @staticmethod
    def int_to_bool(val: int) -> bool:
        """Convert an integer to a Boolean value per interchange specifications."""
        return bool(val != 0)

    @staticmethod
    def float_to_bool(val: float) -> bool:
        """Convert a float value to a Boolean value per interchange specifications."""
        return bool(val != 0.0)

    api_str_to_bool: Dict[str, bool] = {
        "yes": True,
        "y": True,
        "true": True,
        "no": False,
        "n": False,
        "false": False,
    }
    """Mapping of acceptable normalized values for API string conversion to their
    corresponding Boolean value."""

    @staticmethod
    def str_to_bool(val: str) -> bool:
        """Convert a string to a Boolean value per interchange specifications."""
        _value: str = str.lower(str.strip(val))
        if _value in BooleanValue.api_str_to_bool:
            return BooleanValue.api_str_to_bool[_value]
        else:
            try:
                _f_value: float = float(_value)
                return BooleanValue.float_to_bool(_f_value)
            except ValueError:
                pass
            raise ValueError

    def __init__(self, source: object = None):
        """
        Construct a ``BooleanValue`` variable type from various source types.

        Parameters
        ----------
        source : object
            Source type. Options are:

            - ``None``: Constructs a ``BooleanValue`` type set to ``False``.
            - ``bool`` or ``numpy.bool\_``: Constructs a ``BooleanValue`` type
              with the given Boolean value.
            - ``IVariableValue``: Constructs a ``BooleanValue`` type per the specification

            Any other option raises an exception.
        """
        value: np.bool_
        if source is None:
            value = np.False_
        elif isinstance(source, (bool, np.bool_)):
            value = np.bool_(source)
        elif isinstance(source, IVariableValue):
            from ansys.tools.variableinterop.scalar_value_conversion import to_boolean_value

            value = np.bool_(to_boolean_value(source))
        elif isinstance(
            source,
            (
                int,
                np.byte,
                np.ubyte,
                np.short,
                np.ushort,
                np.intc,
                np.uintc,
                np.int_,
                np.uint,
                np.longlong,
                np.ulonglong,
            ),
        ):
            value = np.bool_(source != 0)
        elif isinstance(source, (float, np.half, np.float16, np.single, np.double, np.longdouble)):
            value = np.bool_(source != 0.0)
        else:
            raise IncompatibleTypesException(type(source).__name__, VariableType.BOOLEAN)

        # Bypass the __setattr__ guard below, which rejects every other write.
        object.__setattr__(self, "_BooleanValue__value", value)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Reject attribute assignment, because this type is immutable.

        Raises
        ------
        AttributeError
            Always.
        """
        raise AttributeError(f"{type(self).__name__} objects are immutable.")

    def __delattr__(self, name: str) -> None:
        """
        Reject attribute deletion, because this type is immutable.

        Raises
        ------
        AttributeError
            Always.
        """
        raise AttributeError(f"{type(self).__name__} objects are immutable.")

    def __reduce__(self) -> Tuple[Any, ...]:
        """
        Reduce this value to a form that can be reconstructed.

        The default reduction for a class using ``__slots__`` restores state with
        ``setattr``, which :meth:`__setattr__` rejects. Reconstructing through the
        constructor instead keeps ``copy.deepcopy`` and ``pickle`` working.

        Returns
        -------
        Tuple[Any, ...]
            Callable and arguments needed to reconstruct this value.
        """
        return (type(self), (self.__value,))

    def __add__(self, other):
        """Magic method add."""
        if isinstance(other, BooleanValue):
            return self.__value.__add__(other.__value)
        else:
            return self.__value.__add__(other)

    def __and__(self, other):
        """Magic method and."""
        if isinstance(other, BooleanValue):
            return self.__value.__and__(other.__value)
        else:
            return self.__value.__and__(other)

    def __bool__(self):
        """Magic method bool."""
        return self.__value.__bool__()

    @overrides
    def __eq__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__eq__(other.__value)
        else:
            return self.__value.__eq__(other)

    def __floordiv__(self, other):
        """Magic method floordiv."""
        if isinstance(other, BooleanValue):
            return self.__value.__floordiv__(other.__value)
        else:
            return self.__value.__floordiv__(other)

    def __gt__(self, other):
        """Magic method gt."""
        if isinstance(other, BooleanValue):
            return self.__value.__gt__(other.__value)
        else:
            return self.__value.__gt__(other)

    def __ge__(self, other):
        """Magic method ge."""
        if isinstance(other, BooleanValue):
            return self.__value.__ge__(other.__value)
        else:
            return self.__value.__ge__(other)

    @overrides
    def __hash__(self):
        return self.__value.__hash__()

    def __lshift__(self, other):
        """Magic method lshift."""
        if isinstance(other, BooleanValue):
            return self.__value.__lshift__(other.__value)
        else:
            return self.__value.__lshift__(other)

    def __mod__(self, other):
        """Magic method mod."""
        if isinstance(other, BooleanValue):
            return self.__value.__mod__(other.__value)
        else:
            return self.__value.__mod__(other)

    def __mul__(self, other):
        """Magic method mul."""
        if isinstance(other, BooleanValue):
            return self.__value.__mul__(other.__value)
        else:
            return self.__value.__mul__(other)

    @overrides
    def __ne__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value.__ne__(other.__value)
        else:
            return self.__value.__ne__(other)

    def __or__(self, other):
        """Magic method or."""
        if isinstance(other, BooleanValue):
            return self.__value.__or__(other.__value)
        else:
            return self.__value.__or__(other)

    def __pow__(self, other):
        """Magic method pow."""
        if isinstance(other, BooleanValue):
            return self.__value.__pow__(other.__value)
        else:
            return self.__value.__pow__(other)

    def __rshift__(self, other):
        """Magic method rshift."""
        if isinstance(other, BooleanValue):
            return self.__value.__rshift__(other.__value)
        else:
            return self.__value.__rshift__(other)

    @overrides
    def __str__(self):
        return self.__value.__str__()

    def __truediv__(self, other):
        """Magic method truediv."""
        if isinstance(other, BooleanValue):
            return self.__value.__truediv__(other.__value)
        else:
            return self.__value.__truediv__(other)

    def __xor__(self, other):
        """Magic method xor."""
        if isinstance(other, BooleanValue):
            return self.__value.__xor__(other.__value)
        else:
            return self.__value.__xor__(other)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        return str(self)

    def to_real_value(self) -> RealValue:
        """
        Convert a given ``BooleanValue`` type to a ``RealValue`` type.

        ``True`` is converted to ``1.0``,  and ``False`` is converted to ``0.0``.

        Returns
        -------
        RealValue
            ``RealValue`` type with value representing the original ``BooleanValue`` type.
        """
        if self:
            return RealValue(1.0)
        else:
            return RealValue(0.0)

    @staticmethod
    def from_api_string(value: str) -> BooleanValue:
        """
        Convert an API string back into a ``BooleanValue`` type.

        The conversion is performed according to the type
        interoperability specifications.

        Values that are parseable as floating-point numbers
        are parsed in that manner and then converted to a ``BooleanValue`` type.

        Values that are non-numeric are checked to see if they match
        any of the following values.  The comparison is case-insensitive.

        - For ``True``: ``"true"``, ``"yes"``, or ``"y"``.
        - For ``False``: ``"false"``, ``"no"``, or ``"n"``.

        Values not interpretable result in a ``ValueError``.

        Parameters
        ----------
        value : str
            String to parse.

        Returns
        -------
        BooleanValue
            ``BooleanValue`` type parsed from the API string.
        """
        return BooleanValue(BooleanValue.str_to_bool(value))

    def to_integer_value(self) -> IntegerValue:
        """
        Convert a given ``BooleanValue`` type to an ``IntegerValue`` type.

        ``True`` is converted to ``1``, and ``False`` is converted to ``0``.

        Returns
        -------
        IntegerValue
            ``IntegerValue`` type with the value representing the original ``BooleanValue`` type.
        """
        if self:
            return IntegerValue(1)
        else:
            return IntegerValue(0)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        result: np.str_ = LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%s", self)
        )
        return result


class IntegerValue(np.int64, IVariableValue):
    """
    Stores a value as an ``IntegerValue`` variable type.

    In Python, the ``IntegerValue`` type is implemented by extending NumPy's int64 type.
    This means that they will decay naturally into ``numpy.int64`` objects when using NumPy's
    arithmetic operators. It also means that they inherit many of the NumPy behaviors,
    which may be slightly different from the behaviors specified in the variable interop
    standards. For example, when converting from real to integer, the value is
    floored instead of rounded. If you want the variable interop standard conversions,
    use the :meth:`to_real_value` method on this class to get a ``RealValue type``, which
    is rounded according to the variable interop standards and decomposes naturally into a
    ``numpy.float64`` type. Other conversions to analogous Python or NumPy types are identical
    between the variable interop standards and the default Python and NumPy behaviors.
    """

    __slots__ = ()
    """
    Makes this type immutable.

    The numeric payload already lives in the ``numpy.int64`` C struct, which exposes no
    mutation API, so suppressing the ``__dict__`` is all that is needed. This works only
    because :class:`IVariableValue` also declares ``__slots__``.
    """

    @overrides
    def __new__(cls, arg: Any = 0):
        """
        Create a new instance.

        Construction behaves differently for floating-point numbers and strings, depending on
        whether the argument is an ``IVariableValue`` type.

        ``IVariableValue`` instances are converted according to the standard interop rules.
        ``Real`` types are rounded. Values with a .5 in the tenths place are rounded away from zero.
        ``String`` types are converted to ``Real`` type and then rounded according to those rules.

        Parameters
        ----------
        arg : Any
            Argument to construct the instance from.
        """

        if isinstance(arg, IVariableValue):
            # Constructing from an IVariableValue is handled specially.
            if arg.variable_type == VariableType.REAL:
                # For IVariableValues representing a real, use a different rounding strategy.
                return super().__new__(
                    cls, Decimal(cast(RealValue, arg)).to_integral(ROUND_HALF_UP)
                )
            elif arg.variable_type == VariableType.STRING:
                # For IVariableValues representing a string, convert to RealValue to use
                # the alternate rounding strategy.
                return cls.__new__(cls, RealValue.from_api_string(cast(StringValue, arg)))
            elif arg.variable_type == VariableType.BOOLEAN:
                return super().__new__(cls, bool(arg))
            else:
                # For other IVariableValues, attempt to use the default conversions.
                return super().__new__(cls, arg)
        else:
            # For non-IVariableValues, use the superclass behavior.
            return super().__new__(cls, arg)

    def __deepcopy__(self, memo: Optional[Dict[int, Any]]) -> IntegerValue:
        """
        Get a deep copy of this value.

        Although this type is immutable, NumPy's own scalar deep copy is not usable
        here: before NumPy 2.5 it reduces to a bare ``numpy.int64``, discarding the
        subclass, and from NumPy 2.5 on it returns ``self``. Constructing a new
        instance keeps the result an ``IntegerValue`` on every supported version.

        Returns
        -------
        IntegerValue
            Deep copy of this value.
        """
        return IntegerValue(self)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_integer(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        return str(self)

    def to_real_value(self) -> RealValue:
        """
        Convert this ``IntegerValue`` type to a ``RealValue`` type.

        Because a ``RealValue`` type is a 64-bit floating point number, it has a 52-bit mantissa.
        That means that a portion of the range of 64-bit ``IntegerValue`` types cannot be completely
        accurately represented by ``RealValue`` types. This conversion is sometimes lossy for
        ``IntegerValue`` types of sufficient magnitude.

        Returns
        -------
        RealValue
            ``RealValue`` type with the same numeric value as the ``IntegerValue`` type.
        """
        return RealValue(self)

    @staticmethod
    def from_api_string(value: str) -> IntegerValue:
        """
        Create an ``IntegerValue`` type from an API string.

        Leading and trailing whitespace is ignored.
        Values that can be correctly parsed as floating-point numbers
        are parsed in that manner and then rounded to integers. When rounding,
        values with a 5 in the tenths place are rounded away from zero.

        Parameters
        ----------
        value : str
            String to parse.

        Returns
        -------
        IntegerValue
            ``IntegerValue`` type parsed from the API string.
        """
        if value is None:
            raise TypeError("Cannot create integer values from `None` type.")

        # Check to see if this looks like a float.
        if any(char == "E" or char == "e" or char == "." for char in value):
            # If so, convert it according to those rules.
            return RealValue(value).to_int_value()
        else:
            # Otherwise, parse as an int.
            return IntegerValue(value)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        result: np.str_ = LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%G", self)
        )
        return result


class RealValue(np.float64, IVariableValue):
    """
    Stores a value as a ``RealValue`` variable type.

    In Python, the ``RealValue`` type is implemented by extending NumPy's float64 type. This means
    that they decay naturally into ``numpy.float64`` objects when using NumPy's
    arithmetic operators. It also means that they inherit many of the NumPy behaviors,
    which may be slightly different from the behaviors specified in the variable interop
    standards. For example, when converting from real to integer, the value is
    floored instead of rounded. If you want the variable interop standard conversions,
    use the :meth:`to_int_value()` method to get an ``IntegerValue`` type with variable
    interop standard rounding (away from zero). The ``IntegerValue`` type decomposes naturally to
    ``numpy.int64`` objects.
    """

    __slots__ = ()
    """
    Makes this type immutable.

    The numeric payload already lives in the ``numpy.float64`` C struct, which exposes
    no mutation API, so suppressing the ``__dict__`` is all that is needed. This works
    only because :class:`IVariableValue` also declares ``__slots__``.
    """

    def __new__(cls, arg: Any = 0.0):
        """
        Create a new instance.

        Parameters
        ----------
        arg : Any
            Argument to construct the instance from.
        """
        if isinstance(arg, BooleanValue):
            return super().__new__(cls, bool(arg))
        else:
            return super().__new__(cls, arg)

    __CANONICAL_INF = "Infinity"
    """
    This is the canonical API string representation for infinity.

    The :meth:`from_api_string()` method accepts other values provided they are
    unambiguously infinity.
    """

    __CANONICAL_NEG_INF = "-Infinity"
    """
    This is the canonical API string representation for negative infinity.

    The :meth:`from_api_string()` method accepts other values provided they are
    unambiguously negative infinity.
    """

    __CANONICAL_NAN = "NaN"
    """
    This is the canonical API string representation for NaN.

    The :meth:`from_api_string` method accepts other values provided they are unambiguously NaN.
    """

    def __deepcopy__(self, memo: Optional[Dict[int, Any]]) -> RealValue:
        """
        Get a deep copy of this value.

        Although this type is immutable, NumPy's own scalar deep copy is not usable
        here: before NumPy 2.5 it reduces to a bare ``numpy.float64``, discarding the
        subclass, and from NumPy 2.5 on it returns ``self``. Constructing a new
        instance keeps the result a ``RealValue`` on every supported version.

        Returns
        -------
        RealValue
            Deep copy of this value.
        """
        return RealValue(self)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_real(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        return str(self)

    @overrides
    def __str__(self) -> str:
        if np.isnan(self):
            return RealValue.__CANONICAL_NAN
        if np.isposinf(self):
            return RealValue.__CANONICAL_INF
        if np.isneginf(self):
            return RealValue.__CANONICAL_NEG_INF
        return np.float64.__str__(self)

    @staticmethod
    def from_api_string(value: str) -> RealValue:
        """
        Convert an API string back into a ``RealValue`` type.

        Parameters
        ----------
        value : str
            String to convert.
        """
        return RealValue(float(value))

    def to_int_value(self) -> IntegerValue:
        """
        Convert this ``RealValue`` type to an ``IntegerValue`` type.

        The conversion is performed according to the type
        interoperability specifications. The value is rounded to the
        nearest integer, where values with a 5 in the tenths place are
        always rounded away from zero. (Note that this is different
        from the default Python rounding behavior.)

        Returns
        -------
        IntegerValue
            ``IntegerValue`` type that is the result of rounding this value
            to the nearest integer. (Values with a 5 in the tenths place
            are rounded away from zero.)
        """
        return IntegerValue(self)

    def to_boolean_value(self) -> BooleanValue:
        """
        Convert this ``RealValue``type to a ``BooleanValue`` type.

        The conversion is performed according to the type
        interoperability specifications. Any value other than exactly 0
        is considered to be ``True``.

        Returns
        -------
        BooleanValue
            ``BooleanValue`` type that is the result of converting the ``RealValue`` type.
        """
        return BooleanValue(self != 0)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        result: np.str_ = LocaleUtils.perform_safe_locale_action(
            locale_name, lambda: locale.format_string("%.15G", self)
        )
        return result


class StringValue(np.str_, IVariableValue):
    """
    Stores a value as an ``IVariableValue`` variable type.

    In Python, the ``IntegerValue`` type is implemented by extending NumPy's ``str\_`` type.
    This means that they decay naturally into ``numpy.str\_`` objects when used with other
    types of operators. It also means that they inherit many of the NumPy behaviors, which
    may be slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from string to integer, values parseable as floating-
    point numbers are rejected instead of parsed as such and then rounded. If you want the
    variable interop standard conversions, use the :meth:`from_api_string()` method on any given
    variable interop type to get an instance of that type, which should decompose
    naturally to the analogous NumPy type.
    """

    __slots__ = ()
    """
    Makes this type immutable.

    The string payload already lives in the ``numpy.str_`` C struct, which exposes no
    mutation API, so suppressing the ``__dict__`` is all that is needed. This works only
    because :class:`IVariableValue` also declares ``__slots__``.
    """

    def __init__(self, value=..., /):
        # Need to override init to make this not abstract, but np.str_ objects are immutable.
        pass

    def __deepcopy__(self, memo: Optional[Dict[int, Any]]) -> StringValue:
        """
        Get a deep copy of this value.

        Although this type is immutable, NumPy's own scalar deep copy is not usable
        here: before NumPy 2.5 it reduces to a bare ``numpy.str_``, discarding the
        subclass, and from NumPy 2.5 on it returns ``self``. Constructing a new
        instance keeps the result a ``StringValue`` on every supported version.

        Returns
        -------
        StringValue
            Deep copy of this value.
        """
        return StringValue(self)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_string(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        return str(self)

    @staticmethod
    def from_api_string(value: str) -> StringValue:
        """
        Convert an API string back to a string value.

        The string is stored exactly as specified. No escaping is performed
        as with the :meth:`from_formatted string` method.

        Parameters
        ----------
        value : str
            String to convert.
        """
        if value is None:
            raise TypeError("Cannot create a `StringValue` type from `None` type.")

        # No conversion / escaping when coming from API string
        return StringValue(value)

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        return self
