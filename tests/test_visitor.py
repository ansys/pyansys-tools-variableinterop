"""Unit tests of IVariableVisitor, and accept methods of value types."""

import pytest

import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.variable_value as variable_value


class TestVisitor(ivariable_visitor.IVariableValueVisitor[str]):
    """
    Implementation of IVariableValueVisitor for testing.

    Simply returns the value when visited.
    """

    def visit_integer(self, value: integer_value.IntegerValue) -> str:
        return value + 0

    def visit_real(self, value: real_value.RealValue) -> str:
        return value + 0.0

    def visit_boolean(self, value: boolean_value.BooleanValue) -> str:
        return value or False

    def visit_string(self, value: string_value.StringValue) -> str:
        return value + ""

    # IntegerArray

    # RealArray

    # BooleanArray

    # StringArray


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(real_value.RealValue(1.0), 1.0, id="Real"),
        pytest.param(integer_value.IntegerValue(1), 1, id="Integer"),
        #pytest.param(boolean_value.BooleanValue(True), True, id="Boolean"),
        pytest.param(string_value.StringValue("錦蛇"), "錦蛇", id="String"),
    ]
)
def test_visiting_a_value_should_work(value: variable_value.IVariableValue, expected: any) -> None:
    """
    Verifies that the visitor pattern is working for IVariableValue.

    Parameters
    ----------
    value The IVariableValue to visit.
    expected The value the IVariableValue wraps.
    """
    # Setup
    visitor = TestVisitor()

    # SUT
    result = value.accept(visitor)

    # Verification
    assert result is not variable_value.IVariableValue
    assert result == expected
