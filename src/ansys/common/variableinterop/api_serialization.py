from typing import Optional

from ansys.common.variableinterop import boolean_array_value as boolean_array_value
from ansys.common.variableinterop import boolean_value as boolean_value
from ansys.common.variableinterop import file_value as file_value
from ansys.common.variableinterop import integer_array_value as integer_array_value
from ansys.common.variableinterop import integer_value as integer_value
from ansys.common.variableinterop import real_array_value as real_array_value
from ansys.common.variableinterop import real_value as real_value
from ansys.common.variableinterop import string_array_value as string_array_value
from ansys.common.variableinterop import string_value as string_value
from ansys.common.variableinterop.api_string_to_value_visitor import APIStringToValueVisitor
from ansys.common.variableinterop.file_scope import FileScope
from ansys.common.variableinterop.isave_context import ILoadContext, ISaveContext
from ansys.common.variableinterop.ivariable_type_pseudovisitor import vartype_accept
from ansys.common.variableinterop.ivariable_visitor import IVariableValueVisitor
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.variable_value import IVariableValue


class ToAPIStringVisitor(IVariableValueVisitor[str]):

    def __init__(self, save_context: Optional[ISaveContext]):
        self._save_context = save_context

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
        return value.to_api_string(value, self._save_context)

    def visit_real_array(self, value: real_array_value.RealArrayValue) -> str:
        return value.to_api_string()

    def visit_boolean_array(self, value: boolean_array_value.BooleanArrayValue) -> str:
        return value.to_api_string()

    def visit_string_array(self, value: string_array_value.StringArrayValue) -> str:
        return value.to_api_string()


def to_api_string(value: IVariableValue, save_context: Optional[ISaveContext] = None) -> str:
    """
    Convert a variable value to an API string.

    Parameters
    ----------
    value the value to convert to an API string
    save_context the save context. This may be omitted in cases where you do not wish to support
        file values.

    Returns
    -------
    The serialized form of value
    """
    return value.accept(ToAPIStringVisitor(save_context))


def from_api_string(var_type: VariableType, source: str, fscope: Optional[FileScope] = None,
                    load_context: Optional[ILoadContext] = None) -> IVariableValue:
    """
    Generate a value from an API string.

    Parameters
    ----------
    var_type the variable type to generate
    source the source string
    fscope the file scope to use to deserialize file variables. May be None if file variables
      are not needed
    load_context the load context to read file contents from. May be None if file variables are
      not needed

    Returns
    -------
    An implementation of IVariableValue of the correct type with a value parsed
    from the specified string.
    """
    generator: APIStringToValueVisitor = \
        APIStringToValueVisitor(source, fscope, load_context)
    result: IVariableValue = vartype_accept(generator, var_type)
    return result