"""Tests for StringArrayValue."""
import numpy
import pytest

from ansys.common.variableinterop import StringArrayValue


@pytest.mark.parametrize(
    'source,expected_result',
    [
        pytest.param(StringArrayValue(values=['foo']), '\"foo\"', id='Single value'),
        pytest.param(StringArrayValue(values=['a', 'b', 'c']),
                     '\"a\",\"b\",\"c\"', id='Single dim'),
        pytest.param(StringArrayValue(values=[['asdf'], ['qwerty']]),
                     'bounds[2,1]{\"asdf\",\"qwerty\"}',
                     id='Two dims'),
        pytest.param(StringArrayValue(values=[
            [["あ", "い", "う"], ["え", "お", "か"]],
            [["き", "く", "け"], ["こ", "が", "ぎ"]]]),
            'bounds[2,2,3]{\"あ\",\"い\",\"う\",\"え\",\"お\",\"か\",' +
            '\"き\",\"く\",\"け\",\"こ\",\"が\",\"ぎ\"}',
            id='Three dims'),
    ]
)
def test_to_api_string(source: StringArrayValue, expected_result: str) -> None:
    """
    Verify to_api_string for StringArrayValue with valid cases.

    Parameters
    ----------
    source : StringArrayValue
        The original StringArrayValue.
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
        pytest.param('\"foo\"', StringArrayValue('\"foo\"', values=['foo']), id='Single value'),
        pytest.param('\"a\",\"b\",\"c\"',
                     StringArrayValue('\"a\",\"b\",\"c\"', values=['a', 'b', 'c']),
                     id='Single dim'),
        pytest.param('bounds[2,1]{\"asdf\",\"qwerty\"}',
                     StringArrayValue(values=[['asdf'], ['qwerty']]),
                     id='Two dims'),
        pytest.param('bounds[2,2,3]{\"あ\",\"い\",\"う\",\"え\",\"お\",\"か\",' +
                     '\"き\",\"く\",\"け\",\"こ\",\"が\",\"ぎ\"}',
                     StringArrayValue(values=[
                         [["あ", "い", "う"], ["え", "お", "か"]],
                         [["き", "く", "け"], ["こ", "が", "ぎ"]]]),
                     id='Three dims'),
    ]
)
def test_from_api_string_valid(source: str, expected_result: StringArrayValue) -> None:
    """
    Verify that valid cases work on StringArrayValue.from_api_string

    Parameters
    ----------
    source : str
        The string to parse.
    expected_result : StringArrayValue
        The expected result.
    """
    # Execute
    result: StringArrayValue = StringArrayValue.from_api_string(source)

    # Verify
    assert isinstance(result, StringArrayValue)
    assert numpy.array_equal(result, expected_result)
