"""Definition of NumericMetadata."""
from __future__ import annotations

from abc import ABC
from typing import TypeVar

from overrides import overrides

import ansys.common.variableinterop.common_variable_metadata as common_variable_metadata
import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor

T = TypeVar("T")


class NumericMetadata(common_variable_metadata.CommonVariableMetadata, ABC):
    """Generic base class for all numeric metadata implementations."""

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._units: str = ""
        self._display_format: str = ""

    def __eq__(self, other):
        return self.are_equal(other)

    def are_equal(self, metadata: common_variable_metadata.CommonVariableMetadata) -> bool:
        """Determine if a given metadata is equal to this metadata.

        Parameters
        ----------
        metadata Metadata to compare this object to.

        Returns
        -------
        True if metadata objects are equal, false otherwise.
        """
        equal: bool = (isinstance(metadata, NumericMetadata) and
                       super().are_equal(metadata) and
                       self._units == metadata._units and
                       self._display_format == metadata._display_format)
        return equal

    @overrides
    def accept(self, visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[T]) -> T:
        raise NotImplementedError

    @property
    def units(self) -> str:
        """Get the units of the variable."""
        return self._units

    @units.setter
    def units(self, value: str) -> None:
        """Set the units of the variable."""
        self._units = value

    # TODO: Formally define format specifications
    @property
    def display_format(self) -> str:
        """Get the display format of the variable."""
        return self._display_format

    @display_format.setter
    def display_format(self, value: str) -> None:
        """Set the display format of the variable."""
        self._display_format = value
