"""Definition of BooleanValue."""
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Dict

import numpy as np

from ansys.common.variableinterop import exceptions, variable_value

if TYPE_CHECKING:
    from ansys.common.variableinterop import (
        ivariable_visitor, to_bool_visitor, variable_type
    )


def int64_to_bool(val: np.int64) -> bool:
    """
    Convert a numpy int64 to a bool value per interchange
    specifications.
    """
    return val != 0


def int_to_bool(val: int) -> bool:
    """
    Convert an int to a bool value per interchange specifications.
    """
    return val != 0


def float_to_bool(val: float) -> bool:
    """
    Convert a float value to a bool per interchange specifications.
    """
    return val != 0.0


api_str_to_bool: Dict[str, bool] = {
    'yes': True,
    'y': True,
    'true': True,
    'no': False,
    'n': False,
    'false': False
}
"""
A mapping of acceptable normalized values for API string conversion
to their corresponding bool value.
"""


def str_to_bool(val: str):
    """
    Convert a str to a bool per interchange specifications.
    """
    _value: str = val.strip().lower()
    if _value in api_str_to_bool:
        return api_str_to_bool[_value]
    else:
        try:
            _f_value: float = float(_value)
            return float_to_bool(_f_value)
        except ValueError:
            pass
        raise ValueError


class BooleanValue(variable_value.IVariableValue):
    """
    Wrapper around a boolean value.

    If you want the variable interop standard conversions, use xxxx (TODO)
    """

    def __init__(self, source: object = None):
        """
        Construct a BooleanValue from various source types. Supported
        types include:
        None: Constructs a False BooleanValue
        bool or numpy.bool_: Constructs a BooleanValue with the given
            Boolean value.
        IVariableValue: Constructs a BooleanValue per the specification
        Others: raises an exception
        """
        if source is None:
            self.__value: bool = False
        elif isinstance(source, bool):
            self.__value: bool = source
        elif isinstance(source, np.bool_):
            self.__value: bool = bool(source)
        elif isinstance(source, variable_value.IVariableValue):
            self.__value: bool = source.accept(to_bool_visitor.ToBoolVisitor())
        else:
            raise exceptions.IncompatibleTypesException(
                type(source).__name__, variable_type.VariableType.BOOLEAN)

    # equality definition here
    def __eq__(self, other):
        """
        Tests that the two objects are equivalent.
        """
        if isinstance(other, BooleanValue):
            return self.__value == other.__value
        elif isinstance(other, (bool, np.bool_)):
            return self.__value == other
        else:
            # TODO: instead of assuming not equal, should we test
            #  against the Python "falseness" of other?
            return False

    def __bool__(self):
        """
        Return the true-ness or false-ness of this object.
        """
        return self.__value

    def __hash__(self):
        """
        Returns a hash code for this object
        """
        return hash(self.__value)

    T = TypeVar("T")

    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
