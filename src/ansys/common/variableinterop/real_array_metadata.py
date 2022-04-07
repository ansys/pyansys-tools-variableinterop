from .real_metadata import RealMetadata
from .variable_type import VariableType


class RealArrayMetadata(RealMetadata):

    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY
