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

from pathlib import Path

import numpy

import ansys.tools.variableinterop as acvi
from test_file_value import _TestFileValue


def test_default_construct() -> None:
    result = acvi.FileArrayValue()

    assert type(result) is acvi.FileArrayValue
    assert numpy.shape(result) == ()


def test_shape_construct() -> None:
    result = acvi.FileArrayValue(shape_=(2, 4, 9))

    assert type(result) is acvi.FileArrayValue
    assert numpy.shape(result) == (2, 4, 9)


def test_construct_1d():
    # Execute
    sut: acvi.FileArrayValue = acvi.FileArrayValue(
        values=[
            acvi.EMPTY_FILE,
            _TestFileValue(
                "/test/file.bin", "application/bytestream", None, None, None, Path("/test/file.bin")
            ),
            _TestFileValue(
                "/test/file.htm", "text/html", "UTF-8", None, None, Path("/test/file.htm")
            ),
        ]
    )

    # Verify
    assert len(sut) == 3
    assert sut[0] is acvi.EMPTY_FILE

    test_bin_file: acvi.FileValue = sut[1]
    assert test_bin_file.original_file_name == "/test/file.bin"
    assert test_bin_file.mime_type == "application/bytestream"

    test_html_file: acvi.FileValue = sut[2]
    assert test_html_file.original_file_name == "/test/file.htm"
    assert test_html_file.mime_type == "text/html"


def test_to_display_string():
    # Setup
    sut: acvi.FileArrayValue = acvi.FileArrayValue(
        values=[
            acvi.EMPTY_FILE,
            _TestFileValue(
                None, "application/bytestream", None, None, None, None
            ).set_content_override(),
            _TestFileValue(
                Path("file_path_here"),
                "application/bytestream",
                None,
                None,
                None,
                Path("file_path_here"),
            ).set_content_override(),
        ]
    )

    # Execute
    result: str = sut.to_display_string("locale ignored")

    # Verify
    assert (
        result == "<empty file>,<file read from unknown location>,"
        "<file read from file_path_here>"
    )
