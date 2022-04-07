"""Definition of StringMetadata."""
from __future__ import annotations

from typing import List

from . import CommonVariableMetadata
from .string_value import StringValue
from .variable_type import VariableType


class StringMetadata(CommonVariableMetadata):
    """Common metadata for VariableType.STRING and VariableType.STRING_ARRAY."""

    def __init__(self) -> None:
        super().__init__()
        self._enumerated_values: List[StringValue] = []
        self._enumerated_aliases: List[str] = []

    # equality definition here

    # clone here

    # accept here

    def variable_type(self) -> VariableType:
        return VariableType.STRING

    # TODO need implicit coerce for arrays

    @property
    def enumerated_values(self) -> List[StringValue]:
        """
        Get the list of enumerated values.

        May be empty to imply no enumerated values.
        Returns
        -------
        The list of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[StringValue]) -> None:
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
