"""Contains a method for converting a formatted string to a value."""
from numpy import unicode_

from .from_formatted_string_visitor import FromFormattedStringVisitor
from .ivariable_type_pseudovisitor import vartype_accept
from .variable_type import VariableType
from .variable_value import IVariableValue


def from_formatted_string(var_type: VariableType, source: str, locale_name: str) -> IVariableValue:
    """
    Convert a value formatted to a specific locale back into an IVariableValue.

    Parameters
    ----------
    var_type The type of variable to convert to.
    source The string to convert.
    locale_name The locale the string was formatted in.

    Returns
    -------
    An IVariableValue of the specified type whose value matches the
    given string.
    """
    generator: FromFormattedStringVisitor = FromFormattedStringVisitor(
        unicode_(source), locale_name
    )
    result: IVariableValue = vartype_accept(generator, var_type)
    return result
