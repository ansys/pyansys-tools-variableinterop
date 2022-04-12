"""Definition of IVariableValueVisitor."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    import ansys.common.variableinterop.boolean_array_value as boolean_array_value
    import ansys.common.variableinterop.boolean_value as boolean_value
    import ansys.common.variableinterop.integer_array_value as integer_array_value
    import ansys.common.variableinterop.integer_value as integer_value
    import ansys.common.variableinterop.real_array_value as real_array_value
    import ansys.common.variableinterop.real_value as real_value
    import ansys.common.variableinterop.string_array_value as string_array_value
    import ansys.common.variableinterop.string_value as string_value


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
    def visit_integer(self, value: integer_value.IntegerValue) -> T:
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
    def visit_real(self, value: real_value.RealValue) -> T:
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
    def visit_boolean(self, value: boolean_value.BooleanValue) -> T:
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
    def visit_string(self, value: string_value.StringValue) -> T:
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
    def visit_integer_array(self, value: integer_array_value.IntegerArrayValue) -> T:
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
    def visit_real_array(self, value: real_array_value.RealArrayValue) -> T:
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
    def visit_boolean_array(self, value: boolean_array_value.BooleanArrayValue) -> T:
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
    def visit_string_array(self, value: string_array_value.StringArrayValue) -> T:
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