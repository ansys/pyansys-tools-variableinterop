"""Definition of BooleanMetadata."""
from __future__ import annotations

from ansys.common.variableinterop import common_variable_metadata
from ansys.common.variableinterop import ivariablemetadata_visitor
from ansys.common.variableinterop import variable_type


class BooleanMetadata(common_variable_metadata.CommonVariableMetadata):
    """Common metadata for VariableType.BOOLEAN and VariableType.BOOLEAN_ARRAY."""

    # equality definition here

    # clone here

    def accept(
            self,
            visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[common_variable_metadata.T]
    ) -> common_variable_metadata.T:
        return visitor.visit_boolean(self)

    @property
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    # TODO need implicit coerce for arrays
