from ansys.common.variableinterop import string_array_value as string_array_value, \
    boolean_array_value as boolean_array_value, real_array_value as real_array_value, \
    file_value as file_value, integer_array_value as integer_array_value, \
    string_value as string_value, boolean_value as boolean_value, real_value as real_value, \
    integer_value as integer_value
from ansys.common.variableinterop.api_string_to_value_visitor import APIStringToValueVisitor
from ansys.common.variableinterop.ivariable_type_pseudovisitor import vartype_accept
from ansys.common.variableinterop.file_scope import FileScope
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.variable_value import IVariableValue
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from typing import Optional


class ToAPIStringVisitor(IVariableValueVisitor[str]):

    def __init__(self, file_scope: Optional[FileScope]):
        self.__scope = file_scope

    def visit_integer(self, value: integer_value.IntegerValue) -> str:
        return value.to_api_string()

    def visit_real(self, value: real_value.RealValue) -> str:
        return value.to_api_string()

    def visit_boolean(self, value: boolean_value.BooleanValue) -> str:
        return value.to_api_string()

    def visit_string(self, value: string_value.StringValue) -> str:
        return value.to_api_string()

    def visit_integer_array(self, value: integer_array_value.IntegerArrayValue) -> str:
        return value.to_api_string()

    def visit_file(self, value: file_value.FileValue) -> str:
        if self.__scope is None:
            raise NotImplementedError("This operation does not support file values.")
        else:
            return value.to_api_string(value, self.__scope.to_api_string_file_store())

    def visit_real_array(self, value: real_array_value.RealArrayValue) -> str:
        return value.to_api_string()

    def visit_boolean_array(self, value: boolean_array_value.BooleanArrayValue) -> str:
        return value.to_api_string()

    def visit_string_array(self, value: string_array_value.StringArrayValue) -> str:
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


def from_api_string(var_type: VariableType, source: str, fscope: Optional[FileScope] = None) -> IVariableValue:
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