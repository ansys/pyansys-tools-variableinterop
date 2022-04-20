from typing import Callable, Optional

from ansys.common.variableinterop import file_value as file_value
from ansys.common.variableinterop.api_string_to_value_visitor import APIStringToValueVisitor
from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
from ansys.common.variableinterop.file_scope import FileScope
from ansys.common.variableinterop.ivariable_type_pseudovisitor import vartype_accept
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.variable_value import IVariableValue


class ToAPIStringVisitor(IVariableValueVisitor[str]):

    def __init__(self, file_scope: Optional[FileScope]):
        self.__scope = file_scope

    def visit_integer(self, value: IntegerValue) -> str:
        return value.to_api_string()

    def visit_real(self, value: RealValue) -> str:
        return value.to_api_string()

    def visit_boolean(self, value: BooleanValue) -> str:
        return value.to_api_string()

    def visit_string(self, value: StringValue) -> str:
        return value.to_api_string()

    def visit_integer_array(self, value: IntegerArrayValue) -> str:
        return value.to_api_string()

    def visit_file(self, value: file_value.FileValue) -> str:
        if isinstance(self.__scope, FileScope):
            file_store: Callable[[file_value.FileValue], str] =\
                lambda target_file_val: self.__scope.to_api_string_file_store(  # type: ignore
                    target_file_val)
            return value.to_api_string(file_store)
        else:
            raise NotImplementedError("This operation does not support file values.")

    def visit_real_array(self, value: RealArrayValue) -> str:
        return value.to_api_string()

    def visit_boolean_array(self, value: BooleanArrayValue) -> str:
        return value.to_api_string()

    def visit_string_array(self, value: StringArrayValue) -> str:
        return value.to_api_string()


def to_api_string(value: IVariableValue, file_scope: FileScope = None):
    """
    Convert a variable value to an API string.

    Parameters
    ----------
    value the value to convert to an API string
    file_scope the file scope. This may be omitted in cases where you do not wish to support
        file values.

    Returns
    -------

    """
    return value.accept(ToAPIStringVisitor(file_scope))


def from_api_string(var_type: VariableType,
                    source: str,
                    fscope: Optional[FileScope] = None) -> IVariableValue:
    """
    Generate a value from an API string.

    Parameters
    ----------
    var_type the variable type to generate
    source the source string

    Returns
    -------
    An implementation of IVariableValue of the correct type with a value parsed
    from the specified string.
    """
    generator: APIStringToValueVisitor = \
        APIStringToValueVisitor(source, fscope)
    result: IVariableValue = vartype_accept(generator, var_type)
    return result
