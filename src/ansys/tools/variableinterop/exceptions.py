# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Provides custom exception types."""

from configparser import ConfigParser
import os
from typing import Optional, Union

from .variable_type import VariableType


def _error(name: str, *args: object) -> str:
    """
    Return a formatted error string from the ``strings.properties`` object.

    Parameters
    ----------
    name : str
        Name of the string in the properties file.
    *args : object
        Optional formatting arguments.

    Returns
    -------
        Formatted error string.
    """
    parser = ConfigParser()
    parser.read(os.path.join(os.path.dirname(__file__), "strings.properties"))
    return parser.get("Errors", name).format(*args)


class IncompatibleTypesException(BaseException):
    """Indicates that the types used in a conversion are incompatible."""

    def __init__(
        self,
        from_type: Union[VariableType, str],
        to_type: Union[VariableType, str],
    ):
        """
        Construct exception.

        Parameters
        ----------
        from_type : Union[VariableType, str]
            ``VariableType`` or string identifying the type to convert from.
        to_type : Union[VariableType, str]
            ``VariableType`` or string identifying the type to convert to.
        """
        self.from_type: Optional[VariableType]
        self.from_type_str: str
        self.to_type: Optional[VariableType]

        if isinstance(from_type, VariableType):
            self.from_type = from_type
            self.from_type_str = from_type.associated_type_name
        else:
            self.from_type = None
            self.from_type_str = from_type
        if isinstance(to_type, VariableType):
            self.to_type = to_type
            self.to_type_str = to_type.associated_type_name
        else:
            self.to_type = None
            self.to_type_str = to_type
        message: str = _error("ERROR_INCOMPATIBLE_TYPES", self.from_type_str, self.to_type_str)
        super().__init__(message)


class FormatException(BaseException):
    """Indicates that the string used to create a variable value was incorrectly
    formatted."""

    def __init__(self):
        """Construct exception."""
        message: str = _error("ERROR_FORMAT")
        super().__init__(message)


class ValueDeserializationUnsupportedException(Exception):
    """Indicates that deserializing a value is not allowed."""

    def __init__(self, message: str):
        """Construct a new instance."""
        super().__init__(message)
