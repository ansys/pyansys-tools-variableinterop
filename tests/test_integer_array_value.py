"""Tests for IntegerArrayValue."""
import numpy
import pytest

from ansys.tools.variableinterop import IntegerArrayValue


def test_default_construct() -> None:
    result = IntegerArrayValue()

    assert type(result) is IntegerArrayValue
    assert numpy.shape(result) == ()


def test_shape_construct() -> None:
    result = IntegerArrayValue(shape_=(2, 4, 9))

    assert type(result) is IntegerArrayValue
    assert numpy.shape(result) == (2, 4, 9)


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(IntegerArrayValue(values=[42]), "42", id="0d"),
        pytest.param(IntegerArrayValue(values=[1, 2, 3]), "1,2,3", id="1d"),
        pytest.param(IntegerArrayValue(values=[[1, 2], [3, 4]]), "bounds[2,2]{1,2,3,4}", id="2d"),
        pytest.param(
            IntegerArrayValue(values=[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, -11, -12]]]),
            "bounds[2,2,3]{1,2,3,4,5,6,7,8,9,10,-11,-12}",
            id="3d",
        ),
        pytest.param(
            IntegerArrayValue(values=[-9223372036854775808, 9223372036854775807]),
            "-9223372036854775808,9223372036854775807",
            id="min and max 64 bit",
        ),
    ],
)
def test_to_api_string(source: IntegerArrayValue, expected_result: str) -> None:
    """
    Verify to_api_string for IntegerArrayValue with valid cases.

    Parameters
    ----------
    source : IntegerArrayValue
        The original IntegerArrayValue.
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
        pytest.param("42", IntegerArrayValue(values=[42]), id="0d"),
        pytest.param("1,2,3", IntegerArrayValue(values=[1, 2, 3]), id="1d"),
        pytest.param("bounds[2,2]{1,2,3,4}", IntegerArrayValue(values=[[1, 2], [3, 4]]), id="2d"),
        pytest.param(
            "bounds[2,2,3]{1,2,3,4,5,6,7,8,9,10,-11,-12}",
            IntegerArrayValue(values=[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, -11, -12]]]),
            id="3d",
        ),
        pytest.param(
            "-9223372036854775808,9223372036854775807",
            IntegerArrayValue(values=[-9223372036854775808, 9223372036854775807]),
            id="min and max 64 bit",
        ),
    ],
)
def test_from_api_string_valid(source: str, expected_result: IntegerArrayValue) -> None:
    """
    Verify that valid cases work on IntegerArrayValue.from_api_string.

    Parameters
    ----------
    source : str
        The string to parse.
    expected_result : IntegerArrayValue
        The expected result.
    """
    # Execute
    result: IntegerArrayValue = IntegerArrayValue.from_api_string(source)

    # Verify
    assert isinstance(result, IntegerArrayValue)
    assert numpy.array_equal(result, expected_result)
