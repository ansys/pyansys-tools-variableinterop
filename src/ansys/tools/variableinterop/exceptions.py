"""Custom Exception types."""

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
    The formatted error string.
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
