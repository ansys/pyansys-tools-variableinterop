"""Definition of array value visitors."""
import numpy as np
from overrides import overrides

from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
import ansys.common.variableinterop.exceptions as exceptions
from ansys.common.variableinterop.file_array_value import FileArrayValue
from ansys.common.variableinterop.file_value import FileValue
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value


class __ToBooleanArrayVisitor(ivariable_visitor.IVariableValueVisitor[BooleanArrayValue]):
    """Visitor pattern to call conversion methods to BooleanArrayValue."""

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
    Convert the given value to a BooleanArrayValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other : IVariableValue
        The other value to convert to a BooleanArrayValue.

    Returns
    -------
    BooleanArrayValue
    The value as a BooleanArrayValue.

    """
    return other.accept(__ToBooleanArrayVisitor())


class __ToIntegerArrayVisitor(ivariable_visitor.IVariableValueVisitor[IntegerArrayValue]):
    """Visitor pattern to call conversion methods to IntegerArrayValue."""

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
    Convert the given value to a IntegerArrayValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other : IVariableValue
        The other value to convert to a IntegerArrayValue.

    Returns
    -------
    IntegerArrayValue
    The value as a IntegerArrayValue.

    """
    return other.accept(__ToIntegerArrayVisitor())


class __ToRealArrayVisitor(ivariable_visitor.IVariableValueVisitor[RealArrayValue]):
    """Visitor pattern to call conversion methods to RealArrayValue."""

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
    Convert the given value to a RealArrayValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other : IVariableValue
        The other value to convert to a RealArrayValue.

    Returns
    -------
    RealArrayValue
    The value as a RealArrayValue.

    """
    return other.accept(__ToRealArrayVisitor())


class __ToStringArrayVisitor(ivariable_visitor.IVariableValueVisitor[StringArrayValue]):
    """Visitor pattern to call conversion methods to StringArrayValue."""

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
    Convert the given value to a StringArrayValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other : IVariableValue
        The other value to convert to a StringArrayValue.

    Returns
    -------
    StringArrayValue
    The value as a StringArrayValue.

    """
    return other.accept(__ToStringArrayVisitor())
