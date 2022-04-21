"""Definition of scalar value visitors."""

from overrides import overrides

from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
from ansys.common.variableinterop.exceptions import IncompatibleTypesException
from ansys.common.variableinterop.file_array_value import FileArrayValue
from ansys.common.variableinterop.file_value import FileValue
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.variable_value import IVariableValue


class __ToBooleanVisitor(IVariableValueVisitor[bool]):
    """An IVariableValueVisitor which returns a bool equivalent of the \
    object visited."""

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
        raise IncompatibleTypesException(value.variable_type(), "bool")

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type(), "bool")

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type(), "bool")

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type(), "bool")

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type(), "bool")

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> bool:
        raise IncompatibleTypesException(value.variable_type(), "bool")


def to_boolean_value(other: IVariableValue) -> BooleanValue:
    """
    Convert the given value to a BooleanValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other the other value to convert to a BooleanValue.

    Returns
    -------
    The value as a RealValue.

    """
    return other.accept(__ToBooleanVisitor())


class __ToIntegerVisitor(IVariableValueVisitor[IntegerValue]):
    """This visitor implementation converts the visited value to a RealValue."""

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
        raise IncompatibleTypesException(value.variable_type(), VariableType.INTEGER)

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
        raise IncompatibleTypesException(VariableType.FILE_ARRAY, VariableType.INTEGER_ARRAY)


def to_integer_value(other: IVariableValue) -> IntegerValue:
    """
    Convert the given value to an IntegerValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).
    Parameters
    ----------
    other the other value to convert to a RealValue.
    Returns
    -------
    The value as a RealValue.
    """
    return other.accept(__ToIntegerVisitor())


class __ToRealVisitor(IVariableValueVisitor[RealValue]):
    """This visitor implementation converts the visited value to a RealValue."""

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
        raise IncompatibleTypesException(value.variable_type(), VariableType.REAL)

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
        raise IncompatibleTypesException(value.variable_type(), VariableType.REAL)


def to_real_value(other: IVariableValue) -> RealValue:
    """
    Convert the given value to a RealValue.

    The conversion is performed according to the type interoperability specifications.
    Note that some conversions are lossy (resulting in a loss of precision)
    and some conversions are not possible (raises IncompatibleTypesException).

    Parameters
    ----------
    other the other value to convert to a RealValue.

    Returns
    -------
    The value as a RealValue.

    """
    return other.accept(__ToRealVisitor())
