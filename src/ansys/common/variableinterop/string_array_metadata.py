from .string_metadata import StringMetadata
from .variable_type import VariableType


class StringArrayMetadata(StringMetadata):
    """Metadata for VariableType.STRING_ARRAY"""

    @property
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY
