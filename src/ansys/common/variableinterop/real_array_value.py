from __future__ import annotations

import functools
import locale
from typing import TypeVar

import numpy as np
from numpy.typing import ArrayLike
from overrides import overrides

from ansys.common.variableinterop.array_to_from_string_util import ArrayToFromStringUtil
import ansys.common.variableinterop.boolean_array_value as boolean_array_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
from ansys.common.variableinterop.locale_utils import LocaleUtils
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.variable_type as variable_type
from .variable_value import CommonArrayValue

T = TypeVar("T")


class RealArrayValue(CommonArrayValue[np.float64]):
    """Array of real values.

    In Python RealArrayValue is implemented by extending NumPy's ndarray type. This means that
    they will decay naturally into numpy.ndarray objects when using numpy's array
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def __new__(cls, shape_: ArrayLike = None, values: ArrayLike = None):
        if values:
            return np.array(values, dtype=np.float64).view(cls)
        return super().__new__(cls, shape=shape_, dtype=np.float64)

    def __eq__(self, other: object) -> bool:
        return np.array_equal(self, other)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.REAL_ARRAY

    def to_boolean_array_value(self):
        return np.vectorize(np.bool_)(self).view(boolean_array_value.BooleanArrayValue)

    # TODO: full implementation

    @overrides
    def to_api_string(self) -> str:
        raise NotImplementedError

    @staticmethod
    def from_api_string(value: str) -> None:
        raise NotImplementedError

    # TODO: overrides when right branch merged over
    def to_formatted_string(self, locale_name: str) -> str:
        def parse_real_element(elem: np.float64) -> str:
            value: str = real_value.RealValue(elem).to_formatted_string(locale_name)

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

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
