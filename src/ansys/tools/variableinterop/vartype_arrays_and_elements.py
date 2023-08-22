"""Defines functions for determining the correct array type for a scalar type and vice-
versa."""

from typing import Optional

from .exceptions import _error
from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from .variable_type import VariableType


class __ScalarToArrayPseudoVisitor(IVariableTypePseudoVisitor[Optional[VariableType]]):
    """
    Provides the corresponding array type for a given scalar type.

    Provides None if the visited type has no array type or is an array.
    """

    def visit_unknown(self) -> Optional[VariableType]:
        return None

    def visit_int(self) -> Optional[VariableType]:
        return VariableType.INTEGER_ARRAY

    def visit_real(self) -> Optional[VariableType]:
        return VariableType.REAL_ARRAY

    def visit_boolean(self) -> Optional[VariableType]:
        return VariableType.BOOLEAN_ARRAY

    def visit_string(self) -> Optional[VariableType]:
        return VariableType.STRING_ARRAY

    def visit_file(self) -> Optional[VariableType]:
        return VariableType.FILE_ARRAY

    def visit_int_array(self) -> Optional[VariableType]:
        return None

    def visit_real_array(self) -> Optional[VariableType]:
        return None

    def visit_bool_array(self) -> Optional[VariableType]:
        return None

    def visit_string_array(self) -> Optional[VariableType]:
        return None

    def visit_file_array(self) -> Optional[VariableType]:
        return None


class __ElementTypePseudoVisitor(IVariableTypePseudoVisitor[Optional[VariableType]]):
    """
    Provides the corresponding element type for a given array type.

    Provides None if the visited type is not an array.
    """

    def visit_unknown(self) -> Optional[VariableType]:
        return None

    def visit_int(self) -> Optional[VariableType]:
        return None

    def visit_real(self) -> Optional[VariableType]:
        return None

    def visit_boolean(self) -> Optional[VariableType]:
        return None

    def visit_string(self) -> Optional[VariableType]:
        return None

    def visit_file(self) -> Optional[VariableType]:
        return None

    def visit_int_array(self) -> Optional[VariableType]:
        return VariableType.INTEGER

    def visit_real_array(self) -> Optional[VariableType]:
        return VariableType.REAL

    def visit_bool_array(self) -> Optional[VariableType]:
        return VariableType.BOOLEAN

    def visit_string_array(self) -> Optional[VariableType]:
        return VariableType.STRING

    def visit_file_array(self) -> Optional[VariableType]:
        return VariableType.FILE


def to_array_type(vartype: VariableType) -> VariableType:
    """
    Given a VariableType, find the corresponding array type, if one exists. Otherwise,
    ValueError is raised.

    Parameters
    ----------
    vartype : VariableType
        The variable type of interest.

    Returns
    -------
    VariableType
        The corresponding array type.

    Raises
    ------
    ValueError
        If the specified type does not have a corresponding array type.
    """
    result: Optional[VariableType] = vartype_accept(__ScalarToArrayPseudoVisitor(), vartype)

    if result is None:
        raise ValueError(_error("ERROR_NO_ARRAY_TYPE", vartype.associated_type_name))
    else:
        return result


def get_element_type(vartype: VariableType) -> VariableType:
    """
    Given a VariableType representing an array, return the corresponding element type.

    When a non-array type is passed, ValueError is raised.

    Parameters
    ----------
    vartype : VariableType
        The variable type of interest.

    Returns
    -------
    VariableType
        The corresponding element type.

    Raises
    ------
    ValueError
        If the specified type does not have a corresponding element type.
    """
    result: Optional[VariableType] = vartype_accept(__ElementTypePseudoVisitor(), vartype)

    if result is None:
        raise ValueError(_error("ERROR_NO_SCALAR_TYPE", vartype.associated_type_name))
    else:
        return result
