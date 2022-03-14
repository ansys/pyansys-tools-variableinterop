from __future__ import annotations

from abc import ABC
from typing import TypeVar

from .common_variable_metadata import CommonVariableMetadata

T = TypeVar("T")


class NumericMetadata(CommonVariableMetadata, ABC):
    """
    Generic base class for all numeric metadata implementations
    """

    def __init__(self):
        self._units: str = ""
        self._display_format: str = ""

    # TODO: Should units be part of value?
    @property
    def units(self) -> str:
        """The units of the variable"""
        return self._units

    @units.setter
    def units(self, value: str):
        self._units = value

    # TODO: Formally define format specifications
    @property
    def display_format(self) -> str:
        return self._display_format

    @display_format.setter
    def display_format(self, value: str):
        self._display_format = value
