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
"""Defines scalar value visitors."""

from overrides import overrides

from .array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from .exceptions import IncompatibleTypesException
from .file_array_value import FileArrayValue
from .file_value import FileValue
from .ivariable_visitor import IVariableValueVisitor
from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from .variable_type import VariableType
from .variable_value import IVariableValue


class __ToBooleanVisitor(IVariableValueVisitor[bool]):
    """Converts visited values to the ``BooleanValue`` type when possible."""

    @overrides
    def visit_boolean(self, value: "BooleanValue") -> bool:
        return bool(value)

    @overrides
    def visit_integer(self, value: IntegerValue) -> bool:
        return BooleanValue.int64_to_bool(value)

    @overrides
    def visit_real(self, value: RealValue) -> bool:
        return BooleanValue.float_to_bool(value)

    @overrides
    def visit_string(self, value: StringValue) -> bool:
        return BooleanValue.str_to_bool(value)

    @overrides
    def visit_file(self, value: FileValue) -> bool:
        raise IncompatibleTypesException(value.variable_type, "bool")

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type, "bool")

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type, "bool")

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type, "bool")

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type, "bool")

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type, "bool")


def to_boolean_value(other: IVariableValue) -> BooleanValue:
    """
    Convert the given value to a ``BooleanValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to a ``BooleanValue`` type.

    Returns
    -------
    BooleanValue
        Value as a ``BooleanValue`` type.
    """
    return BooleanValue(other.accept(__ToBooleanVisitor()))


class __ToIntegerVisitor(IVariableValueVisitor[IntegerValue]):
    """Converts visited values to the ``IntegerValue`` type when possible."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> IntegerValue:
        return value

    @overrides
    def visit_real(self, value: RealValue) -> IntegerValue:
        return value.to_int_value()

    @overrides
    def visit_boolean(self, value: BooleanValue) -> IntegerValue:
        return value.to_integer_value()

    @overrides
    def visit_string(self, value: StringValue) -> IntegerValue:
        return IntegerValue.from_api_string(value.to_api_string())

    @overrides
    def visit_file(self, value: FileValue) -> IntegerValue:
        raise IncompatibleTypesException(value.variable_type, VariableType.INTEGER)

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.INTEGER_ARRAY, VariableType.INTEGER)

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.REAL_ARRAY, VariableType.INTEGER)

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.BOOLEAN_ARRAY, VariableType.INTEGER)

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.STRING_ARRAY, VariableType.INTEGER)

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> IntegerValue:
        raise IncompatibleTypesException(VariableType.FILE_ARRAY, VariableType.INTEGER)


def to_integer_value(other: IVariableValue) -> IntegerValue:
    """
    Convert the given value to an ``IntegerValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to an ``IntegerValue`` type.

    Returns
    -------
    IntegerValue
        Value as an ``IntegerValue`` type.
    """
    return other.accept(__ToIntegerVisitor())


class __ToRealVisitor(IVariableValueVisitor[RealValue]):
    """Converts visited values to the ``RealValue`` type when possible."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> RealValue:
        return value.to_real_value()

    @overrides
    def visit_real(self, value: RealValue) -> RealValue:
        return value

    @overrides
    def visit_boolean(self, value: BooleanValue) -> RealValue:
        return value.to_real_value()

    @overrides
    def visit_string(self, value: StringValue) -> RealValue:
        return RealValue.from_api_string(value.to_api_string())

    @overrides
    def visit_file(self, value: FileValue) -> RealValue:
        raise IncompatibleTypesException(value.variable_type, VariableType.REAL)

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.INTEGER_ARRAY, VariableType.REAL)

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.REAL_ARRAY, VariableType.REAL)

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.BOOLEAN_ARRAY, VariableType.REAL)

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.STRING_ARRAY, VariableType.REAL)

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> RealValue:
        raise IncompatibleTypesException(VariableType.FILE_ARRAY, VariableType.REAL)


def to_real_value(other: IVariableValue) -> RealValue:
    """
    Convert the given value to a ``RealValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises ``IncompatibleTypesException``).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to a ``RealValue`` type.

    Returns
    -------
    RealValue
        Value as a ``RealValue`` type.
    """
    return other.accept(__ToRealVisitor())


class __ToStringVisitor(IVariableValueVisitor[StringValue]):
    """Converts visited values to a ``StringValue`` type when possible."""

    @overrides
    def visit_integer(self, value: IntegerValue) -> StringValue:
        return StringValue(value.to_api_string())

    @overrides
    def visit_real(self, value: RealValue) -> StringValue:
        return StringValue(value.to_api_string())

    @overrides
    def visit_boolean(self, value: BooleanValue) -> StringValue:
        return StringValue(value.to_api_string())

    @overrides
    def visit_string(self, value: StringValue) -> StringValue:
        return value

    @overrides
    def visit_file(self, value: FileValue) -> StringValue:
        raise IncompatibleTypesException(VariableType.FILE, VariableType.STRING)

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> StringValue:
        return StringValue(value.to_api_string())

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> StringValue:
        return StringValue(value.to_api_string())

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> StringValue:
        return StringValue(value.to_api_string())

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> StringValue:
        return StringValue(value.to_api_string())

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> StringValue:
        raise IncompatibleTypesException(VariableType.FILE_ARRAY, VariableType.STRING)


def to_string_value(other: IVariableValue) -> StringValue:
    """
    Convert the given value to a ``StringValue`` type.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision),
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other : IVariableValue
        Other value to convert to a ``StringValue`` type.

    Returns
    -------
    StringValue
        Value as a ``StringValue`` type.
    """
    return other.accept(__ToStringVisitor())
