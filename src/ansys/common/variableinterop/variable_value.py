"""Definition of IVariableValue and related classes."""
from __future__ import annotations

import copy
import random
from abc import ABC, abstractmethod
import copy
import random
from typing import Generic, Tuple, TypeVar

import numpy as np
from numpy.typing import NDArray
from overrides import overrides

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
    def to_formatted_string(self, locale_name: str) -> str:
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

    @overrides
    def __hash__(self) -> int:
        flat: np.flatiter = self.flat
        length: int = len(flat)

        # Sample from array data at up to 16 pseudo-random indices
        num_samples = min(16, length)
        if length <= 16:
            indices = range(length)
        else:
            rand_generator = random.Random(42)
            indices = set()
            while len(indices) < num_samples:
                indices.add(rand_generator.randint(0, length-1))

        # Simple hash calculation
        hash_ = 0
        for i in indices:
            hash_ = (hash_ * 17 + hash(flat[i])) % 2147483648  # signed int32 max value

        return hash_

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
