"""Definition of IVariableValue and related classes."""
from __future__ import annotations

from abc import ABC, abstractmethod

from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor, T
import ansys.common.variableinterop.variable_type as variable_type_lib


class IVariableValue(ABC):
    """Interface that defines the common behavior between variable types."""

    # equality definition here

    # hashcode definition here

    # clone here

    @abstractmethod
    def accept(
            self, visitor: IVariableValueVisitor[T]
    ) -> T:
        """
        Invoke the visitor pattern of this object using the passed in visitor implementation.

        Parameters
        ----------
        visitor The visitor object to call

        Returns
        -------
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
        The variable type of this object
        """
        raise NotImplementedError

    @abstractmethod
    def to_api_string(self) -> str:
        """
        Convert this value to an API string.

        Returns
        -------
        A string appropriate for use in files and APIs.
        """
        raise NotImplementedError

    @abstractmethod
    def from_api_string(self, value: str) -> None:
        """
        Convert an API string back into a value.

        Parameters
        ----------
        value
        The string to convert.
        """
        raise NotImplementedError

    # to_formatted_string here

    # from_formatted_string here

    @abstractmethod
    def get_modelcenter_type(self) -> str:
        """
        Get the ModelCenter type string for this value type.

        Returns
        -------
        String to use as the type for a variable on the ModelCenter API.
        """
        raise NotImplementedError
