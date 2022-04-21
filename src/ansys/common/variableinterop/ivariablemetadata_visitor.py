"""Definition of IVariableMetadataVisitor."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from ansys.common.variableinterop import FileArrayMetadata, FileMetadata
    from ansys.common.variableinterop.array_metadata import (
        BooleanArrayMetadata,
        IntegerArrayMetadata,
        RealArrayMetadata,
        StringArrayMetadata,
    )
    from ansys.common.variableinterop.scalar_metadata import (
        BooleanMetadata,
        IntegerMetadata,
        RealMetadata,
        StringMetadata,
    )

T = TypeVar("T")


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
        metadata
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
        metadata
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
        metadata
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
        metadata
            The StringMetadata being visited

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self, metadata: FileMetadata):
        """
        Will be called if accept is called on a FileMetadata.

        Parameters
        ----------
        metadata The FileMetadata being visited

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
        metadata
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
        metadata
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
        metadata
            The BooleanArrayMetaData being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, metadata: StringArrayMetadata) -> T:
        """
        Will be called if accept is called on a StringArrayMetaData.

        Parameters
        ----------
        metadata
            The StringArrayMetaData being visited.

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self, metadata: FileArrayMetadata):
        """
        Will be called if accept is called on a FileArrayMetadata.

        Parameters
        ----------
        metadata The FileArrayMetadata being visited

        Returns
        -------
        The result.
        """
        raise NotImplementedError
