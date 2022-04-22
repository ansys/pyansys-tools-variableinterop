from typing import Optional

from ansys.common.variableinterop import file_value as file_value
from ansys.common.variableinterop.api_string_to_value_visitor import APIStringToValueVisitor
from ansys.common.variableinterop.array_values import (
    BooleanArrayValue,
    IntegerArrayValue,
    RealArrayValue,
    StringArrayValue,
)
from ansys.common.variableinterop.file_scope import FileScope
from ansys.common.variableinterop.isave_context import ILoadContext, ISaveContext
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

    def __init__(self, save_context: Optional[ISaveContext]):
        self._save_context = save_context

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
        return value.to_api_string(self._save_context)

    def visit_real_array(self, value: RealArrayValue) -> str:
        return value.to_api_string()

    def visit_boolean_array(self, value: BooleanArrayValue) -> str:
        return value.to_api_string()

    def visit_string_array(self, value: StringArrayValue) -> str:
        return value.to_api_string()

    def visit_file_array(self, value: file_value.FileValue) -> str:
        return value.to_api_string(self._save_context)


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
