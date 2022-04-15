from typing import TypeVar

from overrides import overrides

from ansys.common.variableinterop.real_metadata import RealMetadata
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.ivariablemetadata_visitor import IVariableMetadataVisitor


class RealArrayMetadata(RealMetadata):
    """Metadata for RealArrayValue"""

    T = TypeVar("T")

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_real_array(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL_ARRAY
