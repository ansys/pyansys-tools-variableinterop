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
from typing import Any, Optional, Protocol, Set, Type, TypeVar, Union
import numpy as np

REAL_NAME="Real"
REAL_TYPE=np.float64
INTEGER_NAME="Integer"
INTEGER_TYPE=np.int64
BOOLEAN_NAME="Boolean"
BOOLEAN_TYPE=bool
STRING_NAME="String"
STRING_TYPE=str

RequiredTypes : dict[str, Type] = {
    REAL_NAME: REAL_TYPE,
    INTEGER_NAME: INTEGER_TYPE,
    BOOLEAN_NAME: BOOLEAN_TYPE,
    STRING_NAME: STRING_TYPE,
#    "File",
#    "Struct"
    }
"""
The list of types that a type library must support.

The meanings are:

* Real - 64 bit floating point number
* Integer - 64 bit integer number
* Boolean - Logical true/false
* String - Unicode string

"""

TypesRequired: dict[Type, str] = {t: s for (s,t) in RequiredTypes.items()}

class ITypeInformation(Protocol):
    """Defines a data type"""

    @property
    @abstractmethod
    def canonical_name(self) -> str:
        "Canonical name of the type"
        raise NotImplementedError
    
    @property
    @abstractmethod
    def aliases(self) -> Set[str]:
        """Set of aliases for the type"""
        raise NotImplementedError
    
    @property
    @abstractmethod
    def type_description(self) -> str:
        """Detailed description of the type"""
        raise NotImplementedError
    
    @abstractmethod
    def get_ui_display_name(self, locale: str) -> str:
        """Detailed description of the type"""
        raise NotImplementedError

    @property
    @abstractmethod
    def value_type(self) -> Type:
        """The Python type used for values of this type"""
        raise NotImplementedError

    @property
    @abstractmethod
    def metadata_type(self) -> Type:
        """The Python type used for metadata of this type"""
        raise NotImplementedError

@dataclass
class TypeCompatibility:
    """Assertions about how types behave when setting a value of one type to a value of a different type"""

    allowed: bool
    """Whether linking is allowed given the source and destination types"""

    lossy: bool
    """
    Whether this conversion may be lossy.
     
    For example, converting from real numbers to an integral type loses precision. Converting
    from 64-bit integral types to real types is also lossy because for large values there are
    more sig figs than most computer real types support.
    """

    runtime_checked: bool
    """
    Whether converting from the source to the destination type might throw an exception at runtime.
     
    This may be because there is some processing involved, such as converting a string to
    a number, or because there are limits, such as converting from a 32-bit number to a 64-bit number.
    """

INCOMPATIBLE = TypeCompatibility(False, False, False)

SOURCE_TYPE = TypeVar('SOURCE_TYPE')
"""Type variable representing the actual type library type for a source parameter"""
DEST_TYPE = TypeVar('DEST_TYPE')
"""Type variable representing the actual type library type for a destination parameter or return value"""
METADATA_TYPE = TypeVar('METADATA_TYPE')
"""Type variable representing the actual type library type for a variable's metadata"""

