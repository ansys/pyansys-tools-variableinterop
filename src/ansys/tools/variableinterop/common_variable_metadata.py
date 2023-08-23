"""Definition of CommonVariableMetadata."""
from __future__ import annotations

from abc import ABC, abstractmethod
import copy
from typing import Any, Dict, Type, TypeVar

from overrides import overrides

from ansys.tools.variableinterop import exceptions
import ansys.tools.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.tools.variableinterop.variable_type as variable_type_lib

from .variable_value import IVariableValue


class CommonVariableMetadata(ABC):
    """
    Common metadata for variables.

    It may be that many uses have additional metadata, but this core set is defined by
    the Ansys Interoperability Guidelines. It allows a common understanding between
    products of some high-use properties. It does not exclude defining additional or
    more specific metadata as needed.
    """

    def __init__(self) -> None:
        """Initialize all members."""
        self._description: str = ""
        self._custom_metadata: Dict[str, IVariableValue] = {}

    def __eq__(self, other):
        """Determine if a given object is equal to this metadata."""
        return self.equals(other)

    def equals(self, other: Any) -> bool:
        """
        Determine if a given object is equal to this metadata.

        Parameters
        ----------
        other : Any
            Object to compare this object to.

        Returns
        -------
        bool
            ``True`` if metadata objects are equal, ``False`` otherwise.
        """
        equal: bool = (
            isinstance(other, CommonVariableMetadata)
            and self.variable_type == other.variable_type
            and self._description == other._description
            and self._custom_metadata == other._custom_metadata
        )
        return equal

    def clone(self) -> CommonVariableMetadata:
        """Get a deep copy of this metadata."""
        return copy.deepcopy(self)

    @abstractmethod
    def accept(
        self,
        visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[ivariablemetadata_visitor.T],
    ) -> ivariablemetadata_visitor.T:
        """
        Invoke the visitor pattern of this object using the passed in visitor
        implementation.

        Parameters
        ----------
        visitor : IVariableMetadataVisitor[T]
            The visitor object to call.

        Returns
        -------
        T
            The results of the visitor invocation.
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
        value : str
            The new description to set.
        """
        self._description = value

    @property
    def custom_metadata(self) -> Dict[str, IVariableValue]:
        """Additional, custom metadata may be stored in this dictionary."""
        return self._custom_metadata

    def get_default_value(self) -> IVariableValue:
        """
        Get default value that should be used for variable describe by this metadata.

        The metadata may have set lower bound, upper bounds or
        enumerated values which restricts what are possible valid
        values. This method will select a valid default value.

        - If the type's default value (e.g. 0 or empty string) is a
          valid value for the metadata, use it.
        - else if metadata has enumerated values, select the first
          value in the enumerated values which is valid per the other
          restrictions.
        - else if metadata has a lower bound and is it is valid, use it.
        - else if metadata does not have a lower bound, but does have an
          upper bound, use upper bound.
        - else no value is valid, use the type's default value.
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

        class __DefaultValueVisitor(
            ivariablemetadata_visitor.IVariableMetadataVisitor[IVariableValue]
        ):
            """Metadata visitor to implement getting the default value."""

            @staticmethod
            def __get_str_enumerated_default(
                metadata: scalar_metadata.StringMetadata,
            ) -> scalar_values.StringValue:
                """
                For given StringMetadata, use enumerated values to get the default value
                to use for the associated variable.

                Parameters
                ----------
                metadata : StringMetadata
                    Metadata to use to generate default value.

                Returns
                -------
                StringValue
                    Default value to use for associated variable.
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
                For a numeric metadata (i.e. IntegerMetadata or RealMetadata) get the
                default value to use.

                Parameters
                ----------
                metadata : M
                    Metadata to use to generate default value.
                type_ : Type[T]
                    Type of the default value to generate.

                Returns
                -------
                T
                    Default value to use for associated variable.
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
        Convert the value of the given variable value to the appropriate type for this
        metadata.

        Parameters
        ----------
        source : IVariableValue
            value to convert

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

        class __RuntimeConvertVisitor(
            ivariablemetadata_visitor.IVariableMetadataVisitor[IVariableValue]
        ):
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
                    source.variable_type, variable_type_lib.VariableType.FILE
                )

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
                    source.variable_type, variable_type_lib.VariableType.FILE_ARRAY
                )

        visitor = __RuntimeConvertVisitor()
        return self.accept(visitor)

    @property
    @abstractmethod
    def variable_type(self) -> variable_type_lib.VariableType:
        """
        Variable type of this object.

        Returns
        -------
        VariableType
            The variable type of this object.
        """
        raise NotImplementedError
