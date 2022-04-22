"""Definition of IVariableValueVisitor."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar


if TYPE_CHECKING:
    from ansys.common.variableinterop import FileArrayValue
    from ansys.common.variableinterop.array_values import (
        BooleanArrayValue,
        IntegerArrayValue,
        RealArrayValue,
        StringArrayValue,
    )
    from ansys.common.variableinterop.file_value import FileValue
    from ansys.common.variableinterop.scalar_values import (
        BooleanValue,
        IntegerValue,
        RealValue,
        StringValue,
    )

T = TypeVar("T")


class IVariableValueVisitor(ABC, Generic[T]):
    """
    The interface to be implemented to instantiate the visitor pattern.

    Pass an instance to IVariableValue.accept().
    """

    # Single dispatch would make this prettier, but doesn't work with
    #  class methods until 3.8:
    #  https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_integer(self, value: IntegerValue) -> T:
        """
        Will be called if accept is called on an IntegerValue.

        Parameters
        ----------
        value The IntegerValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self, value: RealValue) -> T:
        """
        Will be called if accept is called on a RealValue.

        Parameters
        ----------
        value The RealValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean(self, value: BooleanValue) -> T:
        """
        Will be called if accept is called on a BooleanValue.

        Parameters
        ----------
        value The BooleanValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string(self, value: StringValue) -> T:
        """
        Will be called if accept is called on a StringValue.

        Parameters
        ----------
        value The StringValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_integer_array(self, value: IntegerArrayValue) -> T:
        """
        Will be called if accept is called on an IntegerArrayValue.

        Parameters
        ----------
        value The IntegerArrayValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self, value: FileValue) -> T:
        """
        Will be called if accept is called on an FileValue.

        Parameters
        ----------
        value The FileValue being visited

        Returns
        -------
        The result
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real_array(self, value: RealArrayValue) -> T:
        """
        Will be called if accept is called on a RealArrayValue.

        Parameters
        ----------
        value The RealArrayValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean_array(self, value: BooleanArrayValue) -> T:
        """
        Will be called if accept is called on a BooleanArrayValue.

        Parameters
        ----------
        value The BooleanArrayValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self, value: StringArrayValue) -> T:
        """
        Will be called if accept is called on a StringArrayValue.

        Parameters
        ----------
        value The StringArrayValue being visited.

        Returns
        -------
        The result.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self, value: FileArrayValue) -> T:
        """
        Will be called if accept is called on an FileArrayValue.

        Parameters
        ----------
        value The FileArrayValue being visited

        Returns
        -------
        The result
        """
        raise NotImplementedError
