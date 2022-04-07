import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import StringValue


@pytest.mark.parametrize(
    "arg,expect_equality",
    [
        pytest.param("", numpy.str_(""), id="empty"),
        pytest.param("ASCII-only", numpy.str_("ASCII-only"), id="ascii-codespace"),
        pytest.param("(ノ-_-)ノ ミᴉᴉɔsɐ-uou", numpy.str_("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
                     id="unicode-codespace"),

        # It's weird, but this is actually how numpy.str_ and the built-in Python strings work.
        # Do we want this?
        pytest.param(None, numpy.str_("None"), id="None"),
    ])
def test_construct(arg: str, expect_equality: numpy.str_) -> None:
    """Verify that __init__ for StringValue correctly instantiates the superclass data"""
    instance: StringValue = StringValue(arg)
    assert instance == expect_equality


@pytest.mark.parametrize(
    "source,expected_value",
    [
        pytest.param("", StringValue(""), id="empty"),
        pytest.param(" \t\r\n", StringValue(" \t\r\n"), id="whitespace only"),
        pytest.param("ASCII-only", StringValue("ASCII-only"), id="ascii-codespace"),
        pytest.param("(ノ-_-)ノ ミᴉᴉɔsɐ-uou", StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
                     id="unicode-codespace"),
        pytest.param("Escapes>\n\r\t\\\"<", StringValue("Escapes>\n\r\t\\\"<"),
                     id="characters escaped in formatted string unmodified")
    ])
def test_from_api_string(source: str, expected_value: StringValue) -> None:
    """
    Verify that from_api_string for StringValue works correctly for valid cases.
    Parameters
    ----------
    source the source string
    expected_value the expected value
    """
    # Execute
    result: StringValue = StringValue.from_api_string(source)

    # Verify
    assert type(result) is StringValue
    assert result == expected_value


def test_from_api_string_rejects_none() -> None:
    """
    Verify that from_api_string cannot be called with None.
    """
    with _create_exception_context(TypeError):
        result: StringValue = StringValue.from_api_string(None)
