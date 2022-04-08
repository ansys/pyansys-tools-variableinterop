"""Definition of BooleanValue."""
from __future__ import annotations
from numpy import bool_
from typing import TYPE_CHECKING, TypeVar

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
        if source is None:
            self.__value = False
        elif isinstance(source, (bool, bool_)):
            self.__value = source
        elif isinstance(source, variable_value.IVariableValue):
            self.__value = source.accept(to_bool_visitor.ToBoolVisitor())
        else:
            raise ValueError

    # equality definition here

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
