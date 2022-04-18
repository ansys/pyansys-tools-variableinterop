from typing import TypeVar

from overrides import overrides

from ansys.common.variableinterop.ivariablemetadata_visitor import IVariableMetadataVisitor
from ansys.common.variableinterop.string_metadata import StringMetadata
from ansys.common.variableinterop.variable_type import VariableType


class StringArrayMetadata(StringMetadata):
    """Metadata for StringArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_string_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING_ARRAY
