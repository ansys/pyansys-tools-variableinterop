from overrides import overrides

from .real_metadata import RealMetadata
from .variable_type import VariableType


class RealArrayMetadata(RealMetadata):
    """Metadata for VariableType.REAL_ARRAY"""

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY
