# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy
import pytest

from ansys.tools.variableinterop import BooleanValue, IntegerValue, RealValue, StringValue
from test_utils import _create_exception_context


@pytest.mark.parametrize(
    "arg,expect_equality",
    [
        pytest.param("", numpy.str_(""), id="empty"),
        pytest.param("ASCII-only", numpy.str_("ASCII-only"), id="ascii-codespace"),
        pytest.param(
            "(ノ-_-)ノ ミᴉᴉɔsɐ-uou", numpy.str_("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), id="unicode-codespace"
        ),
        pytest.param(None, numpy.str_("None"), id="None"),
        pytest.param(IntegerValue(0), numpy.str_("0"), id="from IntegerValue -1"),
        pytest.param(
            IntegerValue(9223372036854775807),
            numpy.str_("9223372036854775807"),
            id="from IntegerValue max",
        ),
        pytest.param(
            IntegerValue(-9223372036854775808),
            numpy.str_("-9223372036854775808"),
            id="from IntegerValue min",
        ),
        pytest.param(IntegerValue(0), numpy.str_("0"), id="from IntegerValue zero"),
        pytest.param(
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            numpy.str_("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            id="from other StringValue",
        ),
        pytest.param(
            RealValue(1.7976931348623157e308), "1.7976931348623157e+308", id="From RealValue max"
        ),
        pytest.param(
            RealValue(-1.7976931348623157e308), "-1.7976931348623157e+308", id="From RealValue min"
        ),
        pytest.param(RealValue(0.0), "0.0", id="From RealValue 0"),
        pytest.param(
            RealValue(2.2250738585072014e-308),
            "2.2250738585072014e-308",
            id="from RealValue epsilon",
        ),
        pytest.param(
            RealValue(1.0000000000000002), "1.0000000000000002", id="from RealValue epsilon+1"
        ),
        pytest.param(BooleanValue(True), numpy.str_("True"), id="from BooleanValue true"),
        pytest.param(BooleanValue(False), numpy.str_("False"), id="from BooleanValue false"),
    ],
)
def test_construct(arg: str, expect_equality: numpy.str_) -> None:
    """Verify that __init__ for StringValue correctly instantiates the superclass
    data."""
    instance: StringValue = StringValue(arg)
    assert instance == expect_equality


@pytest.mark.parametrize(
    "source,expected_value",
    [
        pytest.param("", StringValue(""), id="empty"),
        pytest.param(" \t\r\n", StringValue(" \t\r\n"), id="whitespace only"),
        pytest.param("ASCII-only", StringValue("ASCII-only"), id="ascii-codespace"),
        pytest.param(
            "(ノ-_-)ノ ミᴉᴉɔsɐ-uou", StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), id="unicode-codespace"
        ),
        pytest.param(
            'Escapes>\n\r\t\\"<',
            StringValue('Escapes>\n\r\t\\"<'),
            id="characters escaped in formatted string unmodified",
        ),
    ],
)
def test_from_api_string(source: str, expected_value: StringValue) -> None:
    """
    Verify that from_api_string for StringValue works correctly for valid cases.

    Parameters
    ----------
    source : str
        The source string.
    expected_value : StringValue
        The expected value.
    """
    # Execute
    result: StringValue = StringValue.from_api_string(source)

    # Verify
    assert type(result) is StringValue
    assert result == expected_value


def test_from_api_string_rejects_none() -> None:
    """Verify that from_api_string cannot be called with None."""
    with _create_exception_context(TypeError):
        result: StringValue = StringValue.from_api_string(None)


@pytest.mark.parametrize(
    "source,expected_value",
    [
        pytest.param(StringValue(""), "", id="empty"),
        pytest.param(StringValue(" \t\r\n"), " \t\r\n", id="whitespace only"),
        pytest.param(StringValue("ASCII-only"), "ASCII-only", id="ascii-codespace"),
        pytest.param(
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"), "(ノ-_-)ノ ミᴉᴉɔsɐ-uou", id="unicode-codespace"
        ),
        pytest.param(
            StringValue('Escapes>\n\r\t\\"<'),
            'Escapes>\n\r\t\\"<',
            id="characters escaped in formatted string unmodified",
        ),
    ],
)
def test_to_api_string(source: StringValue, expected_value: str) -> None:
    """
    Verify that to_api_string for StringValue works correctly for valid cases.

    Parameters
    ----------
    source : str
        The original StringValue.
    expected_value : StringValue
        The expected API string.
    """
    # Execute
    result: str = source.to_api_string()

    # Verify
    assert type(result) is str
    assert result == expected_value


def test_clone() -> None:
    """Verifies that clone returns a new StringValue with the same value."""
    # Setup
    sut: StringValue = StringValue("word")

    # SUT
    result: StringValue = sut.clone()

    # Verification
    assert result is not sut
    assert result == "word"
