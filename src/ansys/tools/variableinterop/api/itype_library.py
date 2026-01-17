# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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
"""Provides the ITypeLibrary abstraction."""

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Protocol, Set, Type

import numpy as np

# Names and types that are required
REAL_NAME = "Real"
REAL_TYPE = np.float64
INTEGER_NAME = "Integer"
INTEGER_TYPE = np.int64
BOOLEAN_NAME = "Boolean"
BOOLEAN_TYPE = bool
STRING_NAME = "String"
STRING_TYPE = str

RequiredTypes: dict[str, Type] = {
    REAL_NAME: REAL_TYPE,
    INTEGER_NAME: INTEGER_TYPE,
    BOOLEAN_NAME: BOOLEAN_TYPE,
    STRING_NAME: STRING_TYPE,
    #    "File",
    #    "Struct"
}
"""
The list of types that a type library must support, and what native type it is expected
to be able to convert to.

The meanings are:

* Real - 64 bit floating point number should be convertible to numpy.float64
* Integer - 64 bit integer number should be convertible to numpy.int64
* Boolean - Logical true/false should be convertible to bool
* String - Unicode string should be convertible to str
"""

TypesRequired: dict[Type, str] = {t: s for (s, t) in RequiredTypes.items()}
"""The reverse of ``RequiredTypes``, for each required native type, what is the name of
that type."""


class ITypeInformation(Protocol):
    """Defines a data type."""

    @property
    @abstractmethod
    def canonical_name(self) -> str:
        "Canonical name of the type"
        raise NotImplementedError

    @property
    @abstractmethod
    def aliases(self) -> Set[str]:
        """Set of aliases that are accepted for the type."""
        raise NotImplementedError

    @property
    @abstractmethod
    def type_description(self) -> str:
        """Detailed description of the type."""
        raise NotImplementedError

    @abstractmethod
    def get_ui_display_name(self, locale: str) -> str:
        """A UI display name in a given locale for the type."""
        raise NotImplementedError

    @property
    @abstractmethod
    def value_type(self) -> Type:
        """The Python type used for values of this type."""
        raise NotImplementedError

    @property
    @abstractmethod
    def metadata_type(self) -> Type:
        """The Python type used for metadata of this type."""
        raise NotImplementedError


@dataclass
class TypeCompatibility:
    """Assertions about how types behave when setting a value of one type to a value of
    a different type."""

    allowed: bool
    """Whether linking is allowed given the source and destination types."""

    lossy: bool
    """
    Whether this conversion may be lossy.

    For example, converting from real numbers to an integral type loses precision.
    Converting from 64-bit integral types to real types is also lossy because for large
    values there are more sig figs than most computer real types support.
    """

    runtime_checked: bool
    """
    Whether converting from the source to the destination type might throw an exception
    at runtime.

    This may be because there is some processing involved, such as converting a string
    to a number, or because there are limits, such as converting from a 32-bit number to
    a 64-bit number.
    """


INCOMPATIBLE = TypeCompatibility(False, False, False)
"""TypeCompatibility assertion that two types are not compatible at all."""


