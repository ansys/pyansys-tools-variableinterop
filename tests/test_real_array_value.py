"""Tests for RealArrayValue."""
from typing import Dict

import numpy
import pytest

from ansys.common.variableinterop import RealArrayValue


@pytest.mark.parametrize(
    'source,expected_result',
    [
        pytest.param(RealArrayValue(values=[4.2]), '4.2', id='Single value'),
        pytest.param(RealArrayValue(values=[3.14, 4.25, 5.36]), '3.14,4.25,5.36', id='Single dim'),
        pytest.param(RealArrayValue(values=[[1.7976931348623157E+308], [-1.7976931348623157E+308]]),
                     'bounds[2,1]{1.7976931348623157e+308,-1.7976931348623157e+308}',
                     id='Two dims'),
        pytest.param(RealArrayValue(values=[
            [[1.1, 2.2, 3.3], [4.4, 5.5, 6.6]],
            [[7.7, 8.8, 9.9], [10.0, -11.1, -12.2]]]),
                     'bounds[2,2,3]{1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,10.0,-11.1,-12.2}',
                     id='Three dims'),
    ]
)
def test_to_api_string(source: RealArrayValue, expected_result: str) -> None:
    """
    Verify to_api_string for RealArrayValue with valid cases.

    Parameters
    ----------
    source : RealArrayValue
        The original RealArrayValue.
    expected_result : str
        The expected API string.
    """
    # Execute
    result: str = source.to_api_string()

    # Verify
    assert type(result) is str
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param('4.2', RealArrayValue(values=[4.2]), id='Single value'),
        pytest.param('3.14,4.25,5.36', RealArrayValue(values=[3.14, 4.25, 5.36]), id='Single dim'),
        pytest.param('bounds[2,1]{1.7976931348623157e+308,-1.7976931348623157e+308}',
                     RealArrayValue(values=[[1.7976931348623157E+308], [-1.7976931348623157E+308]]),
                     id='Two dims'),
        pytest.param('bounds[2,2,3]{1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,10.0,-11.1,-12.2}',
                     RealArrayValue(values=[
                         [[1.1, 2.2, 3.3], [4.4, 5.5, 6.6]],
                         [[7.7, 8.8, 9.9], [10.0, -11.1, -12.2]]]),
                     id='Three dims'),
    ]
)
def test_from_api_string_valid(source: str, expected_result: RealArrayValue) -> None:
    """
    Verify that valid cases work on RealArrayValue.from_api_string

    Parameters
    ----------
    source : str
        The string to parse.
    expected_result : RealArrayValue
        The expected result.
    """
    # Execute
    result: RealArrayValue = RealArrayValue.from_api_string(source)

    # Verify
    assert isinstance(result, RealArrayValue)
    assert numpy.array_equal(result, expected_result)


def test_hash_as_dict_keys() -> None:
    """
    Simple test of hashing by using array value as keys in a dictionary.
    """
    # SUT
    test_value = RealArrayValue(values=[1.0, 1.5])
    copy_value = test_value.clone()
    other_value = RealArrayValue(values=[1.0, 1.6])
    d: Dict[RealArrayValue, int] = dict()
    d[test_value] = 0
    d[copy_value] = 1
    d[other_value] = 2

    # Verify
    # Dict length should be 2, as copy_value should collide (and overwrite) test_value
    assert len(d) == 2
    assert d[test_value] == 1
    assert d[other_value] == 2