class ITypeLibrary(Protocol):
    """Defines a type library"""

    @property
    @abstractmethod
    def type_library_identifier(self) -> str:
        """A URI that uniquely identifies this type library.
        
        This URI does not have to point to anything or resolve to a valid document. It is used only as an
        identifier. The type names returned by `allowed_types` are only relevant within this URI namespace.
        """
        raise NotImplementedError
    
    @property
    @abstractmethod
    def allowed_types(self) -> Set[ITypeInformation]:
        """ Gets the list of data types allowed by the type library.
         
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
            The type name or alias to query

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
        Tests if the source type is valid as the source of data for the destination type.

        Parameters
        ----------
        source_type: str
            The source type to test
        dest_type: str
            The destination type to test

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

        Parameters
        ----------
        source: Any
            Source object to convert
        source_type: str
            Type of data being passed as the source
        dest_type: str
            Type of object to convert the source into
        
        Returns
        -------
        Any
            Source value converted to the destination type
        """
        raise NotImplementedError

    @abstractmethod
    def compute_safe_default_value(self, metadata: METADATA_TYPE) -> Optional[DEST_TYPE]:
        """
        Given a metadata object from this type library, return the default value provided by that object

        Type parameters are"

        * :any:`METADATA_TYPE` - Type of metadata object
        * :any:`DEST_TYPE` - Value type for the given metadata type
        
        Parameters
        ----------
        metadata: METADATA_TYPE
            Metadata object to inspect

        Returns
        -------
        Optional[DEST_TYPE]
            Default value as specified or constrainted in the metadata, or `None` if the metadata does
            not specify one. If the implementation returns a non-null value, it MUST be an instance of
            the value type specified by the metadata.
        """
        raise NotImplementedError
    
    @abstractmethod
    def value_to_byte_array(self, source: SOURCE_TYPE, source_type: str) -> bytes:
        """
        Convert a value generated by this type system to a byte array.

        This conversion is used to support passing values "over the wire" to a remote system.
        Conversions of this type are surprisingly difficult to get right all the time,
        especially if the type system is available on multiple platforms.
        It is suggested to use a purpose-built external library such as protobuf for
        performing these conversions.

        Type parameters are:

        * :any:`SOURCE_TYPE` - Type of the source object. Must be a type supported by this type library.

        Parameters
        ----------
        source: SOURCE_TYPE
            Source value object as created by this type system.
        source_type: str
            Type of data being passed as the source

        Returns
        -------
        bytes
            Representation of the value as a byte array.
        """
        raise NotImplementedError
    
    @abstractmethod
    def byte_array_to_value(self, dest_type: str, source: bytes) -> DEST_TYPE:
        """
        Convert a value generated by `value_to_byte_array` back into a value of the specified type.

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
        DEST_TYPE
            Deserialized value
        """
        raise NotImplementedError
    
    @abstractmethod
    def metadata_to_byte_array(self, source: SOURCE_TYPE) -> bytes:
        """
        Convert a metadata object generated by this type system to a byte array.

        This conversion is used to support passing values "over the wire" to a remote system.
        Conversions of this type are surprisingly difficult to get right all the time,
        especially if the type system is available on multiple platforms.
        It is suggested to use a purpose-built external library such as protobuf for
        performing these conversions.

        Type parameters are:

        * :any:`SOURCE_TYPE` - Type of the source metadata object. Must be a type supported by this type library.
        
        Parameters
        ----------
        source: SOURCE_TYPE
            Source metadata object as created by this type system.
        
        Returns
        -------
        bytes
            Representation of the metadata as a byte array.
        """
        raise NotImplementedError
    
    @abstractmethod
    def byte_array_to_metadata(self, dest_type: str, source: bytes) -> DEST_TYPE:
        """
        Convert a value generated by `metadata_to_byte_array` back into a metadata object of the specified type.

        Type parameters are:
        
        * :any:`DEST_TYPE` - Type to deserialize to

        Parameters
        ----------
        dest_type: str
            Type of metadata object to deserialize.
        source: bytes
            Bytes to convert.
                
        Returns
        -------
        DEST_TYPE
            Deserialized value
        """
        raise NotImplementedError
    
    # @abstractmethod
    # def value_to_native_double(self, value: SOURCE_TYPE) -> float:
    #     """
    #     Convert a value generated by this type library of the "Real" type to a Python `float`.
         
    #     The implementation must be able to perform this conversion when provided with an object
    #     it uses to represent values of the "Real" type.
    #     The implementation may perform this conversion when provided with an object that is not an instance of
    #     the "Real" type, but when the conversion, but only if the conversion can be performed losslessly.
    #     If the conversion would be lossy, the implementation must throw an exception.

    #     Type parameters are:
        
    #     * :any:`SOURCE_TYPE` - Type of the value object as defined by the type library
        
    #     Parameters
    #     ----------
    #     value: SOURCE_TYPE
    #         Value to convert.

    #     Returns
    #     -------
    #     float
    #         Value as a Python `float`

    #     Raises
    #     ------
    #     TypeError 
    #         When the conversion cannot be performed, either because the conversion is
    #         generally not possible or because the conversion would be lossy.
    #     """
    #     raise NotImplementedError
    
    # @abstractmethod
    # def value_to_native_int(self, value: SOURCE_TYPE) -> int:
    #     """
    #     Convert a value generated by this type library of the "Integer" type to a Python `int`.
         
    #     The implementation must be able to perform this conversion when provided with an object
    #     it uses to represent values of the "Integer" type.
    #     The implementation may perform this conversion when provided with an object that is not an instance of
    #     the "Integer" type, but when the conversion, but only if the conversion can be performed losslessly.
    #     If the conversion would be lossy, the implementation must throw an exception.

    #     Type parameters are:
        
    #     * :any:`SOURCE_TYPE` - Type of the value object as defined by the type library
        

    #     Parameters
    #     ----------
    #     value: SOURCE_TYPE
    #         Value to convert.

    #     Returns
    #     -------
    #     int
    #         Value as a Python `int`

    #     Raises
    #     ------
    #     TypeError 
    #         When the conversion cannot be performed, either because the conversion is
    #         generally not possible or because the conversion would be lossy.
    #     """
    #     raise NotImplementedError

    # @abstractmethod
    # def value_to_native_str(self, value: SOURCE_TYPE) -> str:
    #     """
    #     Convert a value generated by this type library of the "String" type to a Python `str`.
         
    #     The implementation must be able to perform this conversion when provided with an object
    #     it uses to represent values of the "String" type.
    #     The implementation may perform this conversion when provided with an object that is not an instance of
    #     the "String" type, but when the conversion, but only if the conversion can be performed losslessly.
    #     If the conversion would be lossy, the implementation must throw an exception.

    #     Type parameters are:
        
    #     * :any:`SOURCE_TYPE` - Type of the value object as defined by the type library
        
    #     Parameters
    #     ----------
    #     value: SOURCE_TYPE
    #         Value to convert.

    #     Returns
    #     -------
    #     str
    #         Value as a Python `str`

    #     Raises
    #     ------
    #     TypeError 
    #         When the conversion cannot be performed, either because the conversion is
    #         generally not possible or because the conversion would be lossy.
    #     """
    #     raise NotImplementedError        
    
    # @abstractmethod
    # def value_to_native_bool(self, value: SOURCE_TYPE) -> bool:
    #     """
    #     Convert a value generated by this type library of the "Boolean" type to a Python `bool`.
         
    #     The implementation must be able to perform this conversion when provided with an object
    #     it uses to represent values of the "Boolean" type.
    #     The implementation may perform this conversion when provided with an object that is not an instance of
    #     the "Boolean" type, but when the conversion, but only if the conversion can be performed losslessly.
    #     If the conversion would be lossy, the implementation must throw an exception.

    #     Type parameters are:
        
    #     * :any:`SOURCE_TYPE` - Type of the value object as defined by the type library
        
    #     Parameters
    #     ----------
    #     value: SOURCE_TYPE
    #         Value to convert.

    #     Returns
    #     -------
    #     bool
    #         Value as a Python `bool`

    #     Raises
    #     ------
    #     TypeError 
    #         When the conversion cannot be performed, either because the conversion is
    #         generally not possible or because the conversion would be lossy.
    #     """
    #     raise NotImplementedError
    
    # @abstractmethod
    # def value_from_native_double(self, value: float) -> DEST_TYPE:
    #     """
    #     Given a Python `float`, create an instance of this type library's object for the "Real" type with the equivalent value.

    #     Type parameters are:
        
    #     * :any:`DEST_TYPE` - Type for "Real" values from the type library.

    #     Parameters
    #     ----------
    #     value: float
    #         Value to convert.
                
    #     Returns
    #     -------
    #     DEST_TYPE
    #         Type library's object for a "Real" value with the same value.
    #     """
    #     raise NotImplementedError
    
    # @abstractmethod
    # def value_from_native_int(self, value: int) -> DEST_TYPE:
    #     """
    #     Given a Python `int`, create an instance of this type library's object for the "Integer" type with the equivalent value.

    #     Type parameters are:
        
    #     * :any:`DEST_TYPE` - Type for "Integer" values from the type library.
        
    #     Parameters
    #     ----------
    #     value: int
    #         Value to convert.
        
    #     Returns
    #     -------
    #     DEST_TYPE
    #         Type library's object for a "Integer" value with the same value.
    #     """
    #     raise NotImplementedError

    # @abstractmethod
    # def value_from_native_str(self, value: str) -> DEST_TYPE:
    #     """
    #     Given a Python `str`, create an instance of this type library's object for the "String" type with the equivalent value.

    #     Type parameters are:
        
    #     * :any:`DEST_TYPE` - Type for "String" values from the type library.

    #     Parameters
    #     ----------
    #     value: str
    #         Value to convert.
        
    #     Returns
    #     -------
    #     DEST_TYPE
    #         Type library's object for a "String" value with the same value.
    #     """
    #     raise NotImplementedError

    # @abstractmethod
    # def value_from_native_bool(self, value: bool) -> DEST_TYPE:
    #     """
    #     Given a Python `bool`, create an instance of this type library's object for the "Boolean" type with the equivalent value.

    #     Type parameters are:
        
    #     * :any:`DEST_TYPE` - Type for "Boolean" values from the type library.
        
    #     Parameters
    #     ----------
    #     value: bool
    #         Value to convert.
        
    #     Returns
    #     -------
    #     DEST_TYPE
    #         Type library's object for a "Boolean" value with the same value.
    #     """
    #     raise NotImplementedError            