"""Definition of IVariableValue and related classes."""
from __future__ import annotations

from abc import ABC, abstractmethod

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

from .variable_type import VariableType


class IVariableValue(ABC):
    """Interface that defines the common behavior between variable types."""

    # equality definition here

    # hashcode definition here

    # clone here

    @abstractmethod
    def accept(
            self, visitor: ivariable_visitor.IVariableVisitor[ivariable_visitor.T]
    ) -> ivariable_visitor.T:
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
    def variable_type(self) -> VariableType:
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

    @staticmethod
    def from_api_string(var_type: VariableType, source: str) -> IVariableValue:
        """
        Create a value from an API string.

        Parameters
        ----------
        var_type the variable type
        source the string from which to convert

        Returns
        -------
        An IVariableValue implementation with the specified type

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
