"""Definition of RealValue."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import TypeVar

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


class RealValue(np.float64, variable_value.IVariableValue):
    """
    Wrapper around a real value.

    In Python RealValue is implemented by extending NumPy's float64 type. This means that
    they will decay naturally into numpy.float64 objects when using numpy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

    # equality definition here

    # hashcode definition here

    __CANONICAL_INF = "Infinity"
    """
    This is the canonical API string representation for infinity.

    from_api_string will accept other values provided they are
    unambiguously infinity.
    """

    __CANONICAL_NEG_INF = "-Infinity"
    """
    This is the canonical API string representation for negative infinity.

    from_api_string will accept other values provided they are
    unambiguously negative infinity.
    """

    __CANONICAL_NAN = "NaN"
    """
    This is the canonical API string representation for NaN.

    from_api_string will accept other values provided they are
    unambiguously NaN.
    """

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_real(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.REAL

    @overrides
    def to_api_string(self) -> str:
        return str(self)

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
        Convert an API string back into a value.

        Parameters
        ----------
        value
        The string to convert.
        """
        return RealValue(float(value))

    def to_int_value(self) -> integer_value.IntegerValue:
        """
        Convert this RealValue to an IntegerValue.

        The conversion is performed according to the type
        interoperability specifications. The value is rounded to the
        nearest integer, where values with a 5 in the tenths place are
        always rounded away from zero. (Note that this is different
        from the "default" Python rounding behavior.)

        Returns
        -------
        An IntegerValue that is the result of rounding this value
        to the nearest integer (values with a 5 in the tenths place
        are rounded away from zero).
        """
        return integer_value.IntegerValue(Decimal(self).to_integral(ROUND_HALF_UP))

    def to_boolean_value(self) -> boolean_value.BooleanValue:
        """
        Convert this RealValue to a BooleanValue.

        The conversion is performed according to the type
        interoperability specifications. Any value other than exactly 0
        is considered to be 'True'.
        Returns
        -------
        A BooleanValue that is the result of converting this RealValue.
        """
        return boolean_value.BooleanValue(self != 0)

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
