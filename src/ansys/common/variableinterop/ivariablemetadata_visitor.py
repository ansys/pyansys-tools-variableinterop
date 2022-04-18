"""Definition of IVariableMetadataVisitor."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    import ansys.common.variableinterop.boolean_metadata as boolean_metadata
    import ansys.common.variableinterop.integer_metadata as integer_metadata
    import ansys.common.variableinterop.real_metadata as real_metadata
    import ansys.common.variableinterop.string_metadata as string_metadata
    import ansys.common.variableinterop.real_array_metadata as real_array_metadata
    import ansys.common.variableinterop.integer_array_metadata as integer_array_metadata
    import ansys.common.variableinterop.boolean_array_metadata as boolean_array_metadata
    import ansys.common.variableinterop.string_array_metadata as string_array_metadata

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
    def visit_integer(self, metadata: integer_metadata.IntegerMetadata) -> T:
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
    def visit_real(self, metadata: real_metadata.RealMetadata) -> T:
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
    def visit_boolean(self, metadata: boolean_metadata.BooleanMetadata) -> T:
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
    def visit_string(self, metadata: string_metadata.StringMetadata) -> T:
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
    def visit_integer_array(self, metadata: integer_array_metadata.IntegerArrayMetadata) -> T:
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
    def visit_real_array(self, metadata: real_array_metadata.RealArrayMetadata) -> T:
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
    def visit_boolean_array(self, metadata: boolean_array_metadata.BooleanArrayMetadata) -> T:
        """
        Will be called if accept is called on a BooleanArrayMetaData.

        Parameters
        ----------
        metadata
            The BooleanArrayMetaData being visited.

        Returns
        -------
        T
            The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, metadata: string_array_metadata.StringArrayMetadata) -> T:
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
