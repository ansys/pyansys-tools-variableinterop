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

import json
import os
from os import PathLike
from pathlib import Path
from typing import Any, Optional, Union
from uuid import UUID

from overrides import overrides
import pytest

import ansys.tools.variableinterop as acvi

test_read_file: Path = Path("in.file")
test_contents: str = "12345"


class _TestFileValue(acvi.LocalFileValue):
    """A concrete implementation of FileValue used to test its constructor."""

    def __init__(
        self,
        original_path: Optional[PathLike],
        mime_type: Optional[str],
        encoding: Optional[str],
        value_id: Optional[UUID],
        file_size: Optional[int],
        actual_content_file_name: Optional[PathLike],
    ):
        super().__init__(
            original_path, mime_type, encoding, value_id, file_size, actual_content_file_name
        )
        self._has_content_override: bool = False

    def set_content_override(self) -> "_TestFileValue":
        """Causes this instance to report it has content regardless of how it was
        constructed."""
        self._has_content_override = True
        return self

    @overrides
    def _has_content(self) -> bool:
        return self._has_content_override or bool(self._original_path)


class __TestSaveContext(acvi.ISaveContext):
    def save_file(self, source: Union[PathLike, str], id: Optional[str]) -> str:
        if not id:
            return "file:///" + str(source).lstrip("/")
        else:
            return id

    #    def save_file_stream(self, source: Union[PathLike, str], id: Optional[str]) -> Tuple[
    #        Stream, str]:
    #        raise NotImplementedError()

    def flush(self) -> None:
        pass

    def close(self) -> None:
        pass


__TEST_UUID = UUID("EC6F3C91-ECBD-4D3D-88F3-05062E41CE9F")
"""A test UUID used to avoid regenerating UUIDs all over the place in the test."""


__EMPTY_UUID = UUID(int=0)
"""Convenience variable for an empty UUID."""


@pytest.mark.parametrize(
    "".join(
        (
            "specified_orig_path,expected_orig_path,",
            "specified_mime_type,expected_mime_type,",
            "specified_encoding,expected_encoding,",
            "specified_value_id,expected_value_id,",
            "specified_size,expected_size",
        )
    ),
    [
        pytest.param(
            "/path/to/orig/file",
            "/path/to/orig/file",
            "text/testfile",
            "text/testfile",
            "Shift-JIS",
            "Shift-JIS",
            __TEST_UUID,
            __TEST_UUID,
            10,
            10,
            id="all arguments specified",
        ),
        pytest.param(
            None,
            None,
            "text/testfile",
            "text/testfile",
            "Shift-JIS",
            "Shift-JIS",
            __TEST_UUID,
            __TEST_UUID,
            10,
            10,
            id="no original path",
        ),
        pytest.param(
            "/path/to/orig/file",
            "/path/to/orig/file",
            None,
            "",
            "Shift-JIS",
            "Shift-JIS",
            __TEST_UUID,
            __TEST_UUID,
            10,
            10,
            id="no mimetype",
        ),
        pytest.param(
            "/path/to/orig/file",
            "/path/to/orig/file",
            "text/testfile",
            "text/testfile",
            None,
            None,
            __TEST_UUID,
            __TEST_UUID,
            10,
            10,
            id="no encoding",
        ),
        pytest.param(
            "/path/to/orig/file",
            "/path/to/orig/file",
            "text/testfile",
            "text/testfile",
            "Shift-JIS",
            "Shift-JIS",
            None,
            None,
            10,
            10,
            id="no UUID",
        ),
        pytest.param(
            "/path/to/orig/file",
            "/path/to/orig/file",
            "text/testfile",
            "text/testfile",
            "Shift-JIS",
            "Shift-JIS",
            __TEST_UUID,
            __TEST_UUID,
            None,
            None,
            id="all arguments specified",
        ),
    ],
)
def test_constructor(
    specified_orig_path: Optional[PathLike],
    expected_orig_path: Optional[PathLike],
    specified_mime_type: Optional[str],
    expected_mime_type: Optional[str],
    specified_encoding: Optional[str],
    expected_encoding: Optional[str],
    specified_value_id: Optional[UUID],
    expected_value_id: Optional[UUID],
    specified_size: Optional[int],
    expected_size: Optional[int],
) -> None:
    """
    Verify that the constructor works correctly.

    Parameters
    ----------
    specified_orig_path the original path to pass to the constructor
    expected_orig_path the expected value for the original_file_name property
    specified_mime_type the mime type to pass to the constructor
    expected_mime_type the expected value for the mime_type property
    specified_encoding the encoding to pass to the constructor
    expected_encoding the expected encoding stored in the file_encoding property
    specified_value_id the UUID to pass to the constructor
    expected_value_id the expected to find in the id property
                     (None causes the test to expect a random UUID).
    specified_size the file size to pass to the constructor
    expected_size the expected file size to find
    """
    # Setup

    # Execute
    sut: _TestFileValue = _TestFileValue(
        specified_orig_path,
        specified_mime_type,
        specified_encoding,
        specified_value_id,
        specified_size,
        test_read_file,
    )

    # Verify
    assert sut.mime_type == expected_mime_type
    assert sut.original_file_name == expected_orig_path
    assert sut.file_encoding == expected_encoding
    assert sut.file_size == expected_size
    if expected_value_id is not None:
        assert sut.id == expected_value_id
    else:
        # Passing None for the expected value ID argument
        # means the test should expect to see a random, nonempty GUID there.
        assert isinstance(sut.id, UUID)
        assert sut.id != __EMPTY_UUID


