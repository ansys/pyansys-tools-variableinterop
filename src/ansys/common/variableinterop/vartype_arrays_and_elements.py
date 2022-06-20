"""Defines functions for determining the correct array type for a scalar type and vice-versa."""

from typing import Optional

import ansys.common.variableinterop.exceptions as exceptions
import ansys.common.variableinterop.ivariable_type_pseudovisitor as pseudovisitor
import ansys.common.variableinterop.variable_type as variable_type


class __ScalarToArrayPseudoVisitor(
    pseudovisitor.IVariableTypePseudoVisitor[Optional[variable_type.VariableType]]
):
    """
    Provides the corresponding array type for a given scalar type.

    Provides None if the visited type has no array type or is an array.
    """

    def visit_unknown(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_int(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.INTEGER_ARRAY

    def visit_real(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.REAL_ARRAY

    def visit_boolean(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.BOOLEAN_ARRAY

    def visit_string(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.STRING_ARRAY

    def visit_file(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.FILE_ARRAY

    def visit_int_array(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_real_array(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_bool_array(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_string_array(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_file_array(self) -> Optional[variable_type.VariableType]:
        return None


class __ElementTypePseudoVisitor(
    pseudovisitor.IVariableTypePseudoVisitor[Optional[variable_type.VariableType]]
):
    """
    Provides the corresponding element type for a given array type.

    Provides None if the visited type is not an array.
    """

    def visit_unknown(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_int(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_real(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_boolean(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_string(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_file(self) -> Optional[variable_type.VariableType]:
        return None

    def visit_int_array(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.INTEGER

    def visit_real_array(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.REAL

    def visit_bool_array(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.BOOLEAN

    def visit_string_array(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.STRING

    def visit_file_array(self) -> Optional[variable_type.VariableType]:
        return variable_type.VariableType.FILE


def to_array_type(vartype: variable_type.VariableType) -> variable_type.VariableType:
    """Given a VariableType, find the corresponding array type, if one \
    exists. Otherwise, ValueError is raised.

    Parameters
    ----------
    vartype the variable type of interest.

    Returns
    -------
    The corresponding array type.

    Raises
    ------
    ValueError if the specified type does not have a corresponding array type.

    """
    result: Optional[variable_type.VariableType] = pseudovisitor.vartype_accept(
        __ScalarToArrayPseudoVisitor(), vartype
    )

    if result is None:
        raise ValueError(exceptions._error("ERROR_NO_ARRAY_TYPE", vartype.associated_type_name))
    else:
        return result


def get_element_type(vartype: variable_type.VariableType) -> variable_type.VariableType:
    """
    Given a VariableType representing an array, return the corresponding element type.

    When a non-array type is passed, ValueError is raised.

    Parameters
    ----------
    vartype the variable type of interest.

    Returns
    -------
    The corresponding element type.

    Raises
    ------
    ValueError if the specified type does not have a corresponding element type.

    """
    result: Optional[variable_type.VariableType] = pseudovisitor.vartype_accept(
        __ElementTypePseudoVisitor(), vartype
    )

    if result is None:
        raise ValueError(exceptions._error("ERROR_NO_SCALAR_TYPE", vartype.associated_type_name))
    else:
        return result
