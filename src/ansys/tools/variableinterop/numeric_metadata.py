# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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
