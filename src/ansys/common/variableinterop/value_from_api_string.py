"""Definition of from_api_string."""
from ansys.common.variableinterop.api_string_to_value_visitor import APIStringToValueVisitor
from ansys.common.variableinterop.ivariable_type_pseudovisitor import vartype_accept
from ansys.common.variableinterop.variable_type import VariableType
from ansys.common.variableinterop.variable_value import IVariableValue


def from_api_string(var_type: VariableType, source: str) -> IVariableValue:
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
        APIStringToValueVisitor(source)
    result: IVariableValue = vartype_accept(generator, var_type)
    return result
