import ansys.common.variableinterop as acvi
from os import PathLike
import pytest
from typing import Any, Optional
from uuid import UUID


class __TestFileValue(acvi.FileValue):
    """A concrete implementation of FileValue used to test its constructor."""

    def actual_content_file_name(self) -> Optional[PathLike]:
        return None

    def get_contents(self, encoding: Optional[Any]) -> str:
        raise NotImplementedError()

    def write_file(self, file_name: PathLike) -> None:
        raise NotImplementedError()


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


def test_empty_file_value():
    """Verifies that EMPTY_FILE works as expected."""

    assert isinstance(acvi.EMPTY_FILE, acvi.FileValue)
    assert acvi.EMPTY_FILE.actual_content_file_name is None
    assert acvi.EMPTY_FILE.mime_type == ''
    assert acvi.EMPTY_FILE.original_file_name is None
    assert acvi.EMPTY_FILE.file_encoding is None
    assert acvi.EMPTY_FILE.id == __EMPTY_UUID
