"""Provides a method for checking whether a variable type is an array type."""
from overrides import overrides

from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from .variable_type import VariableType


class _VarTypeIsArrayVisitor(IVariableTypePseudoVisitor[bool]):
    """
    Determines whether the visited variable type is an array.

    ``True`` is returned if the visited type is an array type, and ``False`` is returned
    otherwise.
    """

    @overrides
    def visit_unknown(self) -> bool:
        return False

    @overrides
    def visit_int(self) -> bool:
        return False

    @overrides
    def visit_real(self) -> bool:
        return False

    @overrides
    def visit_boolean(self) -> bool:
        return False

    @overrides
    def visit_string(self) -> bool:
        return False

    @overrides
    def visit_file(self) -> bool:
        return False

    @overrides
    def visit_int_array(self) -> bool:
        return True

    @overrides
    def visit_real_array(self) -> bool:
        return True

    @overrides
    def visit_bool_array(self) -> bool:
        return True

    @overrides
    def visit_string_array(self) -> bool:
        return True

    @overrides
    def visit_file_array(self) -> bool:
        return True


def var_type_is_array(vartype: VariableType) -> bool:
    """
    Check whether the provided variable type is an array type.

    Parameters
    ----------
    vartype : VariableType
        Variable type of interest.

    Returns
    -------
    bool
        ``True`` if the specified variable type is an array type, ``False`` otherwise.
    """
    return vartype_accept(_VarTypeIsArrayVisitor(), vartype)
