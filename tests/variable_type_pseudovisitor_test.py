import pytest

from ansys.tools.variableinterop import IVariableTypePseudoVisitor, VariableType, vartype_accept


class TestPseudoVisitor(IVariableTypePseudoVisitor[str]):
    def visit_unknown(self):
        return "dunno"

    def visit_int(self):
        return "whole number"

    def visit_real(self):
        return "whole number and change"

    def visit_boolean(self):
        return "true or false"

    def visit_string(self):
        return "letters"

    def visit_file(self):
        return "pages"

    def visit_int_array(self):
        return "some whole numbers"

    def visit_real_array(self):
        return "some whole numbers and change"

    def visit_bool_array(self):
        return "some true or false"

    def visit_string_array(self):
        return "some letters"

    def visit_file_array(self):
        return "some pages"


@pytest.mark.parametrize(
    "var_type,expect_return",
    [
        pytest.param(VariableType.UNKNOWN, "dunno"),
        pytest.param(VariableType.INTEGER, "whole number"),
        pytest.param(VariableType.REAL, "whole number and change"),
        pytest.param(VariableType.BOOLEAN, "true or false"),
        pytest.param(VariableType.STRING, "letters"),
        pytest.param(VariableType.FILE, "pages"),
        pytest.param(VariableType.INTEGER_ARRAY, "some whole numbers"),
        pytest.param(VariableType.REAL_ARRAY, "some whole numbers and change"),
        pytest.param(VariableType.BOOLEAN_ARRAY, "some true or false"),
        pytest.param(VariableType.STRING_ARRAY, "some letters"),
        pytest.param(VariableType.FILE_ARRAY, "some pages"),
        pytest.param(None, "dunno"),
    ],
)
def test_accept_pseudovisitor(var_type: VariableType, expect_return: str) -> None:
    # Setup: create a test pseudo-visitor.
    visitor: IVariableTypePseudoVisitor[str] = TestPseudoVisitor()

    # Execute: pseudo-visit the type.
    # The pseudo-visitor returns a string depending on the type it was sent to.
    # If there is any mistake in the mapping in IVariableTypePseudoVisitor's accept implementation,
    # (or for that matter in the test), at least one test case will fail,
    # unless the mistake in the test and the mistake in the implementation exactly cancel
    # one another out (seems reasonably unlikely)
    result: str = vartype_accept(visitor, var_type)

    # Verify: the result from the pseudo-visitor should match the type it was sent to visit.
    assert result == expect_return
