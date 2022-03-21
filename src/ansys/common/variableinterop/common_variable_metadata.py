from abc import ABC, abstractmethod
from typing import Dict

from .variable_type import VariableType
from .variable_value import IVariableValue


class CommonVariableMetadata(ABC):
    """
    Common metadata for variables. It may be that many
    uses have additional metadata, but this core set
    is defined by the Ansys Interoperability Guidelines.
    It allows a common understanding between products of
    some high-use properties. It does not exclude defining
    additional or more specific metadata as needed.
    """

    def __init__(self) -> None:
        self._description: str = ""
        self._custom_metadata: Dict[str, IVariableValue] = {}

    @property
    def description(self) -> str:
        """A description of the variable"""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def custom_metadata(self) -> Dict[str, IVariableValue]:
        """Additional, custom metadata may be stored in this dictionary"""
        return self._custom_metadata

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
