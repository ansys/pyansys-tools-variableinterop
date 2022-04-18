"""Definitions of array metadata types."""
from typing import TypeVar

from overrides import overrides

from ansys.common.variableinterop.ivariablemetadata_visitor import IVariableMetadataVisitor
from ansys.common.variableinterop.scalar_metadata import (
    BooleanMetadata,
    IntegerMetadata,
    RealMetadata,
    StringMetadata,
)
from ansys.common.variableinterop.variable_type import VariableType


class BooleanArrayMetadata(BooleanMetadata):
    """Metadata for BooleanArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY


class IntegerArrayMetadata(IntegerMetadata):
    """Metadata for IntegerArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY


class RealArrayMetadata(RealMetadata):
    """Metadata for RealArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY


class StringArrayMetadata(StringMetadata):
    """Metadata for StringArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY
