from __future__ import annotations

from os import PathLike
from typing import Any, Optional
from uuid import uuid4

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

        # TODO: Make consistent for mime_type and encoding w/r/t Optional

        def __init__(
            self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[Any]
        ) -> None:
            super().__init__(to_read, mime_type, encoding, uuid4())

        @property
        def actual_content_file_name(self) -> Optional[PathLike]:
            return self._original_path

        def write_file(self, file_name: PathLike) -> None:
            # TODO: Implement
            raise NotImplementedError()

        def get_contents(self, encoding: Optional[Any]) -> str:
            # TODO: Implement
            raise NotImplementedError()

    def read_from_file(
        self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[Any]
    ) -> file_value.FileValue:
        return NonManagingFileScope(to_read, mime_type, encoding)
