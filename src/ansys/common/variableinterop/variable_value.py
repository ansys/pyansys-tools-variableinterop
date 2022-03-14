"""
Definition of IVariableValue and related classes
"""
from __future__ import annotations
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
import numpy as np

# Used for the generic visitor pattern
from .variable_type import VariableType

T = TypeVar('T')


class IVariableValue(ABC):
    """Interface that defines the common behavior between variable types"""

    @abstractmethod
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
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


class IVariableValueVisitor(ABC, Generic[T]):
    """
    The interface to be implemented to instantiate the visitor pattern. Pass an instance
    to IVariableValue.accept().
    """

    # Single dispatch would make this prettier, but doesn't work with
    #  class methods until 3.8:
    #  https://docs.python.org/3/library/functools.html#functools.singledispatch

    @abstractmethod
    def visit_int(self, value: IntegerValue) -> T:
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
    def visit_real(self, value: RealValue) -> T:
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


# TODO: I'm used to languages like Java and C# which encourage a class per file.
#  What is best practice here?

class IntegerValue(np.int64, IVariableValue):
    """
    In Python IntegerValue is implemented by extending NumPy's int64 type. This means that
    they will decay naturally into numpy.int64 objects when using numpy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards. For
    example, when converting from real to integer, the value will be floored instead of
    rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        # inheritdoc (What is the correct way to do this?)
        return visitor.visit_int(self)

    def variable_type(self) -> VariableType:
        # inheritdoc (What is the correct way to do this?)
        return VariableType.INTEGER


class RealValue(np.float64, IVariableValue):
    """
    In Python RealValue is implemented by extending NumPy's float64 type. This means that
    they will decay naturally into numpy.float64 objects when using numpy's arithmetic
    operators. It also means that they inherit many of the numpy behaviors, which may be
    slightly different from the behaviors specified in the variable interop standards.
    For example, when converting from real to integer, the value will be floored instead
    of rounded. If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        # inheritdoc (What is the correct way to do this?)
        return visitor.visit_real(self)

    def variable_type(self) -> VariableType:
        # inheritdoc (What is the correct way to do this?)
        return VariableType.REAL
