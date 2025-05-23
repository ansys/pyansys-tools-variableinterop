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
"""Tests for StringArrayValue."""
import numpy
import pytest

from ansys.tools.variableinterop import StringArrayValue


def test_default_construct() -> None:
    result = StringArrayValue()

    assert type(result) is StringArrayValue
    assert numpy.shape(result) == ()


def test_shape_construct() -> None:
    result = StringArrayValue(shape_=(2, 4, 9))

    assert type(result) is StringArrayValue
    assert numpy.shape(result) == (2, 4, 9)


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(StringArrayValue(values=["foo"]), '"foo"', id="Single value"),
        pytest.param(StringArrayValue(values=["a", "b", "c"]), '"a","b","c"', id="Single dim"),
        pytest.param(
            StringArrayValue(values=[["asdf"], ["qwerty"]]),
            'bounds[2,1]{"asdf","qwerty"}',
            id="Two dims",
        ),
        pytest.param(
            StringArrayValue(
                values=[
                    [["あ", "い", "う"], ["え", "お", "か"]],
                    [["き", "く", "け"], ["こ", "が", "ぎ"]],
                ]
            ),
            'bounds[2,2,3]{"あ","い","う","え","お","か",' + '"き","く","け","こ","が","ぎ"}',
            id="Three dims",
        ),
        pytest.param(
            StringArrayValue(
                values=[
                    'doublequote>"<',
                    "backslash>\\<",
                    "whitespace>\r\n\t<",
                    "null>\0<",
                    "contains, commas",
                ]
            ),
            r'"doublequote>\"<","backslash>\\<","whitespace>\r\n\t<","null>\0<","contains, commas"',
            id="escapes",
        ),
    ],
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
        pytest.param('"foo"', StringArrayValue('"foo"', values=["foo"]), id="Single value"),
        pytest.param(
            '"a","b","c"', StringArrayValue('"a","b","c"', values=["a", "b", "c"]), id="Single dim"
        ),
        pytest.param(
            'bounds[2,1]{"asdf","qwerty"}',
            StringArrayValue(values=[["asdf"], ["qwerty"]]),
            id="Two dims",
        ),
        pytest.param(
            'bounds[2,2,3]{"あ","い","う","え","お","か",' + '"き","く","け","こ","が","ぎ"}',
            StringArrayValue(
                values=[
                    [["あ", "い", "う"], ["え", "お", "か"]],
                    [["き", "く", "け"], ["こ", "が", "ぎ"]],
                ]
            ),
            id="Three dims",
        ),
        pytest.param(
            r'"doublequote>\"<","backslash>\\<","whitespace>\r\n\t<","null>\0<"'
            r',"unr\e\cogniz\ed","contains, commas"',
            StringArrayValue(
                values=[
                    'doublequote>"<',
                    "backslash>\\<",
                    "whitespace>\r\n\t<",
                    "null>\0<",
                    "unrecognized",
                    "contains, commas",
                ]
            ),
            id="escapes",
        ),
    ],
)
def test_from_api_string_valid(source: str, expected_result: StringArrayValue) -> None:
    """
    Verify that valid cases work on StringArrayValue.from_api_string.

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
