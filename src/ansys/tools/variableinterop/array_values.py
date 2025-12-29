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
"""Defines all array value implementations of the ``IVariableValue`` variable type."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
import functools
import locale
from typing import Optional, TypeVar

import numpy as np
from numpy.typing import ArrayLike
from overrides import overrides

from .isave_context import ISaveContext
from .ivariable_visitor import IVariableValueVisitor
from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from .utils.array_to_from_string_util import ArrayToFromStringUtil
from .utils.locale_utils import LocaleUtils
from .utils.string_escaping import escape_string, unescape_string
from .variable_type import VariableType
from .variable_value import CommonArrayValue

T = TypeVar("T")


class BooleanArrayValue(CommonArrayValue[np.bool_]):
    """
    Stores a value as a ``BooleanArrayValue`` variable type.

    In Python, a ``BooleanArrayValue`` type is implemented by extending NumPy's ``ndarray`` type.
    This means that they decay naturally into ``numpy.ndarray`` objects when using NumPy's
    array operators.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return np.array(values, dtype=np.bool_).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=np.bool_).view(cls)
        else:
            return np.zeros(shape=(), dtype=np.bool_).view(cls)

    @overrides
    def __eq__(self, other) -> bool:
        return np.array_equal(self, other)

    @overrides
    def clone(self) -> BooleanArrayValue:
        return np.copy(self).view(BooleanArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY

    def to_real_array_value(self) -> RealArrayValue:
        """
        Convert this value to a ``RealArrayValue`` type.

        Returns
        -------
        RealArrayValue
            ``RealArrayValue`` type with the same values converted to real numbers.
        """
        return self.astype(np.float64).view(RealArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        """
        Convert this value to an ``IntegerArrayValue`` type.

        Returns
        -------
        IntegerArrayValue
           ``IntegerArrayValue`` type with the same values converted to integers.
        """
        return self.astype(np.int64).view(IntegerArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        """
        Convert this value to a ``StringArrayValue`` type.

        Returns
        -------
        StringArrayValue
            ``StringArrayValue`` type with the same values converted to strings.
        """
        return self.astype(np.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: BooleanValue(elem.tolist()).to_api_string()
        )
        return api_string

    @staticmethod
    def from_api_string(value: str) -> BooleanArrayValue:
        """
        Convert an API-formatted string to a ``BooleanArrayValue`` type.

        Parameters
        ----------
        value : str
            API string to parse.

        Returns
        -------
        BooleanArrayValue
            Result of parsing the ``BooleanArrayValue`` type.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: BooleanArrayValue(values=val),
            lambda val: BooleanValue.from_api_string(val),
        )

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: BooleanValue(elem.tolist()).to_display_string(locale_name)
        )
        return api_string
        pass


class IntegerArrayValue(CommonArrayValue[np.int64]):
    """
    Stores a value as an ``IntegerArrayValue`` variable type.

    In Python, the ``IntegerArrayValue`` type is implemented by extending NumPy's ``ndarray`` type.
    This means that they decay naturally into ``numpy.ndarray`` objects when using NumPy's
    array operators. It also means that they inherit many of the NumPy behaviors, which
    may be slightly different from the behaviors specified in the variable interop
    standards. For example, when converting from real to integer, the value is
    floored instead of rounded. If you want the variable interop standard conversions,
    call the ``to_integer_array_value`` method on the ``RealArrayValue`` type and use the resulting
    ``IntegerArrayValue`` type as you would a NumPy ``ndarray`` of int64 values.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return np.array(values, dtype=np.int64).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=np.int64).view(cls)
        else:
            return np.zeros(shape=(), dtype=np.int64).view(cls)

    @overrides
    def __eq__(self, other):
        return np.array_equal(self, other)

    @overrides
    def clone(self) -> IntegerArrayValue:
        return np.copy(self).view(IntegerArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY

    def to_boolean_array_value(self) -> BooleanArrayValue:
        """
        Convert this value to a ``BooleanArrayValue`` type.

        Returns
        -------
        BooleanArrayValue
            ``BooleanArrayValue`` type with the same values converted to Boolean values.
        """
        return np.vectorize(np.bool_)(self).view(BooleanArrayValue)

    def to_real_array_value(self) -> RealArrayValue:
        """
        Convert this value to a ``RealArrayValue`` type.

        Returns
        -------
        RealArrayValue
            ``RealArrayValue`` type with the same values converted to real values.
        """
        return self.astype(np.float64).view(RealArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        """
        Convert this value to a ``StringArrayValue`` type.

        Returns
        -------
        StringArrayValue
            ``StringArrayValue`` type converted to an array of strings.
        """
        return self.astype(np.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: IntegerValue(elem).to_api_string()
        )
        return api_string

    @staticmethod
    def from_api_string(value: str) -> IntegerArrayValue:
        """
        Convert an API-formatted string to an ``IntegerArrayValue`` type.

        Parameters
        ----------
        value : str
            API string to parse.

        Returns
        -------
        IntegerArrayValue
            Result of parsing the ``IntegerArrayValue`` type.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: IntegerArrayValue(values=val),
            lambda val: IntegerValue.from_api_string(val),
        )

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: IntegerValue(elem).to_display_string(locale_name)
        )
        return api_string


class RealArrayValue(CommonArrayValue[np.float64]):
    """
    Stores a value as a ``RealArrayValue`` variable type.

    In Python, the ``RealArrayValue`` type is implemented by extending NumPy's ``ndarray`` type.
    This means that they decay naturally into ``numpy.ndarray`` objects when using NumPy's
    array operators. It also means that they inherit many of the NumPy behaviors, which
    may be slightly different from the behaviors specified in the variable interop
    standards. For example, when converting from real to integer, the value is
    floored instead of rounded. If you want the variable interop standard conversions,
    call the ``to_integer_array_value`` method on the ``RealArrayValue`` type and use the resulting
    ``IntegerArrayValue`` type as you would a NumPy ``ndarray`` of int64 values.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return np.array(values, dtype=np.float64).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=np.float64).view(cls)
        else:
            return np.zeros(shape=(), dtype=np.float64).view(cls)

    @overrides
    def __eq__(self, other: RealArrayValue) -> bool:
        return np.array_equal(self, other)

    @overrides
    def clone(self) -> RealArrayValue:
        return np.copy(self).view(RealArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY

    def to_boolean_array_value(self) -> BooleanArrayValue:
        """
        Convert this value to a ``BooleanArrayValue`` type.

        Returns
        -------
        BooleanArrayValue
            ``BooleanArrayValue`` type with the same values converted to Boolean values.
        """
        return np.vectorize(np.bool_)(self).view(BooleanArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        """
        Convert this value to an ``IntegerArrayValue`` type.

        Returns
        -------
        IntegerArrayValue
            ``IntegerArrayValue`` type with the same values converted to integers.
        """

        def away_from_zero(x: np.float64) -> np.int64:
            return np.int64(Decimal(x).to_integral(ROUND_HALF_UP))

        return np.vectorize(away_from_zero)(self).astype(np.int64).view(IntegerArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        """
        Convert the value to a ``StringArrayValue`` type.

        Returns
        -------
        StringArrayValue
            ``StringArrayValue`` type with the same value converted to strings.
        """
        return self.astype(np.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: RealValue(elem).to_api_string()
        )
        return api_string

    @staticmethod
    def from_api_string(value: str) -> RealArrayValue:
        """
        Convert an API-formatted string to the ``RealArrayValue`` type.

        Parameters
        ----------
        value : str
            API string to parse.

        Returns
        -------
        RealArrayValue
            Result of parsing the ``RealArrayValue`` type.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: RealArrayValue(values=val),
            lambda val: RealValue.from_api_string(val),
        )

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        def parse_real_element(elem: np.float64) -> str:
            value: str = RealValue(elem).to_display_string(locale_name)

            # Old form arrays (without quotes around each item) do not work for languages where ','
            # is the decimal separator. Use new form for those languages.
            def escape_if_needed(val: str) -> str:
                if locale.localeconv()["decimal_point"] == ",":
                    val = '"' + val + '"'
                return val

            value = LocaleUtils.perform_safe_locale_action(
                locale_name, functools.partial(escape_if_needed, val=value)
            )
            return value

        api_string: str = ArrayToFromStringUtil.value_to_string(self, parse_real_element)
        return api_string


class StringArrayValue(CommonArrayValue[np.str_]):
    """
    Stores a value as a ``StringArrayValue`` variable type.

    In Python, the ``StringArrayValue`` type is implemented by extending NumPy's ``ndarray`` type.
    This means that they decay naturally into ``numpy.ndarray`` objects when using NumPy's
    array operators.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return np.array(values, dtype=np.str_).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=np.str_).view(cls)
        else:
            return np.zeros(shape=(), dtype=np.str_).view(cls)

    @overrides
    def __eq__(self, other):
        return np.array_equal(self, other)

    @overrides
    def clone(self) -> StringArrayValue:
        return np.copy(self).view(StringArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY

    def to_real_array_value(self) -> RealArrayValue:
        """
        Convert the value to a ``RealArrayValue`` type.

        Returns
        -------
        RealArrayValue
            ``RealArrayValue`` type with the same values converted to real numbers.
        """
        return self.astype(np.float64).view(RealArrayValue)

    def to_boolean_array_value(self) -> BooleanArrayValue:
        """
        Convert the value to a ``BooleanArrayValue`` type.

        Returns
        -------
        BooleanArrayValue
            ``BooleanArrayValue`` type with the same values converted to Boolean values.
        """
        return np.vectorize(BooleanValue.str_to_bool)(self).view(BooleanArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        """
        Convert the value to an ``IntegerArrayValue`` type.

        Returns
        -------
        IntegerArrayValue
            ``IntegerArrayValue`` type with the same values converted to integers.
        """
        return self.to_real_array_value().to_integer_array_value()

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: '"' + escape_string(StringValue(elem).to_api_string()) + '"'
        )
        return api_string

    @staticmethod
    def from_api_string(value: str) -> StringArrayValue:
        """
        Convert an API-formatted string to a ``StringArrayValue`` type.

        Parameters
        ----------
        value : str
            API string to parse.

        Returns
        -------
        StringArrayValue
            Result of parsing the ``StringArrayValue`` type.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: StringArrayValue(values=val),
            lambda val: StringValue.from_api_string(unescape_string(val)),
        )

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: '"' + StringValue(elem).to_display_string(locale_name) + '"'
        )
        return api_string
