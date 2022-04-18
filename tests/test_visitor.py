"""Unit tests of IVariableVisitor, and accept methods of value types."""

from typing import Any

import pytest
from test_utils import _create_exception_context, _test_to_value_visitor
from typing import Type

import ansys.common.variableinterop as acvi


class TestVisitor(acvi.IVariableValueVisitor[str]):
    """
    Implementation of IVariableValueVisitor for testing.

    Simply returns the value when visited.
    """

    def visit_integer(self, value: acvi.IntegerValue) -> str:
        return value + 0

    def visit_real(self, value: acvi.RealValue) -> str:
        return value + 0.0

    def visit_boolean(self, value: acvi.BooleanValue) -> str:
        return value

    def visit_string(self, value: acvi.StringValue) -> str:
        return value + ""

    def visit_integer_array(self, value: acvi.IntegerArrayValue) -> str:
        return value

    def visit_real_array(self, value: acvi.RealArrayValue) -> str:
        return value

    def visit_boolean_array(self, value: acvi.BooleanArrayValue) -> str:
        return value

    def visit_string_array(self, value: acvi.StringArrayValue) -> str:
        return value


# region TestVisitor
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(acvi.RealValue(1.0), 1.0, id="Real"),
        pytest.param(acvi.IntegerValue(1), 1, id="Integer"),
        pytest.param(acvi.BooleanValue(True), True, id="Boolean"),
        pytest.param(acvi.StringValue("錦蛇"), "錦蛇", id="String"),
    ]
)
def test_visiting_a_value_should_work(value: acvi.IVariableValue, expected: Any) -> None:
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
    assert result is not acvi.IVariableValue
    assert result == expected
# endregion


# region ToRealArrayVisitor
@pytest.mark.parametrize(
    "value,expected_result,expected_exception",
    [
        pytest.param(acvi.IntegerValue(0), None, acvi.IncompatibleTypesException,
                     id="IntegerValue"),
        pytest.param(acvi.RealValue(0), None, acvi.IncompatibleTypesException, id="RealValue"),

        # TODO: uncomment when we figure out what to do with BooleanValue since it can't
        #       inherit np.bool_
        # pytest.param(BooleanValue(False), None, IncompatibleTypesException, id="BooleanValue"),

        pytest.param(acvi.StringValue(""), None, acvi.IncompatibleTypesException, id="StringValue"),
        pytest.param(acvi.IntegerArrayValue(values=[1, 2]), acvi.RealArrayValue(values=[1.0, 2.0]),
                     None, id="IntegerArrayValue"),
        pytest.param(acvi.RealArrayValue(values=[1, 2]), acvi.RealArrayValue(values=[1, 2]),
                     None, id="RealArrayValue"),
        pytest.param(acvi.BooleanArrayValue(values=[True, False]),
                     acvi.RealArrayValue(values=[1.0, 0.0]), None, id="BooleanArrayValue"),
        pytest.param(acvi.StringArrayValue(values=["1", "2.5"]),
                     acvi.RealArrayValue(values=[1.0, 2.5]), None, id="StringArrayValue"),
    ])
def test_to_real_array_visitor(value: acvi.IVariableValue,
                               expected_result: acvi.RealArrayValue,
                               expected_exception: Type[BaseException]):
    """Verify that ToRealArrayVisitor gets the expected result, or that the expected exception is
    raised."""

    with _create_exception_context(expected_exception):
        instance = acvi.ToRealArrayVisitor()
        try:
            # SUT
            result: acvi.RealArrayValue = value.accept(instance)

            # Verify (no exception)
            assert result == expected_result

        except acvi.IncompatibleTypesException as e:
            # Verify (expected exception)
            assert e.message == \
                   ("Error: Cannot convert from type {0} to type {1}.\n"
                    "Reason: The types are incompatible.") \
                   .format(value.__class__.__name__, acvi.RealArrayValue.__name__)
            raise e
# endregion


# region ToBooleanArrayVisitor
@pytest.mark.parametrize(
    "value,expected_result,expected_exception",
    [
        pytest.param(acvi.IntegerValue(0),
                     None,
                     acvi.IncompatibleTypesException,
                     id="IntegerValue"),
        pytest.param(acvi.RealValue(0),
                     None,
                     acvi.IncompatibleTypesException,
                     id="RealValue"),

        # TODO: uncomment when we figure out what to do with BooleanValue since it can't
        #       inherit np.bool_
        # pytest.param(BooleanValue(False), None, IncompatibleTypesException, id="BooleanValue"),

        pytest.param(acvi.StringValue(""),
                     None,
                     acvi.IncompatibleTypesException,
                     id="StringValue"),
        pytest.param(acvi.IntegerArrayValue(values=[-1, 0, 1]),
                     acvi.BooleanArrayValue(values=[True, False, True]),
                     None,
                     id="IntegerArrayValue"),
        pytest.param(acvi.RealArrayValue(values=[-1.0, 0.0, 1.0]),
                     acvi.BooleanArrayValue(values=[True, False, True]),
                     None,
                     id="RealArrayValue"),
        pytest.param(acvi.BooleanArrayValue(values=[True, False]),
                     acvi.BooleanArrayValue(values=[True, False]),
                     None,
                     id="BooleanArrayValue"),
        pytest.param(acvi.StringArrayValue(values=[
                         ["yEs", "Y", "tRue", "1", "-1"],
                         ["No", "N", "FalSe", "0", "-0"]]),
                     acvi.BooleanArrayValue(values=[
                         [True, True, True, True, True],
                         [False, False, False, False, False]]),
                     None,
                     id="StringArrayValue_valid"),
        pytest.param(acvi.StringArrayValue(values=["true", "false", "this raises ValueError"]),
                     None,
                     ValueError,
                     id="StringArrayValue_expect_ValueError")
    ])
