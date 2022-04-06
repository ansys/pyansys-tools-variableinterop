"""Definition of RealValue."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

import numpy as np

import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType


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

    # equality definition here

    # hashcode definition here

    def accept(
            self, visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        return visitor.visit_real(self)

    def variable_type(self) -> VariableType:
        return VariableType.REAL

    def to_api_string(self) -> str:
        raise NotImplementedError

    @staticmethod
    def from_api_string(value: str) -> RealValue:
        """
        Convert an API string back into a value.

        Parameters
        ----------
        value
        The string to convert.
        """
        raise NotImplementedError

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

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
