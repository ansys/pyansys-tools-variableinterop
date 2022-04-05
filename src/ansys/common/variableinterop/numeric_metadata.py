"""Definition of NumericMetadata."""
from __future__ import annotations

from abc import ABC
from typing import TypeVar

from .common_variable_metadata import CommonVariableMetadata

T = TypeVar("T")


class NumericMetadata(CommonVariableMetadata, ABC):
    """Generic base class for all numeric metadata implementations."""

    def __init__(self) -> None:
        super().__init__()
        self._units: str = ""
        self._display_format: str = ""

    # equality definition here

    # clone here

    # accept here

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
