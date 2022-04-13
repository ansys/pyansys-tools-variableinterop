"""
Custom Exception types.
"""

from configparser import ConfigParser
import os
from typing import Union

import ansys.common.variableinterop.variable_type as variable_type


def _error(name: str, *args: object) -> str:
    """Return a formatted error string from strings.properties.

    Parameters
    ----------
    name Name of the string in the properties file
    args Optional formatting arguments

    Returns
    -------
    The formatted error string.
    """

    parser = ConfigParser()
    parser.read(os.path.join(os.path.dirname(__file__), "strings.properties"))
    return parser.get("Errors", name).format(*args)


class IncompatibleTypesException(BaseException):
    """Exception raised when attempting to convert from one IVariableValue to an
    incompatible type."""
    def __init__(
            self,
            from_type: Union[variable_type.VariableType, str],
            to_type: Union[variable_type.VariableType, str]):
        """
        Construct exception.
        :param from_type a VariableType or a string identifying the type converting from.
        :param to_type a VariableType or a string identifying the type converting to.
        """
        if isinstance(from_type, variable_type.VariableType):
            self.from_type: variable_type.VariableType = from_type
            self.from_type_str: str = from_type.associated_type_name
        else:
            self.from_type = None
            self.from_type_str: str = from_type
        if isinstance(to_type, variable_type.VariableType):
            self.to_type: variable_type.VariableType = to_type
            self.to_type_str: str = to_type.associated_type_name
        else:
            self.to_type = None
            self.to_type_str: str = to_type
        self.message = _error("ERROR_INCOMPATIBLE_TYPES", self.from_type_str, self.to_type_str )
        super().__init__(self.message)
