from overrides import overrides

from .boolean_metadata import BooleanMetadata
from .variable_type import VariableType


class BooleanArrayMetadata(BooleanMetadata):
    """Metadata for VariableType.BOOLEAN_ARRAY"""

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY
