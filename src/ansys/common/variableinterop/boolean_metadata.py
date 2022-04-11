"""Definition of BooleanMetadata."""
from __future__ import annotations

import ansys.common.variableinterop.common_variable_metadata as common_variable_metadata
import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.variable_type as variable_type


class BooleanMetadata(common_variable_metadata.CommonVariableMetadata):
    """Common metadata for VariableType.BOOLEAN and VariableType.BOOLEAN_ARRAY."""

    def __eq__(self, other):
        return self.are_equal(other)

    # clone here

    def accept(
            self,
            visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[common_variable_metadata.T]
    ) -> common_variable_metadata.T:
        return visitor.visit_boolean(self)

    @property
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    def are_equal(self, metadata: common_variable_metadata.CommonVariableMetadata) -> bool:
        """Determine if a given metadata is equal to this metadata.

        Parameters
        ----------
        metadata Metadata to compare this object to.

        Returns
        -------
        True if metadata objects are equal, false otherwise.
        """
        equal: bool = (isinstance(metadata, BooleanMetadata) and
                       super().are_equal(metadata))
        return equal

    # TODO need implicit coerce for arrays
