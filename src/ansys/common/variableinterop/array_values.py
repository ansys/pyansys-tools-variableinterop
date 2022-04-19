"""Definition of all array value implementations of IVariableValue."""
from __future__ import annotations

import functools
import locale
from typing import TypeVar

import numpy as np
from numpy.typing import ArrayLike
from overrides import overrides

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
from ansys.common.variableinterop.utils.array_to_from_string_util import ArrayToFromStringUtil
from ansys.common.variableinterop.utils.locale_utils import LocaleUtils
import ansys.common.variableinterop.variable_type as variable_type

from .variable_value import CommonArrayValue

T = TypeVar("T")


class BooleanArrayValue(CommonArrayValue[np.bool_]):
    """Array of boolean values.

    In Python BooleanArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.bool_).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.bool_)

    @overrides
    def __eq__(self, other) -> bool:
        return np.array_equal(self, other)

    @overrides
    def clone(self) -> BooleanArrayValue:
        return np.copy(self).view(BooleanArrayValue)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property   # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN_ARRAY

    def to_real_array_value(self) -> RealArrayValue:
        return self.astype(np.float64).view(RealArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        return self.astype(np.int64).view(IntegerArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        return self.astype(np.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem: BooleanValue(elem.tolist()).to_api_string())
        return api_string

    @staticmethod
    def from_api_string(value: str) -> BooleanArrayValue:
        """Convert API formatted string to an BooleanArrayValue value.

        Parameters
        ----------
        value : str API string to be parsed.

        Returns
        -------
        Result of a parse as BooleanArrayValue object.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: BooleanArrayValue(values=val),
            lambda val: BooleanValue.from_api_string(val))

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem: BooleanValue(elem.tolist()).to_display_string(locale_name))
        return api_string
        pass


class IntegerArrayValue(CommonArrayValue[np.int64]):
    """Array of integer values.

    In Python IntegerArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.int64).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.int64)

    @overrides
    def __eq__(self, other):
        return np.array_equal(self, other)

    def clone(self) -> IntegerArrayValue:
        return np.copy(self).view(IntegerArrayValue)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.INTEGER_ARRAY

    def to_boolean_array_value(self):
        return np.vectorize(np.bool_)(self).view(BooleanArrayValue)

    def to_real_array_value(self) -> RealArrayValue:
        return self.astype(np.float64).view(RealArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        return self.astype(np.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem: IntegerValue(elem).to_api_string())
        return api_string

    @staticmethod
    def from_api_string(value: str) -> IntegerArrayValue:
        """Convert API formatted string to an IntegerArrayValue value.

        Parameters
        ----------
        value : str API string to be parsed.

        Returns
        -------
        Result of a parse as IntegerArrayValue object.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: IntegerArrayValue(values=val),
            lambda val: IntegerValue.from_api_string(val))

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem: IntegerValue(elem).to_display_string(locale_name))
        return api_string


class RealArrayValue(CommonArrayValue[np.float64]):
    """Array of real values.

    In Python RealArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.float64).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.float64)

    @overrides
    def __eq__(self, other: RealArrayValue) -> bool:
        return np.array_equal(self, other)

    @overrides
    def clone(self) -> RealArrayValue:
        return np.copy(self).view(RealArrayValue)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.REAL_ARRAY

    def to_boolean_array_value(self):
        return np.vectorize(np.bool_)(self).view(BooleanArrayValue)

    def to_integer_array_value(self):
        def away_from_zero(x: np.float64) -> np.int64:
            f = np.floor if x < 0 else np.ceil
            return np.int64(f(x))

        return np.vectorize(away_from_zero)(self).astype(np.int64) \
            .view(IntegerArrayValue)

    def to_string_array_value(self) -> StringArrayValue:
        return self.astype(np.str_).view(StringArrayValue)

    @overrides
    def to_api_string(self) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem: RealValue(elem).to_api_string())
        return api_string

    @staticmethod
    def from_api_string(value: str) -> RealArrayValue:
        """Convert API formatted string to an RealArrayValue value.

        Parameters
        ----------
        value : str API string to be parsed.

        Returns
        -------
        Result of a parse as RealArrayValue object.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: RealArrayValue(values=val),
            lambda val: RealValue.from_api_string(val))

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        def parse_real_element(elem: np.float64) -> str:
            value: str = RealValue(elem).to_display_string(locale_name)

            # Old form arrays (without quotes around each item) do not work for languages where ','
            # is the decimal separator. Use new form for those languages.
            def escape_if_needed(val: str) -> str:
                if locale.localeconv()["decimal_point"] == ',':
                    val = "\"" + val + "\""
                return val

            value = LocaleUtils.perform_safe_locale_action(
                locale_name,
                functools.partial(escape_if_needed, val=value))
            return value

        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            parse_real_element)
        return api_string


class StringArrayValue(CommonArrayValue[np.str_]):
    """Array of string values.

    In Python StringArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    @overrides
    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.str_).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.str_)

    def __eq__(self, other):
        return np.array_equal(self, other)

    @overrides
    def clone(self) -> StringArrayValue:
        return np.copy(self).view(StringArrayValue)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.STRING_ARRAY

    def to_real_array_value(self) -> RealArrayValue:
        return self.astype(np.float64).view(RealArrayValue)

    def to_boolean_array_value(self) -> BooleanArrayValue:
        # TODO: use BooleanValue.to_api_string() when that is available
        def as_bool(value: str) -> np.bool_:
            normalized: str = str.lower(str.strip(value))
            if normalized in ("yes", "y", "true"):
                return np.bool_(True)
            elif normalized in ("no", "n", "false"):
                return np.bool_(False)
            else:
                # Try to parse as real then convert to boolean
                return np.bool_(np.float64(value))

        return np.vectorize(as_bool)(self).view(BooleanArrayValue)

    def to_integer_array_value(self) -> IntegerArrayValue:
        return self.to_real_array_value().to_integer_array_value()

    @overrides
    def to_api_string(self) -> str:
        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem: "\"" + StringValue(elem).to_api_string() + "\"")
        return api_string

    @staticmethod
    def from_api_string(value: str) -> StringArrayValue:
        """Convert API formatted string to an StringArrayValue value.

        Parameters
        ----------
        value : str API string to be parsed.

        Returns
        -------
        Result of a parse as StringArrayValue object.
        """
        return ArrayToFromStringUtil.string_to_value(
            value,
            lambda val: StringArrayValue(values=val),
            lambda val: StringValue.from_api_string(val))

    @overrides
    def to_display_string(self, locale_name: str) -> str:

        api_string: str = ArrayToFromStringUtil.value_to_string(
            self,
            lambda elem:
            "\"" + StringValue(elem).to_display_string(locale_name) + "\"")
        return api_string
