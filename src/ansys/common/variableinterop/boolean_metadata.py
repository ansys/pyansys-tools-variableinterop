"""Definition of BooleanMetadata."""
from __future__ import annotations

from typing import TypeVar

from overrides import overrides

import ansys.common.variableinterop.common_variable_metadata as common_variable_metadata
import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.variable_type as variable_type

T = TypeVar("T")


class BooleanMetadata(common_variable_metadata.CommonVariableMetadata):
    """Common metadata for VariableType.BOOLEAN and VariableType.BOOLEAN_ARRAY."""

    # equality definition here

    # clone here

    @overrides
    def accept(self, visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    # TODO need implicit coerce for arrays
