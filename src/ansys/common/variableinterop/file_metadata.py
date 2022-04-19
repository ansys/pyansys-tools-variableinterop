"""Definition of FileMetadata."""
from __future__ import annotations

from typing import Any, TypeVar

from overrides import overrides

from .common_variable_metadata import CommonVariableMetadata
from .ivariablemetadata_visitor import IVariableMetadataVisitor
from .variable_type import VariableType

T = TypeVar("T")


class FileMetadata(CommonVariableMetadata):
    """Common metadata for VariableType.FILE."""

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_file(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.FILE

    @overrides
    def equals(self, other: Any) -> bool:
        equal: bool = (isinstance(other, FileMetadata) and
                       super().equals(other))
        return equal
