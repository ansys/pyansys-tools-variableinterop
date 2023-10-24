"""Definition of GetModelCenterTypeForValue."""
from overrides import overrides

from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from .variable_value import IVariableValue


class GetModelCenterTypeForValue:
    """Provides a static method for getting the corresponding ModelCenter type for an
    ``IVariableValue`` object."""

    @staticmethod
    def get_modelcenter_type(value: IVariableValue) -> str:
        """
        Get the corresponding ModelCenter type for an IVariableValue.

        Parameters
        ----------
        value : IVariableValue
            Value to get the type for.

        Returns
        -------
        str
            Corresponding ``ModelCenter`` type string.
        """
        generator = GetModelCenterTypeForValue._GetModelCenterTypeVisitor()
        result: str = vartype_accept(generator, value.variable_type)
        return result

    class _GetModelCenterTypeVisitor(IVariableTypePseudoVisitor[str]):
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
        def visit_file(self) -> str:
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
