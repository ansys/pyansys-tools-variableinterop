"""Definition of CommonVariableMetadata."""
from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from typing import Dict

import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.variable_type as variable_type_lib
import ansys.common.variableinterop.variable_value as variable_value


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
        self._custom_metadata: Dict[str, variable_value.IVariableValue] = {}

    def __eq__(self, other):
        return self.are_equal(other)

    def are_equal(self, metadata: CommonVariableMetadata) -> bool:
        """Determine if a given metadata is equal to this metadata.

        Parameters
        ----------
        metadata Metadata to compare this object to.

        Returns
        -------
        True if metadata objects are equal, false otherwise.
        """
        equal: bool = (isinstance(metadata, CommonVariableMetadata) and
                       self.variable_type == metadata.variable_type and
                       self._description == metadata._description and
                       self._custom_metadata == metadata._custom_metadata)
        return equal

    def clone(self) -> CommonVariableMetadata:
        """Get a deep copy of this metadata."""
        return copy.deepcopy(self)

    @abstractmethod
    def accept(
            self,
            visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[ivariablemetadata_visitor.T]
    ) -> ivariablemetadata_visitor.T:
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
    def custom_metadata(self) -> Dict[str, variable_value.IVariableValue]:
        """Additional, custom metadata may be stored in this dictionary."""
        return self._custom_metadata

    @property
    @abstractmethod
    def variable_type(self) -> variable_type_lib.VariableType:
        """
        Variable type of this object.

        Returns
        -------
        The variable type of this object.
        """
        raise NotImplementedError
