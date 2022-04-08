"""Definition of BooleanValue."""
from __future__ import annotations
from ansys.common.variableinterop.variable_value import IVariableValue
from numpy import bool_
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
    from ansys.common.variableinterop.to_bool_visitor import ToBoolVisitor
    from ansys.common.variableinterop.variable_type import VariableType


class BooleanValue(IVariableValue):
    """
    Wrapper around a boolean value.

    If you want the variable interop standard conversions, use xxxx (TODO)
    """

    __value: bool

    def __init__(self, source: object = None):
        if source is None:
            self.__value = False
        elif isinstance(source, (bool, bool_)):
            self.__value = source
        elif isinstance(source, IVariableValue):
            self.__value = source.accept(ToBoolVisitor())
        else:
            raise ValueError

    # equality definition here
    def __eq__(self, other):
        if isinstance(other, BooleanValue):
            return self.__value == other.__value
        elif isinstance(other, (bool, bool_)):
            return self.__value == other
        else:
            return False

    def __bool__(self):
        return self.__value

    # hashcode definition here

    T = TypeVar("T")

    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN

    def to_api_string(self) -> str:
        raise NotImplementedError

    def from_api_string(self, value: str) -> None:
        raise NotImplementedError

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