class ITypeLibrary(Protocol):
    """Defines a type library."""

    @property
    @abstractmethod
    def type_library_identifier(self) -> str:
        """
        A URI that uniquely identifies this type library.

        This URI does not have to point to anything or resolve to a valid document. It is used
        only as an identifier. The type names returned by `allowed_types` are only relevant
        within this URI namespace.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def allowed_types(self) -> Set[ITypeInformation]:
        """
        Gets the list of data types allowed by the type library.

        Every type library implementation must support the types from `RequiredTypes`.
        """
        raise NotImplementedError

    @abstractmethod
    def get_type(self, type_name: str) -> ITypeInformation:
        """
        Retrieves the type information for a type.

        Parameters
        ----------
        type_name : str
            Type name or alias to query

        Returns
        -------
        ITypeInformation
            Type information for the queried type

        Raises
        ------
        InvalidVariableTypeError
            If the type name is not a valid type for this type library
        """
        raise NotImplementedError

    @abstractmethod
    def is_linking_allowed(self, source_type: str, dest_type: str) -> TypeCompatibility:
        """
        Tests if the source type is valid as the source of data for the destination
        type.

        Parameters
        ----------
        source_type: str
            Source type to test
        dest_type: str
            Destination type to test

        Returns
        -------
        TypeCompatibility
            A `TypeCompatibility` object that describes whether the types are compatible.

        Raises
        ------
        InvalidVariableTypeError
            If the type name is not a valid type for this type library
        """
        raise NotImplementedError

    @abstractmethod
    def runtime_convert(self, source: Any, source_type: Type, dest_type: Type) -> Any:
        """
        Converts an instance of one type into another type.

        If the source and destination types are the same, it is fine to merely return
        the source unmodified.

        A default implementation of this method can be found on ``AbstractInitializerTypeLibrary``.

        Parameters
        ----------
        source: Any
            Source object to convert
        source_type: Type
            Type of data being passed as the source
        dest_type: Type
            Type of object to convert the source into

        Returns
        -------
        Any
            Source value converted to the destination type
        """
        raise NotImplementedError

    @abstractmethod
    def compute_safe_default_value(self, type_name: str, metadata: object) -> Optional[object]:
        """
        Given a metadata object from this type library, return the default value
        provided by that object.

        Parameters
        ----------
        type_name: str
            Type name associated with the metadata object.
        metadata: object
            Metadata object to inspect. The caller MUST pass an object that is an
            instance of the metadata type defined by this implementation for the
            passed `type_name`.

        Returns
        -------
        Optional[DEST_TYPE]
            Default value as specified or constrained in the metadata, or `None` if the
            metadata does not specify one. If the implementation returns a non-null value,
            it MUST be an instance of the value type specified by the metadata.
        """
        raise NotImplementedError

    @abstractmethod
    def value_to_byte_array(self, source_type: str, source: object) -> bytes:
        """
        Convert a value generated by this type system to a byte array.

        This conversion is used to support passing values "over the wire" to a remote system.
        Conversions of this type are surprisingly difficult to get right all the time,
        especially if the type system is available on multiple platforms.
        It is suggested to use a purpose-built external library such as protobuf for
        performing these conversions.

        Parameters
        ----------
        source_type: str
            Type of data being passed as the source
        source: object
            Source value object as created by this type system.

        Returns
        -------
        bytes
            Representation of the value as a byte array.
        """
        raise NotImplementedError

    @abstractmethod
    def byte_array_to_value(self, dest_type: str, source: bytes) -> object:
        """
        Convert a value generated by `value_to_byte_array` back into a value of the
        specified type.

        Type parameters are:

        * :any:`DEST_TYPE` - Type to deserialize to

        Parameters
        ----------
        dest_type: str
            Type of value to deserialize.
        source: bytes
            Bytes to convert.

        Returns
        -------
        object
            Deserialized value
        """
        raise NotImplementedError

    @abstractmethod
    def metadata_to_byte_array(self, source_type: str, source: object) -> bytes:
        """
        Convert a metadata object generated by this type system to a byte array.

        This conversion is used to support passing values "over the wire" to a remote system.
        Conversions of this type are surprisingly difficult to get right all the time,
        especially if the type system is available on multiple platforms.
        It is suggested to use a purpose-built external library such as protobuf for
        performing these conversions.

        Parameters
        ----------
        source_type: str
            Source type name as declared by this type system.
        source: object
            Source metadata object as created by this type system.

        Returns
        -------
        bytes
            Representation of the metadata as a byte array.
        """
        raise NotImplementedError

    @abstractmethod
    def byte_array_to_metadata(self, dest_type: str, source: bytes) -> object:
        """
        Convert a value generated by `metadata_to_byte_array` back into a metadata
        object of the specified type.

        Parameters
        ----------
        dest_type: str
            Type of metadata object to deserialize.
        source: bytes
            Bytes to convert.

        Returns
        -------
        object
            Deserialized value
        """
        raise NotImplementedError
