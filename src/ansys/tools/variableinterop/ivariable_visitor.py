"""Defines the ``IVariableValueVisitor`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from .array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
    from .file_array_value import FileArrayValue
    from .file_value import FileValue
    from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue

T = TypeVar("T")


class IVariableValueVisitor(ABC, Generic[T]):
    """
    Defines the interface to be implemented for using the visitor pattern with variable
    values.

    To use an implementation of this interface, create and pass an instance to the
    :meth:`IVariableValue.accept()` method.
    """

    # Single dispatch would make this prettier, but doesn't work with
    # class methods until 3.8:
    # https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_integer(self, value: IntegerValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        an ``IntegerValue`` type.

        Parameters
        ----------
        value : IntegerValue
            ``IntegerValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self, value: RealValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        a ``RealValue`` type.

        Parameters
        ----------
        value : RealValue
            ``RealValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean(self, value: BooleanValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        a ``BooleanValue`` type.

        Parameters
        ----------
        value : BooleanValue
            ``BooleanValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string(self, value: StringValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        a ``StringValue`` type.

        Parameters
        ----------
        value : StringValue
            ``StringValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_integer_array(self, value: IntegerArrayValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        an ``IntegerArrayValue`` type.

        Parameters
        ----------
        value : IntegerArrayValue
            ``IntegerArrayValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self, value: FileValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        a ``FileValue`` type.

        Parameters
        ----------
        value : FileValue
            ``FileValue`` type to visit.

        Returns
        -------
        T
            Result
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real_array(self, value: RealArrayValue) -> T:
        """
        Method that is called if the `:meth:`IVariableValue.accept()` method is called
        on a ``RealArrayValue`` type.

        Parameters
        ----------
        value : RealArrayValue
            ``RealArrayValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean_array(self, value: BooleanArrayValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        a ``BooleanArrayValue`` type.

        Parameters
        ----------
        value : BooleanArrayValue
            ``BooleanArrayValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, value: StringArrayValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        a ``StringArrayValue`` type.

        Parameters
        ----------
        value : StringArrayValue
            ``StringArrayValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self, value: FileArrayValue) -> T:
        """
        Method that is called if the :meth:`IVariableValue.accept()` method is called on
        a ``FileArrayValue`` type.

        Parameters
        ----------
        value : FileArrayValue
            ``FileArrayValue`` type to visit.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError
