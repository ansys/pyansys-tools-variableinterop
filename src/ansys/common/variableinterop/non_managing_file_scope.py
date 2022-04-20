from __future__ import annotations

from os import PathLike
from typing import Any, Dict, Optional
from uuid import uuid4

from overrides import overrides

import ansys.common.variableinterop.file_scope as file_scope
import ansys.common.variableinterop.file_value as file_value


class NonManagingFileScope(file_scope.FileScope):
    """
    A file scope that allows you to create `FileValue` instances that are backed by arbitrary
    preexisting files on disk. It is up to the caller to ensure that the file remains in place
    and unchanged for the lifespan of the FileValue instance, and that the file is deleted at
    an appropriate time. Because of these restrictions, it is generally not recommended using
    this file scope except for referencing permanently installed files.
    """

    def close(self) -> None:
        pass

    class NonManagingFileValue(file_value.FileValue):

        def _has_content(self) -> bool:
            return bool(self._original_path)

        # TODO: Make consistent for mime_type and encoding w/r/t Optional

        def __init__(
            self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]
        ) -> None:
            super().__init__(to_read, mime_type, encoding, uuid4())

        @property
        def actual_content_file_name(self) -> Optional[PathLike]:
            return self._original_path

        def write_file(self, file_name: PathLike) -> None:
            # TODO: Implement
            raise NotImplementedError()

        def get_contents(self, encoding: Optional[str]) -> str:
            # TODO: Implement
            raise NotImplementedError()

    def read_from_file(
        self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]
    ) -> file_value.FileValue:
        return NonManagingFileScope.NonManagingFileValue(to_read, mime_type, encoding)

    def to_api_string_file_store(self,
                                 file_var: file_value.FileValue) -> str:
        if not issubclass(type(file_var), NonManagingFileScope.NonManagingFileValue):
            raise TypeError("This file scope cannot serialize file values it did not create.")

        # Just return the file name.
        return file_var.actual_content_file_name

    @overrides
    def from_api_object(self, api_object: Dict[str, Optional[str]]) -> file_value.FileValue:
        if file_value.FileValue.CONTENTS_KEY in api_object:
            return NonManagingFileScope.NonManagingFileValue(
                api_object.get(file_value.FileValue.CONTENTS_KEY),
                api_object.get(file_value.FileValue.MIMETYPE_KEY),
                api_object.get(file_value.FileValue.ENCODING_KEY))
        else:
            return file_value.EMPTY_FILE_VALUE