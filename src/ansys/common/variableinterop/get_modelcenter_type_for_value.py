"""Definition of GetModelCenterTypeForValue."""
from overrides import overrides

import ansys.common.variableinterop.ivariable_type_pseudovisitor as pseudo_visitor
from ansys.common.variableinterop.ivariable_type_pseudovisitor import T
import ansys.common.variableinterop.variable_value as variable_value


class GetModelCenterTypeForValue:
    """Static class that provides a method for getting the \
    corresponding ModelCenter type for an IVariableValue."""

    @staticmethod
    def get_modelcenter_type(value: variable_value.IVariableValue) -> str:
        """
        Get the corresponding ModelCenter type for an IVariableValue
        asdf
        Parameters
        ----------
        value The value for which to get the type.

        Returns
        -------
        The corresponding ModelCenter type string.
        """
        generator = GetModelCenterTypeForValue._GetModelCenterTypeVisitor()
        result: str = pseudo_visitor.vartype_accept(generator, value.variable_type)
        return result

    class _GetModelCenterTypeVisitor(pseudo_visitor.IVariableTypePseudoVisitor[str]):
        """Helper visitor used by GetModelCenterTypeForValue."""

        @overrides
        def visit_unknown(self) -> str:
            return "none"

        @overrides
        def visit_int(self) -> str:
            return "int"

        @overrides
        def visit_real(self) -> str:
            return "double"

        @overrides
        def visit_boolean(self) -> str:
            return "bool"

        @overrides
        def visit_string(self) -> str:
            return "string"

        @overrides
        def visit_file(self) -> T:
            return "file"

        @overrides
        def visit_int_array(self) -> str:
            return "int[]"

        @overrides
        def visit_real_array(self) -> str:
            return "double[]"

        @overrides
        def visit_bool_array(self) -> str:
            return "bool[]"

        @overrides
        def visit_string_array(self) -> str:
            return "string[]"

        @overrides
        def visit_file_array(self) -> str:
            return "file[]"
