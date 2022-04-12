from overrides import overrides

from .integer_metadata import IntegerMetadata
from .variable_type import VariableType


class IntegerArrayMetadata(IntegerMetadata):
    """Metadata for VariableType.INTEGER_ARRAY"""

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY
