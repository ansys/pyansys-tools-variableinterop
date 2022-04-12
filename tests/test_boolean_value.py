from typing import Any

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import BooleanValue


@pytest.mark.parametrize(
    "arg,expect_equality",
    [
        pytest.param(True, numpy.bool_(True), id="true"),
        pytest.param(False, numpy.bool_(False), id="false"),
        pytest.param(None, numpy.bool_(False), id="none"),

        # TODO: Should we even accept strings?
        pytest.param("", numpy.bool_(False), id="empty-string"),
        pytest.param("something", numpy.bool_(True), id="non-empty-string"),
        pytest.param("false", numpy.bool_(True), id="non-empty-string-says-false"),
    ])
def test_construct(arg: Any, expect_equality: numpy.bool_) -> None:
    """Verify that __init__ for BooleanValue correctly instantiates the superclass data"""
    instance: BooleanValue = BooleanValue(arg)
    assert instance == expect_equality


@pytest.mark.parametrize(
    "arg,expected_result",
    [
        pytest.param('True', BooleanValue(True), id='True'),
        pytest.param('TRUE', BooleanValue(True), id='TRUE'),
        pytest.param('true', BooleanValue(True), id='true'),
        pytest.param('TrUe', BooleanValue(True), id='TrUe'),
        pytest.param('False', BooleanValue(False), id='False'),
        pytest.param('FALSE', BooleanValue(False), id='FALSE'),
        pytest.param('false', BooleanValue(False), id='false'),
        pytest.param('FaLsE', BooleanValue(False), id='FaLsE'),
        pytest.param('Yes', BooleanValue(True), id='Yes'),
        pytest.param('YES', BooleanValue(True), id='YES'),
        pytest.param('y', BooleanValue(True), id='y'),
        pytest.param('Y', BooleanValue(True), id='Y'),
        pytest.param('No', BooleanValue(False), id='No'),
        pytest.param('no', BooleanValue(False), id='no'),
        pytest.param('n', BooleanValue(False), id='n'),
        pytest.param('N', BooleanValue(False), id='N'),
        pytest.param('0', BooleanValue(False), id='zero'),
        pytest.param('0.0', BooleanValue(False), id='zero point zero'),
        pytest.param('1', BooleanValue(True), id='one point zero'),
        pytest.param('1.0', BooleanValue(True), id='one point zero'),
        pytest.param('true \r\n\t', BooleanValue(True), id='trailing whitespace true'),
        pytest.param('false \r\n\t', BooleanValue(False), id='trailing whitespace false'),
        pytest.param('\r\n\t true', BooleanValue(True), id='leading whitespace true'),
        pytest.param('\r\n\t false', BooleanValue(False), id='leading whitespace false'),
        pytest.param('NaN', BooleanValue(True), id='NaN'),
        pytest.param('Infinity', BooleanValue(True), id='infinity'),
        pytest.param('-Infinity', BooleanValue(True), id='negative infinity'),
    ]
)
def test_from_api_string_valid(arg: str, expected_result: BooleanValue) -> None:
    """
    Verify that BooleanValue.from_api_string works for valid cases
    Parameters
    ----------
    arg the string to parse
    expected_result the expected result
    """
    #Execute
    result: BooleanValue = BooleanValue.from_api_string(arg)

    assert result == expected_result


@pytest.mark.parametrize(
    "arg,expected_exception",
    [
        pytest.param('', ValueError, id='empty'),
        pytest.param(' \t\n\r', ValueError, id='all whitespace'),
        pytest.param('4,555', ValueError, id='Number with thousands separator'),
        pytest.param(None, TypeError, id='None')
    ]
)
def test_from_api_string_invalid(arg: str, expected_exception: BaseException) -> None:
    with _create_exception_context(expected_exception):
        result: BooleanValue = BooleanValue.from_api_string(arg)


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(BooleanValue(True), 'True', id='true'),
        pytest.param(BooleanValue(False), 'False', id='false'),
    ]
)
def test_to_api_string(source: BooleanValue, expected_result: str) -> None:
    """
    Verify that to_api_string for BooleanValue works correctly for valid cases.
    Parameters
    ----------
    source the original BooleanValue
    expected_value the expected API string
    """
    # Execute
    # TODO: restore this once we have a fully independent BooleanValue implementation
    # result: str = source.to_api_string()
    result: str = str(source)

    # Verify
    assert type(result) is str
    assert result == expected_result


@pytest.mark.skip("Enable when bool type fixed")
def test_clone() -> None:
    """Verifies that clone returns a new BooleanValue with the same value."""
    # Setup
    sut: BooleanValue = BooleanValue(True)

    # SUT
    result: BooleanValue = sut.clone()

    # Verification
    assert result is not sut
    assert result is True
