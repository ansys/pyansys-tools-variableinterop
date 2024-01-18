"""Defines array metadata types."""
from overrides import overrides

from .ivariablemetadata_visitor import IVariableMetadataVisitor, T
from .scalar_metadata import BooleanMetadata, IntegerMetadata, RealMetadata, StringMetadata
from .variable_type import VariableType


class BooleanArrayMetadata(BooleanMetadata):
    """Provides metadata for the ``BooleanArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY


class IntegerArrayMetadata(IntegerMetadata):
    """Provides metadata for the ``IntegerArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY


class RealArrayMetadata(RealMetadata):
    """Provides metadata for the ``RealArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY


class StringArrayMetadata(StringMetadata):
    """Provides metadata for the ``StringArrayValue`` variable type."""

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY
