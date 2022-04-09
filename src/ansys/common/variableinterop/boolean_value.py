"""Definition of BooleanValue."""
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Dict

import numpy as np

import ansys.common.variableinterop.variable_value as variable_value

if TYPE_CHECKING:
    import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
    import ansys.common.variableinterop.to_bool_visitor as to_bool_visitor
    import ansys.common.variableinterop.variable_type as variable_type


class BooleanValue(variable_value.IVariableValue):
    """
    Wrapper around a boolean value.

    If you want the variable interop standard conversions, use xxxx (TODO)
    """

    __value: bool

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
            self.__value = False
        elif isinstance(source, (bool, np.bool_)):
            self.__value = source
        elif isinstance(source, variable_value.IVariableValue):
            self.__value = source.accept(to_bool_visitor.ToBoolVisitor())
        else:
            raise ValueError

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

    api_to_bool: Dict[str, bool] = {
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

    # hashcode definition here

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
