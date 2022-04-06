"""Definition of BooleanMetadata."""
from __future__ import annotations

import ansys.common.variableinterop.common_variable_metadata as common_variable_metadata
import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.variable_type as variable_type


class BooleanMetadata(common_variable_metadata.CommonVariableMetadata):
    """Common metadata for VariableType.BOOLEAN and VariableType.BOOLEAN_ARRAY."""

    # equality definition here

    # clone here

    def accept(
            self,
            visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[common_variable_metadata.T]
    ) -> common_variable_metadata.T:
        return visitor.visit_boolean(self)

    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    # TODO need implicit coerce for arrays
