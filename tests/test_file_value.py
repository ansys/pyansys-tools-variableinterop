import json
from os import PathLike
from typing import Any, Optional, Union
from uuid import UUID

import pytest

import ansys.common.variableinterop as acvi


class __TestFileValue(acvi.FileValue):
    """A concrete implementation of FileValue used to test its constructor."""

    def actual_content_file_name(self) -> Optional[PathLike]:
        return None

    def get_contents(self, encoding: Optional[Any]) -> str:
        raise NotImplementedError()

    def write_file(self, file_name: PathLike) -> None:
        raise NotImplementedError()

    def _has_content(self) -> bool:
        return bool(self._original_path)


class __TestSaveContext(acvi.ISaveContext):
    def save_file(self, source: Union[PathLike, str], id: Optional[str]) -> str:
        if not id:
            return "file:///" + str(source).lstrip('/')
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


__EMPTY_UUID = UUID(int = 0)
"""Convenience variable for an empty UUID."""


@pytest.mark.parametrize(
    ''.join(('specified_orig_path,expected_orig_path,',
             'specified_mime_type,expected_mime_type,',
             'specified_encoding,expected_encoding,',
             'specified_value_id,expected_value_id')),
    [
        pytest.param('/path/to/orig/file', '/path/to/orig/file',
                     'text/testfile', 'text/testfile',
                     'Shift-JIS', 'Shift-JIS',
                     __TEST_UUID, __TEST_UUID,
                     id="all arguments specified"),
        pytest.param(None, None,
                     'text/testfile', 'text/testfile',
                     'Shift-JIS', 'Shift-JIS',
                     __TEST_UUID, __TEST_UUID,
                     id="no original path"),
        pytest.param('/path/to/orig/file', '/path/to/orig/file',
                     None, '',
                     'Shift-JIS', 'Shift-JIS',
                     __TEST_UUID, __TEST_UUID,
                     id="no mimetype"),
        pytest.param('/path/to/orig/file', '/path/to/orig/file',
                     'text/testfile', 'text/testfile',
                     None, None,
                     __TEST_UUID, __TEST_UUID,
                     id="no encoding"),
        pytest.param('/path/to/orig/file', '/path/to/orig/file',
                     'text/testfile', 'text/testfile',
                     'Shift-JIS', 'Shift-JIS',
                     None, None,
                     id="no UUID"),
    ]
)
def test_constructor(
        specified_orig_path: Optional[str], expected_orig_path: Optional[str],
        specified_mime_type: Optional[str], expected_mime_type: Optional[str],
        specified_encoding: Optional[Any], expected_encoding: Optional[Any],
        specified_value_id: Optional[UUID], expected_value_id: Optional[UUID]) -> None:
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
    """
    # Setup

    # Execute
    sut: __TestFileValue = __TestFileValue(
        specified_orig_path,
        specified_mime_type,
        specified_encoding,
        specified_value_id)

    # Verify
    assert sut.mime_type == expected_mime_type
    assert sut.original_file_name == expected_orig_path
    assert sut.file_encoding == expected_encoding
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
    sut: __TestFileValue = __TestFileValue('/path/to/orig/file',
                                           'text/testfile',
                                           'Shift-JIS',
                                           __TEST_UUID)

    # Execute
    serialized: str = sut.to_api_string(__TestSaveContext())

    # Verify
    loaded: Any = json.loads(serialized)
    assert loaded.get(acvi.FileValue.CONTENTS_KEY) == 'file:///path/to/orig/file'
    assert loaded.get(acvi.FileValue.ORIGINAL_FILENAME_KEY) == '/path/to/orig/file'
    assert loaded.get(acvi.FileValue.MIMETYPE_KEY) == 'text/testfile'
    assert loaded.get(acvi.FileValue.ENCODING_KEY) == 'Shift-JIS'


def test_empty_file_value():
    """Verifies that EMPTY_FILE works as expected."""

    assert isinstance(acvi.EMPTY_FILE, acvi.FileValue)
    assert acvi.EMPTY_FILE.actual_content_file_name is None
    assert acvi.EMPTY_FILE.mime_type == ''
    assert acvi.EMPTY_FILE.original_file_name is None
    assert acvi.EMPTY_FILE.file_encoding is None
    assert acvi.EMPTY_FILE.id == __EMPTY_UUID
