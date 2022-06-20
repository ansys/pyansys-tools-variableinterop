from pathlib import Path

import numpy
from test_file_value import _TestFileValue

import ansys.common.variableinterop as acvi


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
            _TestFileValue("/test/file.bin", "application/bytestream", None, None),
            _TestFileValue("/test/file.htm", "text/html", "UTF-8", None),
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
            _TestFileValue(None, "application/bytestream", None, None).set_content_override(),
            _TestFileValue(
                Path("file_path_here"), "application/bytestream", None, None
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
