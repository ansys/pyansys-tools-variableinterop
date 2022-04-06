from .boolean_metadata import BooleanMetadata
from .variable_type import VariableType

class BooleanArrayMetadata(BooleanMetadata):

    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY