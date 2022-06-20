"""Definition of IVariableValue and related classes."""
from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from typing import Generic, Tuple, TypeVar

from numpy.typing import NDArray

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_type as variable_type_lib

T = TypeVar("T")


class IVariableValue(ABC):
    """Interface that defines the common behavior between variable types."""

    def clone(self) -> IVariableValue:
        """Get a deep copy of this value."""
        return copy.deepcopy(self)

    @abstractmethod
    def accept(
        self, visitor: ivariable_visitor.IVariableValueVisitor[ivariable_visitor.T]
    ) -> ivariable_visitor.T:
        """
        Invoke the visitor pattern of this object using the passed in visitor implementation.

        Parameters
        ----------
        visitor
            The visitor object to call

        Returns
        -------
        T
            The results of the visitor invocation
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
    def to_api_string(self) -> str:
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
        locale_name
            The locale to format in.

        Returns
        -------
        str
            A string appropriate for use in user facing areas.
        """
        raise NotImplementedError


class CommonArrayValue(Generic[T], NDArray[T], IVariableValue, ABC):
    """Interface that defines common behavior for array types. Inherits ``IVariableValue``."""

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


class VariableState:
    """Bundles a variable state with a validity flag."""

    def __init__(self, value: IVariableValue, is_valid: bool):
        """
        Initialize a new instance.

        Parameters
        ----------
        value : IVariableValue
            The variable value.
        is_valid : bool
            The validity flag (true indicates the value is valid).
        """
        self.__value = value
        self.__is_valid = is_valid

    @property
    def value(self) -> IVariableValue:
        """Get the variable value."""
        return self.__value

    @property
    def is_valid(self) -> bool:
        """Get the validity flag. True indicates the value is valid."""
        return self.__is_valid

    @property
    def safe_value(self) -> IVariableValue:
        """
        Get the variable value.

        VariableValueInvalidError is raised if the variable value is
        not valid.
        """
        if self.__is_valid:
            return self.__value
        else:
            raise VariableValueInvalidError()

    def clone(self) -> VariableState:
        """
        Clone this instance.

        The returned instance contains a clone of this instance's value.

        Returns
        -------
        VariableState
            a deep copy of this instance
        """
        return VariableState(self.__value.clone(), self.__is_valid)
