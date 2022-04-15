"""Provides a function that allows checking whether a variable type is an array type."""
from overrides import overrides

import ansys.common.variableinterop.ivariable_type_pseudovisitor as pseudovisitor
import ansys.common.variableinterop.variable_type as variable_type


class _var_type_is_array_visitor(pseudovisitor.IVariableTypePseudoVisitor[bool]):
    """
    A pseudovisitor implementation that checks whether the visited type is an array.

    True is returned if the visited type is an array type, and false is returned otherwise.
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


def var_type_is_array(vartype: variable_type.VariableType) -> bool:
    """
    Check whether the provided variable type is an array type or not.

    Parameters
    ----------
    vartype the variable type of interest

    Returns
    -------
    True if the specified variable type is an array type, false otherwise.
    """
    return pseudovisitor.vartype_accept(_var_type_is_array_visitor(), vartype)
