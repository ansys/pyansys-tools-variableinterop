"""Definition of CommonVariableMetadata."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict

from .variable_type import VariableType
from .variable_value import IVariableValue


class CommonVariableMetadata(ABC):
    """
    Common metadata for variables.

    It may be that many uses have additional metadata, but this core
    set is defined by the Ansys Interoperability Guidelines.
    It allows a common understanding between products of
    some high-use properties. It does not exclude defining
    additional or more specific metadata as needed.
    """

    def __init__(self) -> None:
        """Initialize all members."""
        self._description: str = ""
        self._custom_metadata: Dict[str, IVariableValue] = {}

    # equality definition here

    # clone here

    # accept here

    @property
    def description(self) -> str:
        """Get the description of the variable."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Set the description of the variable.

        Parameters
        ----------
        value
        The new description to set.
        """
        self._description = value

    @property
    def custom_metadata(self) -> Dict[str, IVariableValue]:
        """Additional, custom metadata may be stored in this dictionary."""
        return self._custom_metadata

    @property
    @abstractmethod
    def variable_type(self) -> VariableType:
        """
        Variable type of this object.

        Returns
        -------
        The variable type of this object.
        """
        raise NotImplementedError
