"""
Definition of IVariableValue and related classes
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

from .variable_type import VariableType


class IVariableValue(ABC):
    """Interface that defines the common behavior between variable types"""

    @abstractmethod
    def accept(
        self, visitor: ivariable_visitor.IVariableVisitor[ivariable_visitor.T]
    ) -> ivariable_visitor.T:
        """
        Invoke the visitor pattern of this object using the passed in visitor implementation

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
        The variable type of this object

        Returns
        -------
        The variable type of this object
        """
        raise NotImplementedError
