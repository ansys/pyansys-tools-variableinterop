import numpy
import pytest

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


def test_clone() -> None:
    """Verifies that clone returns a new StringValue with the same value."""
    # Setup
    sut: StringValue = StringValue("word")

    # SUT
    result: StringValue = sut.clone()

    # Verification
    assert result is not sut
    assert result == "word"
