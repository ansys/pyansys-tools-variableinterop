from typing import TypeVar

from overrides import overrides

from ansys.common.variableinterop.boolean_metadata import BooleanMetadata
from ansys.common.variableinterop.ivariablemetadata_visitor import IVariableMetadataVisitor
from ansys.common.variableinterop.variable_type import VariableType


class BooleanArrayMetadata(BooleanMetadata):
    """Metadata for BooleanArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_boolean_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN_ARRAY
