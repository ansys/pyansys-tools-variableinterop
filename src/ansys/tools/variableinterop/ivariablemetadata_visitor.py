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
"""Defines the ``IVariableMetadataVisitor`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from .array_metadata import (
        BooleanArrayMetadata,
        IntegerArrayMetadata,
        RealArrayMetadata,
        StringArrayMetadata,
    )
    from .file_array_metadata import FileArrayMetadata
    from .file_metadata import FileMetadata
    from .scalar_metadata import BooleanMetadata, IntegerMetadata, RealMetadata, StringMetadata

T = TypeVar("T")


class IVariableMetadataVisitor(ABC, Generic[T]):
    """
    Defines the interface to be implemented for using the visitor pattern with variable
    metadata.

    To use an implementation of this interface, create and pass an instance to the
    :meth:`IVariableValue.accept()` method.
    """

    # Single dispatch would make this prettier, but doesn't work with
    # class methods until 3.8:
    # https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_integer(self, metadata: IntegerMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on an
        ``IntegerMetadata`` type.

        Parameters
        ----------
        metadata : IntegerMetadata
            ``IntegerMetadata`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self, metadata: RealMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``RealMetadata`` type.

        Parameters
        ----------
        metadata : RealMetadata
            ``RealMetadata`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean(self, metadata: BooleanMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``BooleanMetadata`` type.

        Parameters
        ----------
        metadata : BooleanMetadata
            ``BooleanMetadata`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string(self, metadata: StringMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``StringMetadata`` type.

        Parameters
        ----------
        metadata : StringMetadata
            ``StringMetadata`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self, metadata: FileMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``FileMetadata`` type.

        Parameters
        ----------
        metadata : FileMetadata
            ``FileMetadata`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_integer_array(self, metadata: IntegerArrayMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on an
        ``IntegerArrayMetaData`` type.

        Parameters
        ----------
        metadata : IntegerArrayMetadata
            ``IntegerArrayMetadata`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real_array(self, metadata: RealArrayMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``RealArrayMetaData`` type.

        Parameters
        ----------
        metadata : RealArrayMetadata
            ``RealArrayMetaData`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean_array(self, metadata: BooleanArrayMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``BooleanArrayMetaData`` type.

        Parameters
        ----------
        metadata : BooleanArrayMetadata
            ``BooleanArrayMetaData`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, metadata: StringArrayMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``StringArrayMetaData`` type.

        Parameters
        ----------
        metadata : StringArrayMetadata
            ``StringArrayMetaData`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self, metadata: FileArrayMetadata) -> T:
        """
        Method that is called if the ``IVariableValue.accept()`` method is called on a
        ``FileArrayMetadata``` type.

        Parameters
        ----------
        metadata : FileArrayMetadata
            ``FileArrayMetadata`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError
