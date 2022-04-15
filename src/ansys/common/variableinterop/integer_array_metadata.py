from typing import TypeVar

from overrides import overrides

from ansys.common.variableinterop.integer_metadata import IntegerMetadata
from ansys.common.variableinterop.ivariablemetadata_visitor import IVariableMetadataVisitor
from ansys.common.variableinterop.variable_type import VariableType


class IntegerArrayMetadata(IntegerMetadata):
    """Metadata for IntegerArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_integer_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER_ARRAY
