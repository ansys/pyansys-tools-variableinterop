"""Definition of FileArrayMetadata."""
from overrides import overrides

from .file_metadata import FileMetadata
from .ivariablemetadata_visitor import IVariableMetadataVisitor, T
from .variable_type import VariableType


class FileArrayMetadata(FileMetadata):
    """Metadata for VariableType.FILE_ARRAY."""

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.FILE_ARRAY

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_file_array(self)