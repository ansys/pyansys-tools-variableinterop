from __future__ import annotations

from os import PathLike
from typing import Any, Optional
from uuid import UUID, uuid4

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
            self._id: UUID = uuid4()
            self._path: PathLike = to_read
            self._mime_type: str = "" if (mime_type is None) else mime_type
            self._file_encoding: Any = encoding

        @property
        def actual_content_file_name(self) -> Optional[PathLike]:
            return self._path

        @property
        def mime_type(self) -> str:
            return self.mime_type

        @property
        def original_file_name(self) -> Optional[PathLike]:
            return self._path

        @property
        def file_encoding(self) -> Any:
            return self._file_encoding

        @property
        def id(self) -> UUID:
            return self._id

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
