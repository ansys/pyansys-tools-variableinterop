import json
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import UUID

import pytest

import ansys.tools.variableinterop as acvi

__EMPTY_UUID = UUID(int=0)
"""Convenience variable for an empty UUID."""


@pytest.mark.parametrize(
    "to_read,mime_type,encoding,expected_mime_type",
    [
        pytest.param(Path("file/to/read"), "text/testfile", "Shift-JIS", "text/testfile", id="All"),
        pytest.param(Path("file/to/read"), None, "Shift-JIS", "", id="No mimetype"),
        pytest.param(
            Path("file/to/read"),
            "application/bytestream",
            None,
            "application/bytestream",
            id="No encoding",
        ),
    ],
)
def test_read_from_file(
    to_read: PathLike, mime_type: Optional[str], encoding: Optional[Any], expected_mime_type: str
):
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
    "to_read,mime_type,encoding,expected_json_value",
    [
        pytest.param(
            "file/to/read",
            "text/testfile",
            "Shift-JIS",
            {
                acvi.FileValue.CONTENTS_KEY: "file/to/read",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "file/to/read",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
                acvi.FileValue.MIMETYPE_KEY: "text/testfile",
            },
            id="All",
        ),
        pytest.param(
            "file/to/read",
            None,
            "Shift-JIS",
            {
                acvi.FileValue.CONTENTS_KEY: "file/to/read",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "file/to/read",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
            },
            id="No mimetype",
        ),
        pytest.param(
            "file/to/read",
            "application/bytestream",
            None,
            {
                acvi.FileValue.CONTENTS_KEY: "file/to/read",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "file/to/read",
                acvi.FileValue.MIMETYPE_KEY: "application/bytestream",
            },
            id="No encoding",
        ),
    ],
)
def test_to_api_str(
    to_read: str,
    mime_type: Optional[str],
    encoding: Optional[Any],
    expected_json_value: Dict[str, Optional[str]],
) -> None:
    # Setup
    with acvi.NonManagingFileScope() as sut_scope:
        sut_file_inst: acvi.FileValue = sut_scope.read_from_file(to_read, mime_type, encoding)

        # Execute
        result: str = acvi.to_api_string(sut_file_inst, sut_scope)

        # Verify
        assert expected_json_value == json.loads(result)


@pytest.mark.parametrize(
    "source,expected_file_name,expected_mime_type,expected_encoding",
    [
        pytest.param(
            '{"contents":"/file/to/read","originalFileName":"/file/to/read",'
            '"mimeType":"text/testfile","encoding":"Shift-JIS"}',
            Path("/file/to/read"),
            "text/testfile",
            "Shift-JIS",
            id="All present",
        ),
        pytest.param(
            '{"originalFileName":"/file/to/read","contents":"/file/to/read",'
            '"encoding":"Shift-JIS"}',
            Path("/file/to/read"),
            "",
            "Shift-JIS",
            id="Missing mimetype",
        ),
        pytest.param(
            '{"contents":"/file/to/read","originalFileName":"/file/to/read",'
            '"mimeType":"application/bytestream"}',
            Path("/file/to/read"),
            "application/bytestream",
            None,
            id="No encoding",
        ),
    ],
)
def test_from_api_str_valid(
    source: str,
    expected_file_name: PathLike,
    expected_mime_type: str,
    expected_encoding: Optional[Any],
) -> None:

    # Setup
    with acvi.NonManagingFileScope() as sut_scope:

        # Execute
        sut_file_inst: acvi.FileValue = acvi.from_api_string(
            acvi.VariableType.FILE, source, sut_scope, sut_scope
        )

        # Verify
        assert isinstance(sut_file_inst, acvi.FileValue)
        assert sut_file_inst.original_file_name == expected_file_name
        assert sut_file_inst.actual_content_file_name == expected_file_name
        assert sut_file_inst.mime_type == expected_mime_type
        assert sut_file_inst.file_encoding == expected_encoding


def test_array_to_api_str():

    # Setup
    with acvi.NonManagingFileScope() as sut_scope:
        sut_values: acvi.FileArrayValue = acvi.FileArrayValue(
            values=[
                acvi.EMPTY_FILE,
                sut_scope.read_from_file("test/files/test.txt", "text/testfile", "Shift-JIS"),
                sut_scope.read_from_file("test/files/test-jis.txt", None, "Shift-JIS"),
                sut_scope.read_from_file(
                    "test/files/test-item.bin", "application/bytestream", None
                ),
            ]
        )

        # Execute
        result: str = acvi.to_api_string(sut_values, sut_scope)

        # Verify
        json_parsed_result = json.loads(result)
        expected_json_value = [
            {},
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test.txt",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test.txt",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
                acvi.FileValue.MIMETYPE_KEY: "text/testfile",
            },
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test-jis.txt",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-jis.txt",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
            },
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test-item.bin",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-item.bin",
                acvi.FileValue.MIMETYPE_KEY: "application/bytestream",
            },
        ]
        assert json_parsed_result == expected_json_value


