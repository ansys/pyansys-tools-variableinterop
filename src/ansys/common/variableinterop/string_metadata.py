"""Definition of StringMetadata."""
from __future__ import annotations

from typing import List

import ansys.common.variableinterop.common_variable_metadata as common_variable_metadata
import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.variable_type as variable_type


class StringMetadata(common_variable_metadata.CommonVariableMetadata):
    """Common metadata for VariableType.STRING and VariableType.STRING_ARRAY."""

    def __init__(self) -> None:
        super().__init__()
        self._enumerated_values: List[string_value.StringValue] = []
        self._enumerated_aliases: List[str] = []

    # equality definition here

    # clone here

    def accept(
            self,
            visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[common_variable_metadata.T]
    ) -> common_variable_metadata.T:
        return visitor.visit_string(self)

    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.STRING

    # TODO need implicit coerce for arrays

    @property
    def enumerated_values(self) -> List[string_value.StringValue]:
        """
        Get the list of enumerated values.

        May be empty to imply no enumerated values.
        Returns
        -------
        The list of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[string_value.StringValue]) -> None:
        """
        Set the list of enumerated values.

        Parameters
        ----------
        value
        The list of values to set.
        """
        self._enumerated_values = value

    @property
    def enumerated_aliases(self) -> List[str]:
        """
        Get the list of enumerated aliases.

        May be empty to imply no enumerated aliases.
        Returns
        -------
        The list of enumerated aliases.
        """
        return self._enumerated_aliases

    @enumerated_aliases.setter
    def enumerated_aliases(self, value: List[str]) -> None:
        """
        Set the list of enumerated aliases.

        Parameters
        ----------
        value
        The list of aliases to set.
        """
        self._enumerated_aliases = value
