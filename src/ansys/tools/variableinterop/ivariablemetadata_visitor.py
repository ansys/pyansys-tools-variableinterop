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

"""Definition of IVariableMetadataVisitor."""
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
    Defines the interface to be implemented to use the visitor pattern with variable
    metadata.

    Pass an instance to :meth:``CommonVariableMetadata.accept()``.
    """

    # Single dispatch would make this prettier, but doesn't work with
    # class methods until 3.8:
    # https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_integer(self, metadata: IntegerMetadata) -> T:
        """
        Will be called if accept is called on an IntegerMetadata.

        Parameters
        ----------
        metadata : IntegerMetadata
            ``IntegerMetadata`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self, metadata: RealMetadata) -> T:
        """
        Will be called if accept is called on a RealMetadata.

        Parameters
        ----------
        metadata : RealMetadata
            ``RealMetadata`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean(self, metadata: BooleanMetadata) -> T:
        """
        Will be called if accept is called on a BooleanMetadata.

        Parameters
        ----------
        metadata : BooleanMetadata
            ``BooleanMetadata`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string(self, metadata: StringMetadata) -> T:
        """
        Will be called if accept is called on a StringMetadata.

        Parameters
        ----------
        metadata : StringMetadata
            ``StringMetadata`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self, metadata: FileMetadata) -> T:
        """
        Will be called if accept is called on a FileMetadata.

        Parameters
        ----------
        metadata : FileMetadata
            ``FileMetadata`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_integer_array(self, metadata: IntegerArrayMetadata) -> T:
        """
        Will be called if accept is called on an IntegerArrayMetaData.

        Parameters
        ----------
        metadata : IntegerArrayMetadata
            ``IntegerArrayMetadata`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real_array(self, metadata: RealArrayMetadata) -> T:
        """
        Will be called if accept is called on a RealArrayMetaData.

        Parameters
        ----------
        metadata : RealArrayMetadata
            ``RealArrayMetaData`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean_array(self, metadata: BooleanArrayMetadata) -> T:
        """
        Will be called if accept is called on a BooleanArrayMetaData.

        Parameters
        ----------
        metadata : BooleanArrayMetadata
            ``BooleanArrayMetaData`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, metadata: StringArrayMetadata) -> T:
        """
        Will be called if accept is called on a StringArrayMetaData.

        Parameters
        ----------
        metadata : StringArrayMetadata
            ``StringArrayMetaData`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self, metadata: FileArrayMetadata) -> T:
        """
        Will be called if accept is called on a FileArrayMetadata.

        Parameters
        ----------
        metadata : FileArrayMetadata
            ``FileArrayMetadata`` object being visited

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError
