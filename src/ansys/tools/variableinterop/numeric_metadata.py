# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Defines the ``NumericMetadata`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from overrides import overrides

from .common_variable_metadata import CommonVariableMetadata
from .ivariablemetadata_visitor import IVariableMetadataVisitor, T


class NumericMetadata(CommonVariableMetadata, ABC):
    """Provides a generic base for all numeric metadata implementations."""

    _units_json_key = "units"
    _display_format_json_key = "format"

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._units: str = ""
        self._display_format: str = ""

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def equals(self, other: Any) -> bool:
        """
        Determine if a given metadata is equal to this metadata.

        Parameters
        ----------
        other : Any
            Given metadata to compare this metadata to.

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
        raise NotImplementedError  # pragma: nocover

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

    @overrides
    @abstractmethod
    def to_dict(self) -> dict:
        result = super().to_dict()
        if self._units != "" and not str.isspace(self._units):
            result[NumericMetadata._units_json_key] = self._units
        if self._display_format != "" and not str.isspace(self._display_format):
            result[NumericMetadata._display_format_json_key] = self._display_format
        return result

    @staticmethod
    def _from_dict(data: dict) -> tuple[str, str]:
        """
        Helper method for subclasses to extract numeric metadata information from a JSON
        dictionary.

        Returns
        -------
        tuple[str, str]
            A tuple containing the units and display format.
        """
        units: str = data.get(NumericMetadata._units_json_key, "")
        display_format: str = data.get(NumericMetadata._display_format_json_key, "")

        return units, display_format
