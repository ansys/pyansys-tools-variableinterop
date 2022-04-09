import pytest

from ansys.common.variableinterop import IntegerValue, RealValue, StringValue, \
    IntegerArrayValue, RealArrayValue, BooleanArrayValue, StringArrayValue, IVariableValue,\
    IncompatibleTypesException, ToRealArrayVisitor
from test_utils import _create_exception_context


@pytest.mark.parametrize(
    "value,expected_result,expected_exception",
    [
        pytest.param(IntegerValue(0), None, IncompatibleTypesException, id="IntegerValue"),
        pytest.param(RealValue(0), None, IncompatibleTypesException, id="RealValue"),

        # TODO: uncomment when we figure out what to do with BooleanValue since it can't
        #       inherit np.bool_
        # pytest.param(BooleanValue(False), IncompatibleTypesException, id="BooleanValue"),

        pytest.param(StringValue(""), None, IncompatibleTypesException, id="StringValue"),
        pytest.param(IntegerArrayValue(values=[1, 2]), RealArrayValue(values=[1.0, 2.0]), None,
                     id="IntegerArrayValue"),
        pytest.param(RealArrayValue(values=[1, 2]), RealArrayValue(values=[1, 2]), None,
                     id="RealArrayValue"),
        pytest.param(BooleanArrayValue(values=[True, False]), RealArrayValue(values=[1.0, 0.0]),
                     None, id="BooleanArrayValue"),
        pytest.param(StringArrayValue(values=["1", "2.5"]), RealArrayValue(values=[1.0, 2.5]), None,
                     id="StringArrayValue"),
    ])
def test_visit(value: IVariableValue,
               expected_result: RealArrayValue,
               expected_exception: BaseException):
    """Verify that ToRealArrayVisitor gets the expected result, or that the expected exception is
    raised."""

    with _create_exception_context(expected_exception):
        instance = ToRealArrayVisitor()
        try:
            # SUT
            result: RealArrayValue = value.accept(instance)

            # Verify (no exception)
            assert result == expected_result

        except IncompatibleTypesException as e:
            # Verify (expected exception)
            assert e.message == \
                   ("Error: Cannot convert from type {0} to type {1}.\n"
                    "Reason: The types are incompatible.") \
                   .format(value.__class__.__name__, RealArrayValue.__name__)
            raise e
