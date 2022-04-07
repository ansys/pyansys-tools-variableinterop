from .string_metadata import StringMetadata
from .variable_type import VariableType


class IntegerArrayMetadata(StringMetadata):

    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY
