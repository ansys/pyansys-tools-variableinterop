"""Definition of CommonVariableMetadata."""
from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from typing import Any, Dict

from overrides import overrides

from ansys.common.variableinterop import exceptions
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
        """Determine if a given object is equal to this metadata."""
        return self.equals(other)

    def equals(self, other: Any) -> bool:
        """Determine if a given object is equal to this metadata.

        Parameters
        ----------
        other Object to compare this object to.

        Returns
        -------
        True if metadata objects are equal, false otherwise.
        """
        equal: bool = (isinstance(other, CommonVariableMetadata) and
                       self.variable_type == other.variable_type and
                       self._description == other._description and
                       self._custom_metadata == other._custom_metadata)
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

    def runtime_convert(
            self,
            source: variable_value.IVariableValue) -> variable_value.IVariableValue:
        """
        Convert the value of the given variable value to the \
        appropriate type for this meta data.

        Parameters
        ----------
        source : IVariableValue
            value to convert

        Returns
        -------
        Value converted to the appropriate type.
        """
        from ansys.common.variableinterop import (
            array_value_conversion,
            array_values,
            file_array_value,
            file_value,
            scalar_value_conversion,
            scalar_values,
        )

        class __RuntimeConvertVisitor(
            ivariablemetadata_visitor.IVariableMetadataVisitor[
                    variable_value.IVariableValue]):

            # def __init__(self, src: variable_value.IVariableValue):
            #    self._source = src

            @overrides
            def visit_integer(self, metadata) -> scalar_values.IntegerValue:
                return scalar_value_conversion.to_integer_value(source)

            @overrides
            def visit_real(self, metadata) -> scalar_values.RealValue:
                return scalar_value_conversion.to_real_value(source)

            @overrides
            def visit_boolean(self, metadata) -> scalar_values.BooleanValue:
                return scalar_value_conversion.to_boolean_value(source)

            @overrides
            def visit_string(self, metadata) -> scalar_values.StringValue:
                return scalar_value_conversion.to_string_value(source)

            @overrides
            def visit_file(self, metadata) -> file_value.FileValue:
                raise exceptions.IncompatibleTypesException(
                    source.variable_type, variable_type_lib.VariableType.FILE)

            @overrides
            def visit_integer_array(self, metadata) -> array_values.IntegerArrayValue:
                return array_value_conversion.to_integer_array_value(source)

            @overrides
            def visit_real_array(self, metadata) -> array_values.RealArrayValue:
                return array_value_conversion.to_real_array_value(source)

            @overrides
            def visit_boolean_array(self, metadata) -> array_values.BooleanArrayValue:
                return array_value_conversion.to_boolean_array_value(source)

            @overrides
            def visit_string_array(self, metadata) -> array_values.StringArrayValue:
                return array_value_conversion.to_string_array_value(source)

            @overrides
            def visit_file_array(self, metadata) -> file_array_value.FileArrayValue:
                raise exceptions.IncompatibleTypesException(
                    source.variable_type, variable_type_lib.VariableType.FILE_ARRAY)

        visitor = __RuntimeConvertVisitor()
        return self.accept(visitor)

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
