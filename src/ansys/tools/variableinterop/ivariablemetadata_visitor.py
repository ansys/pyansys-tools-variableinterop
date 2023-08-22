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
"""Bruh."""


class IVariableMetadataVisitor(ABC, Generic[T]):
    """
    The interface to be implemented to instantiate the visitor pattern.

    Pass an instance to CommonVariableMetadata.accept().
    """

    # Single dispatch would make this prettier, but doesn't work with
    #  class methods until 3.8:
    #  https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_integer(self, metadata: IntegerMetadata) -> T:
        """
        Will be called if accept is called on an IntegerMetadata.

        Parameters
        ----------
        metadata : IntegerMetadata
            The IntegerMetadata being visited

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self, metadata: RealMetadata) -> T:
        """
        Will be called if accept is called on a RealMetadata.

        Parameters
        ----------
        metadata : RealMetadata
            The RealMetadata being visited

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean(self, metadata: BooleanMetadata) -> T:
        """
        Will be called if accept is called on a BooleanMetadata.

        Parameters
        ----------
        metadata : BooleanMetadata
            The BooleanMetadata being visited

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string(self, metadata: StringMetadata) -> T:
        """
        Will be called if accept is called on a StringMetadata.

        Parameters
        ----------
        metadata : StringMetadata
            The StringMetadata being visited

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self, metadata: FileMetadata) -> T:
        """
        Will be called if accept is called on a FileMetadata.

        Parameters
        ----------
        metadata : FileMetadata
            The FileMetadata being visited

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_integer_array(self, metadata: IntegerArrayMetadata) -> T:
        """
        Will be called if accept is called on an IntegerArrayMetaData.

        Parameters
        ----------
        metadata : IntegerArrayMetadata
            The IntegerArrayMetaData being visited.

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real_array(self, metadata: RealArrayMetadata) -> T:
        """
        Will be called if accept is called on a RealArrayMetaData.

        Parameters
        ----------
        metadata : RealArrayMetadata
            The RealArrayMetaData being visited.

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean_array(self, metadata: BooleanArrayMetadata) -> T:
        """
        Will be called if accept is called on a BooleanArrayMetaData.

        Parameters
        ----------
        metadata : BooleanArrayMetadata
            The BooleanArrayMetaData being visited.

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, metadata: StringArrayMetadata) -> T:
        """
        Will be called if accept is called on a StringArrayMetaData.

        Parameters
        ----------
        metadata : StringArrayMetadata
            The StringArrayMetaData being visited.

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self, metadata: FileArrayMetadata) -> T:
        """
        Will be called if accept is called on a FileArrayMetadata.

        Parameters
        ----------
        metadata : FileArrayMetadata
            The FileArrayMetadata being visited

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError
