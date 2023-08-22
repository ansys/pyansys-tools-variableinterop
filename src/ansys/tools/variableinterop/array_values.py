"""Definition of all array value implementations of IVariableValue."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
import functools
import locale
from typing import Optional, TypeVar

import numpy
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


class BooleanArrayValue(CommonArrayValue[numpy.bool_]):
    """
    Array of boolean values.

    In Python BooleanArrayValue is implemented by extending NumPy's ndarray type. This
    means that they will decay naturally into numpy.ndarray objects when using numpy's
    array operators.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return numpy.array(values, dtype=numpy.bool_).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=numpy.bool_).view(cls)
        else:
            return numpy.zeros(shape=(), dtype=numpy.bool_).view(cls)

    @overrides
    def __eq__(self, other) -> bool:
        return numpy.array_equal(self, other)

    @overrides
    def clone(self) -> BooleanArrayValue:
        return numpy.copy(self).view(BooleanArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY

    def to_real_array_value(self) -> RealArrayValue:
        """
        Convert this value to a RealArrayValue.

        Returns
        -------
        RealArrayValue
            A RealArrayValue with the same values converted to real.
        """
        return self.astype(numpy.float64).view(RealArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        """
        Convert this value to an IntegerArrayValue.

        Returns
        -------
        IntegerArrayValue
            An IntegerArrayValue with the same values converted to int.
        """
        return self.astype(numpy.int64).view(IntegerArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        """
        Convert this value to an StringArrayValue.

        Returns
        -------
        StringArrayValue
            A StringArrayValue with the same values converted to string.
        """
        return self.astype(numpy.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: BooleanValue(elem.tolist()).to_api_string()
        )
        return api_string

    @staticmethod
    def from_api_string(value: str) -> BooleanArrayValue:
        """
        Convert API formatted string to an BooleanArrayValue value.

        Parameters
        ----------
        value : str
            API string to be parsed.

        Returns
        -------
        BooleanArrayValue
            Result of a parse as BooleanArrayValue object.
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


class IntegerArrayValue(CommonArrayValue[numpy.int64]):
    """
    Array of integer values.

    In Python IntegerArrayValue is implemented by extending NumPy's ndarray type. This
    means that they will decay naturally into numpy.ndarray objects when using numpy's
    array operators. It also means that they inherit many of the numpy behaviors, which
    may be slightly different from the behaviors specified in the variable interop
    standards. For example, when converting from real to integer, the value will be
    floored instead of rounded. If you want the variable interop standard conversions,
    call to_integer_array_value on the RealArrayValue and use the resulting
    IntegerArrayValue as you would a NumPy ndarray of int64 values.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return numpy.array(values, dtype=numpy.int64).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=numpy.int64).view(cls)
        else:
            return numpy.zeros(shape=(), dtype=numpy.int64).view(cls)

    @overrides
    def __eq__(self, other):
        return numpy.array_equal(self, other)

    @overrides
    def clone(self) -> IntegerArrayValue:
        return numpy.copy(self).view(IntegerArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY

    def to_boolean_array_value(self) -> BooleanArrayValue:
        """
        Convert this value to a BooleanArrayValue.

        Returns
        -------
        BooleanArrayValue
            A BooleanArrayValue with the same values converted to bool.
        """
        return numpy.vectorize(numpy.bool_)(self).view(BooleanArrayValue)

    def to_real_array_value(self) -> RealArrayValue:
        """
        Convert this value to a RealArrayValue.

        Returns
        -------
        RealArrayValue
            A RealArrayValue with the same values converted to real.
        """
        return self.astype(numpy.float64).view(RealArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        """
        Convert this value to an StringArrayValue.

        Returns
        -------
        StringArrayValue
            A StringArrayValue with the same values converted to string.
        """
        return self.astype(numpy.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: IntegerValue(elem).to_api_string()
        )
        return api_string

    @staticmethod
    def from_api_string(value: str) -> IntegerArrayValue:
        """
        Convert API formatted string to an IntegerArrayValue value.

        Parameters
        ----------
        value : str
            API string to be parsed.

        Returns
        -------
        IntegerArrayValue
            Result of a parse as IntegerArrayValue object.
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


class RealArrayValue(CommonArrayValue[numpy.float64]):
    """
    Array of real values.

    In Python RealArrayValue is implemented by extending NumPy's ndarray type. This
    means that they will decay naturally into numpy.ndarray objects when using numpy's
    array operators. It also means that they inherit many of the numpy behaviors, which
    may be slightly different from the behaviors specified in the variable interop
    standards. For example, when converting from real to integer, the value will be
    floored instead of rounded. If you want the variable interop standard conversions,
    call to_integer_array_value on the RealArrayValue and use the resulting
    IntegerArrayValue as you would a NumPy ndarray of int64 values.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return numpy.array(values, dtype=numpy.float64).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=numpy.float64).view(cls)
        else:
            return numpy.zeros(shape=(), dtype=numpy.float64).view(cls)

    @overrides
    def __eq__(self, other: RealArrayValue) -> bool:
        return numpy.array_equal(self, other)

    @overrides
    def clone(self) -> RealArrayValue:
        return numpy.copy(self).view(RealArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY

    def to_boolean_array_value(self) -> BooleanArrayValue:
        """
        Convert this value to a BooleanArrayValue.

        Returns
        -------
        BooleanArrayValue
            A BooleanArrayValue with the same values converted to bool.
        """
        return numpy.vectorize(numpy.bool_)(self).view(BooleanArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        """
        Convert this value to an IntegerArrayValue.

        Returns
        -------
        IntegerArrayValue
            An IntegerArrayValue with the same values converted to int.
        """

        def away_from_zero(x: numpy.float64) -> numpy.int64:
            return numpy.int64(Decimal(x).to_integral(ROUND_HALF_UP))

        return numpy.vectorize(away_from_zero)(self).astype(numpy.int64).view(IntegerArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        """
        Convert this value to an StringArrayValue.

        Returns
        -------
        StringArrayValue
            A StringArrayValue with the same values converted to string.
        """
        return self.astype(numpy.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self, lambda elem: RealValue(elem).to_api_string()
        )
        return api_string

    @staticmethod
    def from_api_string(value: str) -> RealArrayValue:
        """
        Convert API formatted string to an RealArrayValue value.

        Parameters
        ----------
        value : str
            API string to be parsed.

        Returns
        -------
        RealArrayValue
            Result of a parse as RealArrayValue object.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: RealArrayValue(values=val),
            lambda val: RealValue.from_api_string(val),
        )

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        def parse_real_element(elem: numpy.float64) -> str:
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


class StringArrayValue(CommonArrayValue[numpy.str_]):
    """
    Array of string values.

    In Python StringArrayValue is implemented by extending NumPy's ndarray type. This
    means that they will decay naturally into numpy.ndarray objects when using numpy's
    array operators.
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values is not None:
            return numpy.array(values, dtype=numpy.str_).view(cls)
        elif shape_ is not None:
            return super().__new__(cls, shape=shape_, dtype=numpy.str_).view(cls)
        else:
            return numpy.zeros(shape=(), dtype=numpy.str_).view(cls)

    @overrides
    def __eq__(self, other):
        return numpy.array_equal(self, other)

    @overrides
    def clone(self) -> StringArrayValue:
        return numpy.copy(self).view(StringArrayValue)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY

    def to_real_array_value(self) -> RealArrayValue:
        """
        Convert this value to a RealArrayValue.

        Returns
        -------
        A RealArrayValue with the same values converted to real.
        """
        return self.astype(numpy.float64).view(RealArrayValue)

    def to_boolean_array_value(self) -> BooleanArrayValue:
        """
        Convert this value to a BooleanArrayValue.

        Returns
        -------
        BooleanArrayValue
            A BooleanArrayValue with the same values converted to bool.
        """
        return numpy.vectorize(BooleanValue.str_to_bool)(self).view(BooleanArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        """
        Convert this value to an IntegerArrayValue.

        Returns
        -------
        IntegerArrayValue
            An IntegerArrayValue with the same values converted to int.
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
        Convert API formatted string to an StringArrayValue value.

        Parameters
        ----------
        value : str
            API string to be parsed.

        Returns
        -------
        StringArrayValue
            Result of a parse as StringArrayValue object.
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
