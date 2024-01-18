"""Defines the ``NumericMetadata`` class."""
from __future__ import annotations

from abc import ABC
from typing import Any

from overrides import overrides

from .common_variable_metadata import CommonVariableMetadata
from .ivariablemetadata_visitor import IVariableMetadataVisitor, T


class NumericMetadata(CommonVariableMetadata, ABC):
    """Provides a generic base for all numeric metadata implementations."""

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._units: str = ""
        self._display_format: str = ""

    @overrides
    def __eq__(self, other):
        return self.are_equal(other)

    @overrides
    def equals(self, other: Any) -> bool:
        """
        Determine if a given metadata is equal to this metadata.

        Parameters
        ----------
        other : Any
            Given metadata to compare this metadate to.

        Returns
        -------
        bool
            ``True`` if the two objects are equal, ``False`` otherwise.
        """
        equal: bool = (
            isinstance(other, NumericMetadata)
            and super().equals(other)
            and self._units == other._units
            and self._display_format == other._display_format
        )
        return equal

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        raise NotImplementedError

    @property
    def units(self) -> str:
        """Units of the variable."""
        return self._units

    @units.setter
    def units(self, value: str) -> None:
        self._units = value

    # TODO: Formally define format specifications
    @property
    def display_format(self) -> str:
        """Display format of the variable."""
        return self._display_format

    @display_format.setter
    def display_format(self, value: str) -> None:
        self._display_format = value
