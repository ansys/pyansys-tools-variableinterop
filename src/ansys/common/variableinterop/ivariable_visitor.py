from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.real_value as real_value

T = TypeVar("T")


class IVariableValueVisitor(ABC, Generic[T]):
    """
    The interface to be implemented to instantiate the visitor pattern. Pass an instance
    to IVariableValue.accept().
    """

    # Single dispatch would make this prettier, but doesn't work with
    #  class methods until 3.8:
    #  https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_int(self, value: integer_value.IntegerValue) -> T:
        """
        Will be called if accept is called on an IntegerValue

        Parameters
        ----------
        value The IntegerValue being visited

        Returns
        -------
        The result
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self, value: real_value.RealValue) -> T:
        """
        Will be called if accept is called on an RealValue

        Parameters
        ----------
        value The RealValue being visited

        Returns
        -------
        The result
        """
        raise NotImplementedError

    # TODO: Other types
