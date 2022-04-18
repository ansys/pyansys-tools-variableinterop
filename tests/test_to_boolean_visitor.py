"""Unit tests of ToBooleanValueVisitor"""
import sys

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import (
    BooleanValue,
    IntegerValue,
    IVariableValue,
    RealValue,
    StringValue,
    ToBooleanVisitor,
)


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        # Boolean to Boolean Tests
        pytest.param(BooleanValue(True), (True), None, id="BoolValue(True)"),
        pytest.param(BooleanValue(False), (False), None, id="BoolValue(False)"),
        # Integer to Boolean Tests
        pytest.param(
            IntegerValue(
                numpy.iinfo(numpy.int64).min), True, None, id="IntegerValue(MIN)"),
        pytest.param(IntegerValue(-1), True, None, id="IntegerValue(-1)"),
        pytest.param(IntegerValue(0), False, None, id="IntegerValue(0)"),
        pytest.param(IntegerValue(1), True, None, id="IntegerValue(1)"),
        pytest.param(
            IntegerValue(
                numpy.iinfo(numpy.int64).max), (True), None, id="IntegerValue(MAX)"),
        # Real to Boolean Tests
        pytest.param(RealValue(float("-inf")), (True), None, id="RealValue(-∞)"),
        pytest.param(
            RealValue(-sys.float_info.max), (True), None, id="RealValue(-MAX)"),
        pytest.param(RealValue(-1.0), (True), None, id="RealValue(-1.0)"),
        pytest.param(
            RealValue(-sys.float_info.epsilon), (True), None, id="RealValue(-ε)"),
        pytest.param(
            RealValue(-sys.float_info.min), (True), None, id="RealValue(-MIN)"),
        pytest.param(RealValue(-0.0), (False), None, id="RealValue(-0.0)"),
        pytest.param(RealValue(0.0), (False), None, id="RealValue(0.0)"),
        pytest.param(RealValue(sys.float_info.min), (True), None, id="RealValue(MIN)"),
        pytest.param(
            RealValue(sys.float_info.epsilon), (True), None, id="RealValue(ε)"),
        pytest.param(RealValue(1.0), (True), None, id="RealValue(1.0)"),
        pytest.param(RealValue(sys.float_info.max), (True), None, id="RealValue(MAX)"),
        pytest.param(RealValue(float("inf")), (True), None, id="RealValue(∞)"),
        pytest.param(RealValue(float("nan")), (True), None, id="RealValue(NAN)"),
        # String to Bool Tests
        pytest.param(StringValue("True"), (True), None, id="StringValue(True)"),
        pytest.param(StringValue("False"), (False), None, id="StringValue(False)"),
        pytest.param(StringValue("Y"), (True), None, id="StringValue(Y)"),
        pytest.param(StringValue("N"), (False), None, id="StringValue(N)"),
        pytest.param(StringValue("yes"), (True), None, id="StringValue(yes)"),
        pytest.param(StringValue("no"), (False), None, id="StringValue(no)"),
        pytest.param(StringValue("  true  "), (True), None, id="StringValue(  true  )"),
        pytest.param(
            StringValue("  false  "), (False), None, id="StringValue(  false  )"),
        pytest.param(StringValue("  TRUE  "), (True), None, id="StringValue(  TRUE  )"),
        pytest.param(
            StringValue("  FALSE  "), (False), None, id="StringValue(  FALSE  )"),
        pytest.param(
            StringValue(str(numpy.iinfo(numpy.int64).min)), (True), None,
            id="StringValue(INT64_MIN)"),
        pytest.param(StringValue("-1"), (True), None, id="StringValue(-1)"),
        pytest.param(StringValue("0"), (False), None, id="StringValue(0)"),
        pytest.param(StringValue("1"), (True), None, id="StringValue(1)"),
        pytest.param(
            StringValue(str(numpy.iinfo(numpy.int64).max)), (True), None,
            id="StringValue(INT64_MAX)"),
        pytest.param(
            StringValue("1234567890123456789"), (True), None,
            id="StringValue(1234567890123456789)"),
        pytest.param(StringValue("-inf"), (True), None, id="StringValue(-inf)"),
        pytest.param(
            StringValue(str(-sys.float_info.max)), (True), None,
            id="StringValue(-DLB_MAX)"),
        pytest.param(StringValue("-1.0"), (True), None, id="StringValue(-1.0)"),
        pytest.param(
            StringValue(str(-sys.float_info.epsilon)), (True), None,
            id="StringValue(-DBL_EPSILON)"),
        pytest.param(
            StringValue(str(-sys.float_info.min)), (True), None,
            id="StringValue(-DBL_MIN)"),
        pytest.param(StringValue("-0.0"), (False), None, id="StringValue(-0.0)"),
        pytest.param(StringValue("0.0"), (False), None, id="StringValue(0.0)"),
        pytest.param(
            StringValue(str(sys.float_info.min)), (True), None,
            id="StringValue(DLB_MIN)"),
        pytest.param(
            StringValue(str(sys.float_info.epsilon)), (True), None,
            id="StringValue(DBL_EPSILON)"),
        pytest.param(StringValue("1.0"), (True), None, id="StringValue(1.0)"),
        pytest.param(
            StringValue(str(sys.float_info.max)), (True), None,
            id="StringValue(DBL_MAX)"),
        pytest.param(StringValue("inf"), (True), None, id="StringValue(inf)"),
        pytest.param(StringValue("nan"), (True), None, id="StringValue(nan)"),
        # Other Types
        #  TODO: IntegerArray
        #  TODO: RealArray
        #  TODO: BooleanArray
        #  TODO: StringArray
    ]
)
def test_to_boolean_visitor(
        source: IVariableValue,
        expect: bool,
        expect_exception: BaseException
) -> None:
    """
    Tests ToBoolVisitor handling of various input IVariableValues
    :param source: Source value to test visitor against
    :param expect: Expected return value from visitor, None if
        expected to throw.
    :param expect_exception: Expected exception to be thrown from
            visitor, None if expected to return a value.
    """
    sut = ToBooleanVisitor()
    with _create_exception_context(expect_exception):
        result: IVariableValue = source.accept(sut)
        assert type(result) == type(expect)
        assert result == expect
