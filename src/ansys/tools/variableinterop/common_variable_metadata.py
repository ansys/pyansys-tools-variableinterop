# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Defines the ``CommonVariableMetadata`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from typing import Any, Dict, Type, TypeVar

from overrides import overrides

from .exceptions import IncompatibleTypesException
from .ivariablemetadata_visitor import IVariableMetadataVisitor, T
from .variable_type import VariableType
from .variable_value import IVariableValue


class CommonVariableMetadata(ABC):
    """
    Provides metadata common to all variables.

    While users may have additional metadata, this core set is defined by Ansys
    interoperability guidelines to allow a common understanding between products of some
    high-use properties. These guidelines do not exclude defining additional or more
    specific metadata as needed.
    """

    variable_type_json_key = "type"
    """The JSON key for the variable type."""

    _description_json_key = "description"
    _custom_metadata_json_key = "customMetadata"

    def __init__(self) -> None:
        """Initialize all members."""
        self._description: str = ""
        self._custom_metadata: Dict[str, IVariableValue] = {}

    def __eq__(self, other):
        """Determine if the object is equal to the metadata."""
        return self.equals(other)

    def equals(self, other: Any) -> bool:
        """
        Determine if the object is equal to the metadata.

        Parameters
        ----------
        other : Any
            Other object to compare this object to.

        Returns
        -------
        bool
            ``True`` if the metadata objects are equal, ``False`` otherwise.
        """
        equal: bool = (
            isinstance(other, CommonVariableMetadata)
            and self.variable_type == other.variable_type
            and self._description == other._description
            and self._custom_metadata == other._custom_metadata
        )
        return equal

    def clone(self) -> CommonVariableMetadata:
        """Get a deep copy of the metadata."""
        return copy.deepcopy(self)

    @abstractmethod
    def accept(
        self,
        visitor: IVariableMetadataVisitor[T],
    ) -> T:
        """
        Invoke the visitor pattern of this object using the passed-in visitor
        implementation.

        Parameters
        ----------
        visitor : IVariableMetadataVisitor[T]
            Visitor object to call.

        Returns
        -------
        T
            Results of the visitor invocation.
        """
        raise NotImplementedError  # pragma: nocover

    @property
    def description(self) -> str:
        """Description of the variable."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Set the description of the variable.

        Parameters
        ----------
        value : str
            New description.
        """
        self._description = value

    @property
    def custom_metadata(self) -> Dict[str, IVariableValue]:
        """Custom metadata stored in a dictionary."""
        return self._custom_metadata

    def get_default_value(self) -> IVariableValue:
        """
        Get the default value that should be used for a variable described by this
        metadata.

        The metadata may have set the lower bound, upper bound, or
        enumerated values, which restricts what values are valid. This
        method selects a valid default value.

        - If the type's default value (such as ``0`` or an empty string) is a
          valid value for the metadata, use it.
        - If the metadata has enumerated values, select the first
          enumerated value that is valid per the other restrictions.
        - If the metadata has a lower bound and it is valid, use it.
        - If metadata does not have a lower bound but does have an
          upper bound, use the upper bound.
        - If no value is valid, use the type's default value.
        """
        from ansys.tools.variableinterop import (
            array_metadata,
            array_values,
            file_array_metadata,
            file_array_value,
            file_metadata,
            file_value,
            scalar_metadata,
            scalar_values,
        )

        class __DefaultValueVisitor(IVariableMetadataVisitor[IVariableValue]):
            """Implements the metadata visitor for getting the default value."""

            @staticmethod
            def __get_str_enumerated_default(
                metadata: scalar_metadata.StringMetadata,
            ) -> scalar_values.StringValue:
                """
                For the given ``StringMetadata`` value, use enumerated values to get the
                default value to use for the associated variable.

                Parameters
                ----------
                metadata : StringMetadata
                    Metadata to use to generate the default value.

                Returns
                -------
                StringValue
                    Default value to use for the associated variable.
                """
                default_value: scalar_values.StringValue = scalar_values.StringValue()
                if metadata.enumerated_values is not None and len(metadata.enumerated_values):
                    if default_value not in metadata.enumerated_values:
                        default_value = metadata.enumerated_values[0]
                return default_value

            M = TypeVar("M", scalar_metadata.IntegerMetadata, scalar_metadata.RealMetadata)
            T = TypeVar("T", scalar_values.IntegerValue, scalar_values.RealValue)

            @staticmethod
            def __get_numeric_default(metadata: M, type_: Type[T]) -> T:
                """
                For a numeric metadata (``IntegerMetadata`` or ``RealMetadata`` type),
                get the default value to use for the associated variable.

                Parameters
                ----------
                metadata : M
                    Metadata to use to generate the default value.
                type_ : Type[T]
                    Type of the default value to generate.

                Returns
                -------
                T
                    Default value to use for the associated variable.
                """
                default_value = type_()
                if metadata.enumerated_values is not None and len(metadata.enumerated_values):
                    # enumerated values are defined
                    # if default value is not valid
                    if (
                        default_value not in metadata.enumerated_values
                        or (
                            metadata.lower_bound is not None
                            and default_value < metadata.lower_bound
                        )
                        or (
                            metadata.upper_bound is not None
                            and metadata.upper_bound < default_value
                        )
                    ):
                        # find the first enumerated value that is valid
                        # if one does not exist, use default value anyway
                        default_value = next(
                            (
                                e
                                for e in metadata.enumerated_values
                                if (metadata.lower_bound is None or metadata.lower_bound <= e)
                                and (metadata.upper_bound is None or e <= metadata.upper_bound)
                            ),
                            default_value,
                        )
                else:
                    # no enumerated values are defined
                    # if default value is not valid
                    if (
                        metadata.lower_bound is not None and default_value < metadata.lower_bound
                    ) or (
                        metadata.upper_bound is not None and metadata.upper_bound < default_value
                    ):
                        # default is not valid.
                        # if have a lower_bound
                        if metadata.lower_bound is not None:
                            # if lower_bound is valid, use it
                            if (
                                metadata.upper_bound is None
                                or metadata.lower_bound <= metadata.upper_bound
                            ):
                                default_value = metadata.lower_bound
                        # else if have an upper_bound, use it
                        elif metadata.upper_bound is not None:
                            default_value = metadata.upper_bound
                        # else nothing is valid, just use default value
                    # else default_value is valid, use it

                return default_value

            @overrides
            def visit_integer(
                self, metadata: scalar_metadata.IntegerMetadata
            ) -> scalar_values.IntegerValue:
                return self.__get_numeric_default(metadata, scalar_values.IntegerValue)

            @overrides
            def visit_real(self, metadata: scalar_metadata.RealMetadata) -> scalar_values.RealValue:
                return self.__get_numeric_default(metadata, scalar_values.RealValue)

            @overrides
            def visit_boolean(
                self, metadata: scalar_metadata.BooleanMetadata
            ) -> scalar_values.BooleanValue:
                return scalar_values.BooleanValue()

            @overrides
            def visit_string(
                self, metadata: scalar_metadata.StringMetadata
            ) -> scalar_values.StringValue:
                return self.__get_str_enumerated_default(metadata)

            @overrides
            def visit_file(self, metadata: file_metadata.FileMetadata) -> file_value.FileValue:
                return file_value.EMPTY_FILE

            @overrides
            def visit_integer_array(
                self, metadata: array_metadata.IntegerArrayMetadata
            ) -> array_values.IntegerArrayValue:
                return array_values.IntegerArrayValue()

            @overrides
            def visit_real_array(
                self, metadata: array_metadata.RealArrayMetadata
            ) -> array_values.RealArrayValue:
                return array_values.RealArrayValue()

            @overrides
            def visit_boolean_array(
                self, metadata: array_metadata.BooleanArrayMetadata
            ) -> array_values.BooleanArrayValue:
                return array_values.BooleanArrayValue()

            @overrides
            def visit_string_array(
                self, metadata: array_metadata.StringArrayMetadata
            ) -> array_values.StringArrayValue:
                return array_values.StringArrayValue()

            @overrides
            def visit_file_array(
                self, metadata: file_array_metadata.FileArrayMetadata
            ) -> file_array_value.FileArrayValue:
                return file_array_value.FileArrayValue()

        visitor = __DefaultValueVisitor()
        return self.accept(visitor)

    def runtime_convert(self, source: IVariableValue) -> IVariableValue:
        """
        Convert the value of the variable to the appropriate type for this metadata.

        Parameters
        ----------
        source : IVariableValue
            Value to convert

        Returns
        -------
        IVariableValue
            Value converted to the appropriate type.
        """
        from ansys.tools.variableinterop import (
            array_value_conversion,
            array_values,
            file_array_value,
            file_value,
            scalar_value_conversion,
            scalar_values,
        )

        class __RuntimeConvertVisitor(IVariableMetadataVisitor[IVariableValue]):
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
                raise IncompatibleTypesException(source.variable_type, VariableType.FILE)

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
                raise IncompatibleTypesException(source.variable_type, VariableType.FILE_ARRAY)

        visitor = __RuntimeConvertVisitor()
        return self.accept(visitor)

    @property
    @abstractmethod
    def variable_type(self) -> VariableType:
        """
        Variable type of the object.

        Returns
        -------
        VariableType
            Variable type of the object.
        """
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Creates a dictionary representation of this object suitable for JSON
        serialization.

        Returns
        -------
        dict
            The generated dictionary
        """
        from .ivariable_type_pseudovisitor import vartype_accept
        from .variable_value_json_visitors import VariableTypeToJsonVisitor

        type_visitor = VariableTypeToJsonVisitor()
        result = {
            CommonVariableMetadata.variable_type_json_key:
            vartype_accept(type_visitor, self.variable_type),  # fmt: skip
        }
        if len(self._description) > 0 and not str.isspace(self._description):
            result[CommonVariableMetadata._description_json_key] = self._description
        # LTTODO: implement custom metadata
        return result

    @classmethod
    @abstractmethod
    def from_dict(cls, data) -> "CommonVariableMetadata":
        """
        Creates a new metadata object from the data from a call to to_dict().

        Parameters
        ----------
        data
            The serialized dictionary data.

        Returns
        -------
        CommonVariableMetadata
            The new metadata object.
        """
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def _from_dict(data: dict) -> tuple[str, dict[str, VariableType]]:
        """
        Helper method for subclasses to extract common metadata information from a JSON
        dictionary.

        Parameters
        ----------
        data
            The serialized dictionary data.

        Returns
        -------
        tuple[str, dict[str, variable_type_lib.VariableType]]
            A tuple containing the description and custom metadata dictionary.
        """
        description: str = data.get(CommonVariableMetadata._description_json_key, "")

        # LTTODO: implement custom metadata
        custom_metadata = {}

        return description, custom_metadata