def test_array_to_api_str_2d():

    # TODO: This test does not test the size parameter because the files tested
    # do not really exist.

    # Setup
    with acvi.NonManagingFileScope() as sut_scope:
        sut_values: acvi.FileArrayValue = acvi.FileArrayValue(
            values=[
                [
                    acvi.EMPTY_FILE,
                    sut_scope.read_from_file("test/files/test.txt", "text/testfile", "Shift-JIS"),
                ],
                [
                    sut_scope.read_from_file("test/files/test-jis.txt", None, "Shift-JIS"),
                    sut_scope.read_from_file(
                        "test/files/test-item.bin", "application/bytestream", None
                    ),
                ],
            ]
        )

        # Execute
        result: str = acvi.to_api_string(sut_values, sut_scope)

        # Verify
        json_parsed_result = json.loads(result)
        expected_json_value = [
            [
                {},
                {
                    acvi.FileValue.CONTENTS_KEY: "test/files/test.txt",
                    acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test.txt",
                    acvi.FileValue.ENCODING_KEY: "Shift-JIS",
                    acvi.FileValue.MIMETYPE_KEY: "text/testfile",
                },
            ],
            [
                {
                    acvi.FileValue.CONTENTS_KEY: "test/files/test-jis.txt",
                    acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-jis.txt",
                    acvi.FileValue.ENCODING_KEY: "Shift-JIS",
                },
                {
                    acvi.FileValue.CONTENTS_KEY: "test/files/test-item.bin",
                    acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-item.bin",
                    acvi.FileValue.MIMETYPE_KEY: "application/bytestream",
                },
            ],
        ]
        assert json_parsed_result == expected_json_value


def test_array_from_string():
    expected_json_value = [
        {},
        {
            acvi.FileValue.CONTENTS_KEY: "test/files/test.txt",
            acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test.txt",
            acvi.FileValue.ENCODING_KEY: "Shift-JIS",
            acvi.FileValue.MIMETYPE_KEY: "text/testfile",
        },
        {
            acvi.FileValue.CONTENTS_KEY: "test/files/test-jis.txt",
            acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-jis.txt",
            acvi.FileValue.ENCODING_KEY: "Shift-JIS",
        },
        {
            acvi.FileValue.CONTENTS_KEY: "test/files/test-item.bin",
            acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-item.bin",
            acvi.FileValue.MIMETYPE_KEY: "application/bytestream",
        },
    ]

    with acvi.NonManagingFileScope() as sut_scope:
        result = acvi.from_api_string(
            acvi.VariableType.FILE_ARRAY, json.dumps(expected_json_value), sut_scope, sut_scope
        )
        assert isinstance(result, acvi.FileArrayValue)
        assert result[0] is acvi.EMPTY_FILE
        assert result[1].original_file_name == Path("test/files/test.txt")
        assert result[2].original_file_name == Path("test/files/test-jis.txt")
        assert result[3].original_file_name == Path("test/files/test-item.bin")


def test_array_from_string_2d():
    expected_json_value = [
        [
            {},
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test.txt",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test.txt",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
                acvi.FileValue.MIMETYPE_KEY: "text/testfile",
            },
        ],
        [
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test-jis.txt",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-jis.txt",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
            },
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test-item.bin",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-item.bin",
                acvi.FileValue.MIMETYPE_KEY: "application/bytestream",
            },
        ],
    ]

    with acvi.NonManagingFileScope() as sut_scope:
        result = acvi.from_api_string(
            acvi.VariableType.FILE_ARRAY, json.dumps(expected_json_value), sut_scope, sut_scope
        )
        assert result[0, 0] is acvi.EMPTY_FILE
        assert result[0, 1].original_file_name == Path("test/files/test.txt")
        assert result[1, 0].original_file_name == Path("test/files/test-jis.txt")
        assert result[1, 1].original_file_name == Path("test/files/test-item.bin")


def test_array_from_string_jagged():
    expected_json_value = [
        [
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test.txt",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test.txt",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
                acvi.FileValue.MIMETYPE_KEY: "text/testfile",
            }
        ],
        [
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test-jis.txt",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-jis.txt",
                acvi.FileValue.ENCODING_KEY: "Shift-JIS",
            },
            {
                acvi.FileValue.CONTENTS_KEY: "test/files/test-item.bin",
                acvi.FileValue.ORIGINAL_FILENAME_KEY: "test/files/test-item.bin",
                acvi.FileValue.MIMETYPE_KEY: "application/bytestream",
            },
        ],
    ]

    try:
        with acvi.NonManagingFileScope() as sut_scope:
            result = acvi.from_api_string(
                acvi.VariableType.FILE_ARRAY, json.dumps(expected_json_value), sut_scope, sut_scope
            )
            assert False, "Should have failed by now."

    except TypeError as thrown:
        assert (
            str(thrown) == f"Encountered a {list} when attempting to deserialize "
            f"a file value element. Is the serialized array rectangular?"
        )
