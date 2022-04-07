from __future__ import annotations

from .common_variable_metadata import CommonVariableMetadata
from .variable_type import VariableType


class FileMetadata(CommonVariableMetadata):
    @property
    def variable_type(self) -> VariableType:
        return VariableType.FILE
