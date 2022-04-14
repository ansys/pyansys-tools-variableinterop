"""Definition of IVariableValue and related classes."""
from __future__ import annotations

import copy
import random
from abc import ABC, abstractmethod
from typing import Tuple, TypeVar, Generic

import numpy as np
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


class CommonArrayValue(Generic[T], NDArray[T], IVariableValue, ABC):
    """Interface that defines common behavior for array types. Inherits ``IVariableValue``."""

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
