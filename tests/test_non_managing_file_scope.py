import json
from os import PathLike
from typing import Any, Dict, Optional
from uuid import UUID

import pytest

import ansys.common.variableinterop as acvi

__EMPTY_UUID = UUID(int = 0)
"""Convenience variable for an empty UUID."""


@pytest.mark.parametrize(
    'to_read,mime_type,encoding,expected_mime_type',
    [
        pytest.param('file/to/read', 'text/testfile', 'Shift-JIS', 'text/testfile',
                     id="All"),
        pytest.param('file/to/read', None, 'Shift-JIS', '',
                     id="No mimetype"),
        pytest.param('file/to/read', 'application/bytestream', None, 'application/bytestream',
                     id="No encoding")
    ]
)
def test_read_from_file(to_read: PathLike, mime_type: Optional[str], encoding: Optional[Any],
                        expected_mime_type: str):
    # Setup
    sut: acvi.NonManagingFileScope = acvi.NonManagingFileScope()

    # Execute
    result: acvi.FileValue = sut.read_from_file(to_read, mime_type, encoding)

    # Verify
    assert isinstance(result, acvi.FileValue)
    assert result.original_file_name == to_read
    assert result.actual_content_file_name == to_read
    assert result.mime_type == expected_mime_type
    assert result.file_encoding == encoding


@pytest.mark.parametrize(
    'to_read,mime_type,encoding,expected_json_value',
    [
        pytest.param('file/to/read', 'text/testfile', 'Shift-JIS',
                     {
                         acvi.FileValue.CONTENTS_KEY: 'file/to/read',
                         acvi.FileValue.ORIGINAL_FILENAME_KEY: 'file/to/read',
                         acvi.FileValue.ENCODING_KEY: 'Shift-JIS',
                         acvi.FileValue.MIMETYPE_KEY: 'text/testfile'
                     },
                     id="All"),
        pytest.param('file/to/read', None, 'Shift-JIS',
                     {
                         acvi.FileValue.CONTENTS_KEY: 'file/to/read',
                         acvi.FileValue.ORIGINAL_FILENAME_KEY: 'file/to/read',
                         acvi.FileValue.ENCODING_KEY: 'Shift-JIS',
                     },
                     id="No mimetype"),
        pytest.param('file/to/read', 'application/bytestream', None,
                     {
                         acvi.FileValue.CONTENTS_KEY: 'file/to/read',
                         acvi.FileValue.ORIGINAL_FILENAME_KEY: 'file/to/read',
                         acvi.FileValue.MIMETYPE_KEY: 'application/bytestream'
                     },
                     id="No encoding")
    ]
)
def test_to_api_str(to_read: str, mime_type: Optional[str], encoding: Optional[Any],
                    expected_json_value: Dict[str, Optional[str]]) -> None:
    # Setup
    with acvi.NonManagingFileScope() as sut_scope:
        sut_file_inst: acvi.FileValue = sut_scope.read_from_file(to_read, mime_type, encoding)

        # Execute
        result: str = acvi.to_api_string(sut_file_inst, sut_scope)

        # Verify
        assert expected_json_value == json.loads(result)


@pytest.mark.parametrize(
    'source,expected_file_name,expected_mime_type,expected_encoding',
    [
        pytest.param('{"contents":"/file/to/read","originalFileName":"/file/to/read",'
                     '"mimeType":"text/testfile","encoding":"Shift-JIS"}',
                     '/file/to/read', 'text/testfile', 'Shift-JIS', id="All present"),
        pytest.param('{"originalFileName":"/file/to/read","contents":"/file/to/read",'
                     '"encoding":"Shift-JIS"}',
                     '/file/to/read', '', 'Shift-JIS', id="Missing mimetype"),
        pytest.param('{"contents":"/file/to/read","originalFileName":"/file/to/read",'
                     '"mimeType":"application/bytestream"}',
                     '/file/to/read', 'application/bytestream', None, id="No encoding"),
    ]
)
def test_from_api_str_valid(source: str,
                            expected_file_name: PathLike,
                            expected_mime_type: str,
                            expected_encoding: Optional[Any]) -> None:

    # Setup
    with acvi.NonManagingFileScope() as sut_scope:

        # Execute
        sut_file_inst: acvi.FileValue = acvi.from_api_string(
            acvi.VariableType.FILE, source, sut_scope)  # type:ignore

        # Verify
        assert isinstance(sut_file_inst, acvi.FileValue)
        assert sut_file_inst.original_file_name == expected_file_name
        assert sut_file_inst.actual_content_file_name == expected_file_name
        assert sut_file_inst.mime_type == expected_mime_type
        assert sut_file_inst.file_encoding == expected_encoding
