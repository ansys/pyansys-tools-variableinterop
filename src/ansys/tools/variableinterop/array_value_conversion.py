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
"""Defines array value visitors."""
import numpy as np
from overrides import overrides

from ansys.tools.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
import ansys.tools.variableinterop.exceptions as exceptions
from ansys.tools.variableinterop.file_array_value import FileArrayValue
from ansys.tools.variableinterop.file_value import FileValue
import ansys.tools.variableinterop.ivariable_visitor as ivariable_visitor
from ansys.tools.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
import ansys.tools.variableinterop.variable_type as variable_type
import ansys.tools.variableinterop.variable_value as variable_value


class __ToBooleanArrayVisitor(ivariable_visitor.IVariableValueVisitor[BooleanArrayValue]):
    """Visits variable values and converts to a ``BooleanArrayValue`` type when
    possible."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY
        )

    @overrides
    def visit_real(self, value: RealValue) -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY
        )

    @overrides
    def visit_boolean(self, value: BooleanValue) -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY
        )

    @overrides
    def visit_string(self, value: StringValue) -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY
        )

    @overrides
    def visit_file(self, value: FileValue) -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY
        )

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> BooleanArrayValue:
        return value.to_boolean_array_value()

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> BooleanArrayValue:
        return value.to_boolean_array_value()

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> BooleanArrayValue:
        return np.copy(value).view(BooleanArrayValue)

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> BooleanArrayValue:
        return value.to_boolean_array_value()

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> BooleanArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.BOOLEAN_ARRAY
        )


def to_boolean_array_value(other: variable_value.IVariableValue) -> BooleanArrayValue:
    """
    Convert the given value to a ``BooleanArrayValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises ``IncompatibleTypesException``).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to a ``BooleanArrayValue`` type.

    Returns
    -------
    BooleanArrayValue
        Value as a ``BooleanArrayValue`` type.
    """
    return other.accept(__ToBooleanArrayVisitor())


class __ToIntegerArrayVisitor(ivariable_visitor.IVariableValueVisitor[IntegerArrayValue]):
    """Visits variable values and converts them to ``IntegerArrayValue`` types when
    possible."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY
        )

    @overrides
    def visit_real(self, value: RealValue) -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY
        )

    @overrides
    def visit_boolean(self, value: BooleanValue) -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY
        )

    @overrides
    def visit_string(self, value: StringValue) -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY
        )

    @overrides
    def visit_file(self, value: FileValue) -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY
        )

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> IntegerArrayValue:
        return np.copy(value).view(IntegerArrayValue)

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> IntegerArrayValue:
        return value.to_integer_array_value()

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> IntegerArrayValue:
        return value.to_integer_array_value()

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> IntegerArrayValue:
        return value.to_integer_array_value()

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> IntegerArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.INTEGER_ARRAY
        )


def to_integer_array_value(other: variable_value.IVariableValue) -> IntegerArrayValue:
    """
    Convert the given value to an ``IntegerArrayValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises ``IncompatibleTypesException``).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to an ``IntegerArrayValue`` type.

    Returns
    -------
    IntegerArrayValue
        Value as an ``IntegerArrayValue`` type.
    """
    return other.accept(__ToIntegerArrayVisitor())


class __ToRealArrayVisitor(ivariable_visitor.IVariableValueVisitor[RealArrayValue]):
    """Visits variable values and converts them to ``RealArrayValue`` types when
    possible."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.REAL_ARRAY
        )

    @overrides
    def visit_real(self, value: RealValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.REAL_ARRAY
        )

    @overrides
    def visit_boolean(self, value: BooleanValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.REAL_ARRAY
        )

    @overrides
    def visit_string(self, value: StringValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.REAL_ARRAY
        )

    @overrides
    def visit_file(self, value: FileValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.REAL_ARRAY
        )

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> RealArrayValue:
        return value.to_real_array_value()

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> RealArrayValue:
        return np.copy(value).view(RealArrayValue)

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> RealArrayValue:
        return value.to_real_array_value()

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> RealArrayValue:
        return value.to_real_array_value()

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> RealArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.REAL_ARRAY
        )


def to_real_array_value(other: variable_value.IVariableValue) -> RealArrayValue:
    """
    Convert the given value to a ``RealArrayValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises ``IncompatibleTypesException``).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to a ``RealArrayValue`` type.

    Returns
    -------
    RealArrayValue
        Value as a ``RealArrayValue`` type.
    """
    return other.accept(__ToRealArrayVisitor())


class __ToStringArrayVisitor(ivariable_visitor.IVariableValueVisitor[StringArrayValue]):
    """Visits variable values and converts them to ``StringArrayValue`` types when
    possible."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY
        )

    @overrides
    def visit_real(self, value: RealValue) -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY
        )

    @overrides
    def visit_boolean(self, value: BooleanValue) -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY
        )

    @overrides
    def visit_string(self, value: StringValue) -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY
        )

    @overrides
    def visit_file(self, value: FileValue) -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY
        )

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> StringArrayValue:
        return value.to_string_array_value()

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> StringArrayValue:
        return value.to_string_array_value()

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> StringArrayValue:
        return value.to_string_array_value()

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> StringArrayValue:
        return np.copy(value).view(StringArrayValue)

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> StringArrayValue:
        raise exceptions.IncompatibleTypesException(
            value.variable_type, variable_type.VariableType.STRING_ARRAY
        )


def to_string_array_value(other: variable_value.IVariableValue) -> StringArrayValue:
    """
    Convert the given value to a ``StringArrayValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises ``IncompatibleTypesException``).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to a ``StringArrayValue`` type.

    Returns
    -------
    StringArrayValue
        Value as a ``StringArrayValue`` type.
    """
    return other.accept(__ToStringArrayVisitor())