def test_to_boolean_array_visitor(value: acvi.IVariableValue,
                                  expected_result: acvi.BooleanArrayValue,
                                  expected_exception: Type[BaseException]):
    """
    Verify that ToBooleanArrayVisitor gets the expected result, or that the expected exception is
    raised.
    """
    _test_to_value_visitor(value, expected_result, expected_exception, acvi.ToBooleanArrayVisitor,
                           acvi.BooleanArrayValue)
# endregion


# region ToIntegerArrayVisitor
@pytest.mark.parametrize(
    "value,expected_result,expected_exception",
    [
        pytest.param(acvi.IntegerValue(0),
                     None,
                     acvi.IncompatibleTypesException,
                     id="IntegerValue"),
        pytest.param(acvi.RealValue(0),
                     None,
                     acvi.IncompatibleTypesException,
                     id="RealValue"),

        # TODO: uncomment when we figure out what to do with BooleanValue since it can't
        #       inherit np.bool_
        # pytest.param(BooleanValue(False), None, IncompatibleTypesException, id="BooleanValue"),

        pytest.param(acvi.StringValue(""),
                     None,
                     acvi.IncompatibleTypesException,
                     id="StringValue"),
        pytest.param(acvi.IntegerArrayValue(values=[-1, 0, 1]),
                     acvi.IntegerArrayValue(values=[-1, 0, 1]),
                     None,
                     id="IntegerArrayValue"),
        # TODO: expected results to be updated after merging utils.convert
        # Reals should round away from zero, i.e. 0.1 rounds to 1 and -0.1 to -1
        #   ^ this is not correct
        pytest.param(acvi.RealArrayValue(values=[-0.9, -0.5, -0.1, 0.0, 0.1, 0.5, 0.9]),
                     acvi.IntegerArrayValue(values=[-1, -1, -1, 0, 1, 1, 1]),
                     None,
                     id="RealArrayValue"),
        pytest.param(acvi.BooleanArrayValue(values=[True, False]),
                     acvi.IntegerArrayValue(values=[1, 0]),
                     None,
                     id="BooleanArrayValue"),
        # Test rounding from string arrays as well
        pytest.param(acvi.StringArrayValue(
                        values=["-0.9", "-0.5", "-0.1", "0", "0.1", "0.5", "0.9", "50"]),
                     acvi.IntegerArrayValue(values=[-1, -1, -1, 0, 1, 1, 1, 50]),
                     None,
                     id="StringArrayValue_valid"),
        pytest.param(acvi.StringArrayValue(values=["1", "2", "this raises ValueError"]),
                     None,
                     ValueError,
                     id="StringArrayValue_expect_ValueError")
    ])
def test_to_integer_array_visitor(value: acvi.IVariableValue,
                                  expected_result: acvi.IntegerArrayValue,
                                  expected_exception: Type[BaseException]):
    """
    Verify that ToIntegerArrayVisitor gets the expected result, or that the expected exception is
    raised.
    """
    _test_to_value_visitor(value, expected_result, expected_exception, acvi.ToIntegerArrayVisitor,
                           acvi.IntegerArrayValue)
# endregion


# region ToStringArrayVisitor
@pytest.mark.parametrize(
    "value,expected_result,expected_exception",
    [
        pytest.param(acvi.IntegerValue(0),
                     None,
                     acvi.IncompatibleTypesException,
                     id="IntegerValue"),
        pytest.param(acvi.RealValue(0),
                     None,
                     acvi.IncompatibleTypesException,
                     id="RealValue"),

        # TODO: uncomment when we figure out what to do with BooleanValue since it can't
        #       inherit np.bool_
        # pytest.param(BooleanValue(False), None, IncompatibleTypesException, id="BooleanValue"),

        pytest.param(acvi.StringValue(""),
                     None,
                     acvi.IncompatibleTypesException,
                     id="StringValue"),
        pytest.param(acvi.IntegerArrayValue(values=[-1, 0, 1]),
                     acvi.StringArrayValue(values=["-1", "0", "1"]),
                     None,
                     id="IntegerArrayValue"),
        pytest.param(acvi.RealArrayValue(values=[-1.5, 0.5, 1.5]),
                     acvi.StringArrayValue(values=["-1.5", "0.5", "1.5"]),
                     None,
                     id="RealArrayValue"),
        pytest.param(acvi.BooleanArrayValue(values=[True, False]),
                     acvi.StringArrayValue(values=["True", "False"]),
                     None,
                     id="BooleanArrayValue"),
        pytest.param(acvi.StringArrayValue(values=["1.0", "string cheese"]),
                     acvi.StringArrayValue(values=["1.0", "string cheese"]),
                     None,
                     id="StringArrayValue")
    ])
def test_to_string_array_visitor(value: acvi.IVariableValue,
                                 expected_result: acvi.StringArrayValue,
                                 expected_exception: Type[BaseException]):
    """
    Verify that ToStringArrayVisitor gets the expected result, or that the expected exception is
    raised.
    """
    _test_to_value_visitor(value, expected_result, expected_exception, acvi.ToStringArrayVisitor,
                           acvi.StringArrayValue)
# endregion
