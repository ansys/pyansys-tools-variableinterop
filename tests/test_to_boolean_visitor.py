"""Unit tests of ToBooleanVisitor"""
import sys

import numpy
import pytest

from ansys.common.variableinterop import IVariableValue, BooleanValue, IntegerValue, RealValue, ToBooleanVisitor
from tests.test_utils import _create_exception_context


@pytest.mark.parametrize(
    "source,expect,expect_exception",
    [
        # Boolean to Boolean Tests
        (BooleanValue(True), BooleanValue(True), None),
        (BooleanValue(False), BooleanValue(False), None),
        # Integer to Boolean Tests
        (IntegerValue(numpy.iinfo(numpy.int64).min), BooleanValue(True), None),
        (IntegerValue(-1), BooleanValue(True), None),
        (IntegerValue(0), BooleanValue(False), None),
        (IntegerValue(1), BooleanValue(True), None),
        (IntegerValue(numpy.iinfo(numpy.int64).max), BooleanValue(True), None),
        # Real to Boolean Tests
        (RealValue(float("-inf")), BooleanValue(True), None),
        (RealValue(sys.float_info.min), BooleanValue(True), None),
        (RealValue(-1.0), BooleanValue(True), None),
        (RealValue(-sys.float_info.epsilon), BooleanValue(True), None),
        (RealValue(-0.0), BooleanValue(False), None),
        (RealValue(0.0), BooleanValue(False), None),
        (RealValue(sys.float_info.epsilon), BooleanValue(True), None),
        (RealValue(1.0), BooleanValue(True), None),
        (RealValue(float("inf")), BooleanValue(True), None),
        (RealValue(float("nan")), BooleanValue(True), None),
        # Other Types
        #  TODO: IntegerArray
        #  TODO: RealArray
        #  TODO: BooleanArray
        #  TODO: StringArray
    ]
)
def test_to_boolean_visitor(
        source: IVariableValue,
        expect: BooleanValue,
        expect_exception: BaseException
) -> None:
    """
    Tests ToBooleanVisitor handling of various input IVariableValues
    :param source: Source value to test visitor against
    :param expect: Expected return value from visitor, None if
        expected to throw.
    :param expect_exception: Expected exception to be thrown from
            visitor, None if expected to return a value.
    """
    sut = ToBooleanVisitor()
    with _create_exception_context(expect_exception):
        result: IVariableValue = source.accept(sut)
        assert type(expect) == type(result)
        assert expect == result