def test_base_serialization():
    """Verify that the base serialization routine works."""
    # Setup
    sut: _TestFileValue = _TestFileValue(
        "/path/to/orig/file", "text/testfile", "Shift-JIS", __TEST_UUID, 10, test_read_file
    )

    # Execute
    serialized: str = sut.to_api_string(__TestSaveContext())

    # Verify
    loaded: Any = json.loads(serialized)
    assert loaded.get(acvi.FileValue.CONTENTS_KEY) == str(__TEST_UUID)
    assert loaded.get(acvi.FileValue.ORIGINAL_FILENAME_KEY) == "/path/to/orig/file"
    assert loaded.get(acvi.FileValue.MIMETYPE_KEY) == "text/testfile"
    assert loaded.get(acvi.FileValue.ENCODING_KEY) == "Shift-JIS"
    # TODO: Because a dict[str, str] is used, this number gets converted to a string in JSON,
    # which violates JSON best practices. Might want to consider changing the code structure to
    # support int here.
    assert loaded.get(acvi.FileValue.SIZE_KEY) == "10"


def test_empty_file_value():
    """Verifies that EMPTY_FILE works as expected."""

    assert isinstance(acvi.EMPTY_FILE, acvi.FileValue)
    assert acvi.EMPTY_FILE.actual_content_file_name is None
    assert acvi.EMPTY_FILE.mime_type == ""
    assert acvi.EMPTY_FILE.original_file_name is None
    assert acvi.EMPTY_FILE.file_encoding is None
    assert acvi.EMPTY_FILE.id == __EMPTY_UUID


@pytest.mark.parametrize(
    "sut,expected_result",
    [
        pytest.param(acvi.EMPTY_FILE, "<empty file>", id="empty"),
        pytest.param(
            _TestFileValue(
                None, "application/bytestream", None, None, None, None
            ).set_content_override(),
            "<file read from unknown location>",
            id="nonempty, no original path",
        ),
        pytest.param(
            _TestFileValue(
                Path("file_path_here"), "application/bytestream", None, None, None, None
            ).set_content_override(),
            "<file read from file_path_here>",
            id="has content and original path",
        ),
    ],
)
def test_to_display_string(sut: acvi.FileValue, expected_result: str):
    # Execute
    result: str = sut.to_display_string("locale ignored")

    # Verify
    assert result == expected_result


@pytest.mark.parametrize(
    "orig_path,expected_result",
    [
        pytest.param(None, ".tmp", id="None"),
        pytest.param(Path(""), ".tmp", id="empty"),
        pytest.param(Path("no/ext"), ".tmp", id="no extension"),
        pytest.param(Path("has/tmp/extension.tmp"), ".tmp", id="actually .tmp"),
        pytest.param(Path("a/word/document.doc"), ".doc", id=".doc"),
        pytest.param(Path("multiple/dots/in.a.file.name.txt"), ".txt", id="multiple dots"),
        pytest.param(
            Path("last.dot/is/in/a/directory/element"), ".tmp", id="no ext with dot earlier in path"
        ),
        pytest.param(
            Path("longer/extension.longerthanthefilename"),
            ".longerthanthefilename",
            id="long extension",
        ),
    ],
)
def test_get_extension(orig_path: Optional[Path], expected_result: str):
    # Setup
    sut: acvi.FileValue = _TestFileValue(orig_path, None, None, None, None, test_read_file)

    # Execute
    result: str = sut.get_extension()

    # Verify
    assert result == expected_result


@pytest.mark.anyio
@pytest.mark.parametrize(
    "encoding",
    [
        pytest.param(None),
        pytest.param("UTF-8"),
        pytest.param("shift-jis"),
    ],
)
async def test_get_contents(encoding: Optional[str]):
    # Setup
    test_read_file.write_text(test_contents)
    try:
        file = _TestFileValue(None, None, encoding, None, None, test_read_file)

        # SUT
        result: str = await file.get_contents(encoding)

        # Verification
        assert result == test_contents
    finally:
        os.remove(test_read_file)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "encoding",
    [
        pytest.param(None),
        pytest.param("UTF-8"),
        pytest.param("shift-jis"),
    ],
)
async def test_write_file(encoding: Optional[str]):
    # Setup
    test_read_file.write_text(test_contents, encoding)
    out_file = Path("out.file")
    try:
        file = _TestFileValue(None, None, encoding, None, None, test_read_file)

        # SUT
        await file.write_file(out_file)
        result = out_file.read_text(encoding, None)

        # Verification
        assert result == test_contents
    finally:
        os.remove(test_read_file)
        os.remove(out_file)
