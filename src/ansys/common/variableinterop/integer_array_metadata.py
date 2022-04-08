from .integer_metadata import IntegerMetadata
from .variable_type import VariableType


class IntegerArrayMetadata(IntegerMetadata):
    """Metadata for VariableType.INTEGER_ARRAY"""

    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY
