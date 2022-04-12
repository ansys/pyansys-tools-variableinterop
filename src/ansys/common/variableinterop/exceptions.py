"""
Custom Exception types.
"""

import os
from configparser import ConfigParser
from typing import Dict

from ansys.common.variableinterop.boolean_array_value import BooleanArrayValue
from ansys.common.variableinterop.boolean_value import BooleanValue
from ansys.common.variableinterop.integer_array_value import IntegerArrayValue
from ansys.common.variableinterop.integer_value import IntegerValue
from ansys.common.variableinterop.real_array_value import RealArrayValue
from ansys.common.variableinterop.real_value import RealValue
from ansys.common.variableinterop.string_array_value import StringArrayValue
from ansys.common.variableinterop.string_value import StringValue
from ansys.common.variableinterop.variable_type import VariableType


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

    def __init__(self, from_type: VariableType, to_type: VariableType):
        _class_names: Dict[VariableType, str] = {
            VariableType.STRING: StringValue.__name__,
            VariableType.REAL: RealValue.__name__,
            VariableType.INTEGER: IntegerValue.__name__,
            VariableType.BOOLEAN: BooleanValue.__name__,
            VariableType.STRING_ARRAY: StringArrayValue.__name__,
            VariableType.REAL_ARRAY: RealArrayValue.__name__,
            VariableType.INTEGER_ARRAY: IntegerArrayValue.__name__,
            VariableType.BOOLEAN_ARRAY: BooleanArrayValue.__name__
        }

        self.from_type: VariableType = from_type
        self.to_type: VariableType = to_type
        self.message = _error("ERROR_INCOMPATIBLE_TYPES",
                              _class_names[self.from_type],
                              _class_names[self.to_type])
        super().__init__(self.message)
