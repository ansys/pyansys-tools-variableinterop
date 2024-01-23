# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

import pytest

import ansys.tools.variableinterop as acvi


@pytest.mark.parametrize(
    "unescaped,expected_output",
    [
        pytest.param("", "", id="empty string"),
        pytest.param("no escaping necessary", "no escaping necessary", id="no escaping necessary"),
        pytest.param("whitespace>\t\r\n", r"whitespace>\t\r\n", id="escaped whitespace"),
        pytest.param('doublequote>"', r"doublequote>\"", id="quote"),
        pytest.param(r"backslash>\<", r"backslash>\\<", id="backslash"),
        pytest.param("null>\0<", r"null>\0<", id="null"),
    ],
)
def test_escape_string(unescaped: str, expected_output: str):
    output: str = acvi.escape_string(unescaped)

    assert isinstance(output, str)
    assert output == expected_output


@pytest.mark.parametrize(
    "escaped,expected_output",
    [
        pytest.param("", "", id="empty string"),
        pytest.param("no escaping necessary", "no escaping necessary", id="no escaping necessary"),
        pytest.param(r"whitespace>\t\r\n", "whitespace>\t\r\n", id="escaped whitespace"),
        pytest.param(r"doublequote>\"", 'doublequote>"', id="quote"),
        pytest.param(r"backslash>\\<", r"backslash>\<", id="backslash"),
        pytest.param(r"null>\0<", "null>\0<", id="null"),
        pytest.param(
            r"unr\ecogn\ized \esc\ap\es", "unrecognized escapes", id="drops unrecognized escapes"
        ),
    ],
)
def test_unescape_string(escaped: str, expected_output: str):
    output: str = acvi.unescape_string(escaped)

    assert isinstance(output, str)
    assert output == expected_output
