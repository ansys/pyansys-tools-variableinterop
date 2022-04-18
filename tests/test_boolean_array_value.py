"""Tests for BooleanArrayValue."""
from typing import Dict

import numpy
import pytest

from ansys.common.variableinterop import BooleanArrayValue


# @pytest.mark.skip('bool array nditer returning array of bool instead of a bool for each element')
@pytest.mark.parametrize(
    'source,expected_result',
    [
        pytest.param(BooleanArrayValue(values=[True]), 'True', id='Single value'),
        pytest.param(BooleanArrayValue(values=[False, True, False]),
                     'False,True,False', id='Single dim'),
        pytest.param(BooleanArrayValue(values=[[True], [False]]),
                     'bounds[2,1]{True,False}',
                     id='Two dims'),
        pytest.param(BooleanArrayValue(values=[
            [[False, True, False], [True, False, True]],
            [[False, False, True], [True, False, False]]]),
            'bounds[2,2,3]{False,True,False,True,False,True,False,False,True,True,False,False}',
            id='Three dims'),
    ]
)
def test_to_api_string(source: BooleanArrayValue, expected_result: str) -> None:
    """
    Verify to_api_string for BooleanArrayValue with valid cases.

    Parameters
    ----------
    source : BooleanArrayValue
        The original BooleanArrayValue.
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
        pytest.param('True', BooleanArrayValue(values=[True]), id='Single value'),
        pytest.param('False,True,False', BooleanArrayValue(values=[False, True, False]),
                     id='Single dim'),
        pytest.param('bounds[2,1]{True,False}', BooleanArrayValue(values=[[True], [False]]),
                     id='Two dims'),
        pytest.param(
            'bounds[2,2,3]{False,True,False,True,False,True,False,False,True,True,False,False}',
            BooleanArrayValue(values=[
                [[False, True, False], [True, False, True]],
                [[False, False, True], [True, False, False]]]),
            id='Three dims'),
    ]
)
def test_from_api_string_valid(source: str, expected_result: BooleanArrayValue) -> None:
    """
    Verify that valid cases work on BooleanArrayValue.from_api_string

    Parameters
    ----------
    source : str
        The string to parse.
    expected_result : BooleanArrayValue
        The expected result.
    """
    # Execute
    result: BooleanArrayValue = BooleanArrayValue.from_api_string(source)

    # Verify
    assert isinstance(result, BooleanArrayValue)
    assert numpy.array_equal(result, expected_result)


def test_hash_as_dict_keys() -> None:
    """
    Simple test of hashing by using array value as keys in a dictionary.
    """
    # SUT
    test_value = BooleanArrayValue(values=[True, False])
    copy_value = test_value.clone()
    other_value = BooleanArrayValue(values=[True, True])
    d: Dict[BooleanArrayValue, int] = dict()
    d[test_value] = 0
    d[copy_value] = 1
    d[other_value] = 2

    # Verify
    # Dict length should be 2, as copy_value should collide (and overwrite) test_value
    assert len(d) == 2
    assert d[test_value] == 1
    assert d[other_value] == 2
