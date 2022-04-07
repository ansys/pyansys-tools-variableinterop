from .file_metadata import FileMetadata
from .variable_type import VariableType


class FileArrayMetadata(FileMetadata):

    def variable_type(self) -> VariableType:
        return VariableType.FILE_ARRAY
