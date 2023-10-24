"""Definition of IVariableValueVisitor."""
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
    Defines the interface to be implemented to use the visitor pattern with variable
    values.

    Pass an instance to IVariableValue.accept().
    """

    # Single dispatch would make this prettier, but doesn't work with
    # class methods until 3.8:
    # https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_integer(self, value: IntegerValue) -> T:
        """
        Will be called if accept is called on an IntegerValue.

        Parameters
        ----------
        value : IntegerValue
            ``IntegerValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self, value: RealValue) -> T:
        """
        Will be called if accept is called on a RealValue.

        Parameters
        ----------
        value : RealValue
            ``RealValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean(self, value: BooleanValue) -> T:
        """
        Will be called if accept is called on a BooleanValue.

        Parameters
        ----------
        value : BooleanValue
            ``BooleanValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string(self, value: StringValue) -> T:
        """
        Will be called if accept is called on a StringValue.

        Parameters
        ----------
        value : StringValue
            ``StringValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_integer_array(self, value: IntegerArrayValue) -> T:
        """
        Will be called if accept is called on an IntegerArrayValue.

        Parameters
        ----------
        value : IntegerArrayValue
            ``IntegerArrayValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self, value: FileValue) -> T:
        """
        Will be called if accept is called on an FileValue.

        Parameters
        ----------
        value : FileValue
            ``FileValue`` object being visited

        Returns
        -------
        T
            Result
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real_array(self, value: RealArrayValue) -> T:
        """
        Will be called if accept is called on a RealArrayValue.

        Parameters
        ----------
        value : RealArrayValue
            ``RealArrayValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean_array(self, value: BooleanArrayValue) -> T:
        """
        Will be called if accept is called on a BooleanArrayValue.

        Parameters
        ----------
        value : BooleanArrayValue
            ``BooleanArrayValue`` being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, value: StringArrayValue) -> T:
        """
        Will be called if accept is called on a StringArrayValue.

        Parameters
        ----------
        value : StringArrayValue
            ``StringArrayValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self, value: FileArrayValue) -> T:
        """
        Will be called if accept is called on an FileArrayValue.

        Parameters
        ----------
        value : FileArrayValue
            ``FileArrayValue`` object being visited.

        Returns
        -------
        T
            Result.
        """
        raise NotImplementedError
