"""Definition of ToAPIStringVisitor."""
from typing import Optional

from overrides import overrides

from .api_string_to_value_visitor import APIStringToValueVisitor
from .array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from .file_array_value import FileArrayValue
from .file_scope import FileScope
from .file_value import FileValue
from .isave_context import ILoadContext, ISaveContext
from .ivariable_type_pseudovisitor import vartype_accept
from .ivariable_visitor import IVariableValueVisitor
from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from .variable_type import VariableType
from .variable_value import IVariableValue


class ToAPIStringVisitor(IVariableValueVisitor[str]):
    """Visits values and converts them to an API string."""

    def __init__(self, save_context: Optional[ISaveContext]):
        """
        Initialize the visitor.

        Parameters
        ----------
        save_context : ISaveContext, optional
            The save context to use for conversion.
        """
        self._save_context = save_context

    @overrides
    def visit_integer(self, value: IntegerValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_real(self, value: RealValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_boolean(self, value: BooleanValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_string(self, value: StringValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_integer_array(self, value: IntegerArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_file(self, value: FileValue) -> str:
        return value.to_api_string(self._save_context)

    @overrides
    def visit_real_array(self, value: RealArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_boolean_array(self, value: BooleanArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_string_array(self, value: StringArrayValue) -> str:
        return value.to_api_string()

    @overrides
    def visit_file_array(self, value: FileArrayValue) -> str:
        return value.to_api_string(self._save_context)


def to_api_string(value: IVariableValue, save_context: Optional[ISaveContext] = None) -> str:
    """
    Convert a variable value to an API string.

    Parameters
    ----------
    value : IVariableValue
        Value to convert to an API string.
    save_context : ISaveContext, optional
        The save context. This may be omitted in cases where you do not wish to support
        file values.

    Returns
    -------
    str
        The serialized form of value.
    """
    return value.accept(ToAPIStringVisitor(save_context))


def from_api_string(
    var_type: VariableType,
    source: str,
    fscope: Optional[FileScope] = None,
    load_context: Optional[ILoadContext] = None,
) -> IVariableValue:
    """
    Generate a value from an API string.

    Parameters
    ----------
    var_type : VariableType
        Variable type to generate.
    source : str
       Source string.
    fscope : FileScope, optional
        The file scope to use to deserialize file variables. May be None if file variables
        are not needed.
    load_context : ILoadContext, optional
        Load context to read file contents from. If file variables are
        not needed, the value can be ``None``.

    Returns
    -------
    IVariableValue
        Implementation of ``IVariableValue`` of the correct type with a value parsed from the
        specified string.
    """
    generator: APIStringToValueVisitor = APIStringToValueVisitor(source, fscope, load_context)
    result: IVariableValue = vartype_accept(generator, var_type)
    return result
