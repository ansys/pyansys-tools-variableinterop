# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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
"""Definition of IVariableValue and related classes."""
from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from typing import Generic, Optional, Tuple, TypeVar

from numpy.typing import NDArray

import ansys.tools.variableinterop.variable_type as variable_type_lib

from .isave_context import ISaveContext
from .ivariable_visitor import IVariableValueVisitor

T = TypeVar("T")


class IVariableValue(ABC):
    """Defines an interface for the common behavior among all variable types."""

    def clone(self) -> IVariableValue:
        """Get a deep copy of this value."""
        return copy.deepcopy(self)

    @abstractmethod
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        """
        Invoke the visitor pattern of this object using the passed in visitor
        implementation.

        Parameters
        ----------
        visitor : IVariableValueVisitor
            The visitor object to call

        Returns
        -------
        T
            Results of the visitor invocation
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def variable_type(self) -> variable_type_lib.VariableType:
        """
        Get the variable type of this object.

        Returns
        -------
        VariableType
            The variable type of this object
        """
        raise NotImplementedError

    @abstractmethod
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        """
        Convert this value to an API string.

        Returns
        -------
        str
            A string appropriate for use in files and APIs.
        """
        raise NotImplementedError

    @abstractmethod
    def to_display_string(self, locale_name: str) -> str:
        """
        Convert this value to a formatted string.

        Parameters
        ----------
        locale_name : str
            The locale to format in.

        Returns
        -------
        str
            A string appropriate for use in user facing areas.
        """
        raise NotImplementedError


class CommonArrayValue(Generic[T], NDArray[T], IVariableValue, ABC):
    """
    Interface that defines common behavior for array types.

    Inherits ``IVariableValue``.
    """

    def get_lengths(self) -> Tuple[int]:
        """
        Get dimension sizes of the array.

        Returns
        -------
        Tuple[int]
            Dimension sizes of the array.
        """
        return self.shape

    def rank(self) -> int:
        """
        Get number of dimensions in the array.

        Returns
        -------
        int
            Number of dimensions in the array.
        """
        return len(self.shape)


class VariableValueInvalidError(Exception):
    """Raised to indicate a required variable value was invalid."""

    pass
