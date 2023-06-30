"""Definition of NonManagingFileScope."""
from __future__ import annotations

import os
from os import PathLike
from pathlib import Path
from typing import Dict, Optional, Union, cast
from uuid import uuid4

from overrides import overrides

from .file_scope import FileScope
from .file_value import EMPTY_FILE, FileValue, LocalFileValue
from .isave_context import ILoadContext, ISaveContext


class NonManagingFileScope(FileScope, ISaveContext, ILoadContext):
    """
    A simple file scope implementation that performs no management.

    This file scope that allows you to create `FileValue` instances that are backed by arbitrary
    preexisting files on disk. It is up to the caller to ensure that the file remains in place
    and unchanged for the lifespan of the FileValue instance, and that the file is deleted at
    an appropriate time. Because of these restrictions, it is generally not recommended using
    this file scope except for referencing permanently installed files.

    It also serves as a "pass-through" save context; since the files are assumed to be managed
    externally such that they are permanent or at least not deleted while in use,
    the save context takes no action to actually save them and simply passes through
    their current location on disk as an identifier.
    """

    class NonManagingFileValue(LocalFileValue):
        """Implementation of FileValue used by this scope."""

        @overrides
        def _has_content(self) -> bool:
            return bool(self._original_path)

        def __init__(
            self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]
        ) -> None:
            """
            Construct a new NonManagingFileValue.

            Parameters
            ----------
            original_path Path to the file to wrap.
            mime_type Mime type of the file.
            encoding The encoding of the file.
            value_id The id that uniquely identifies this file. Auto-generated\
                if not supplied.
            """
            size: Optional[int] = None
            # TODO: The tests use a lot of non-existent files, so this prevents
            # it from crashing in those cases. This may not be what we want in an API
            # though? Probably would be better to not let you create a FileValue to a
            # non-existent file?
            if os.path.isfile(to_read):
                st = os.stat(to_read)
                size = st.st_size
            super().__init__(
                original_path=to_read,
                mime_type=mime_type,
                encoding=encoding,
                value_id=uuid4(),
                file_size=size,
                actual_content_file_name=to_read,
            )

        @overrides
        def _send_actual_file(self, save_context: ISaveContext) -> str:
            return save_context.save_file(str(self.actual_content_file_name), None)

    @overrides
    def read_from_file(
        self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]
    ) -> FileValue:
        return NonManagingFileScope.NonManagingFileValue(to_read, mime_type, encoding)

    def to_api_string_file_store(self, file_var: FileValue) -> str:
        """
        TODO.

        Parameters
        ----------
        file_var TODO

        Returns
        -------
        TODO
        """
        if not issubclass(type(file_var), NonManagingFileScope.NonManagingFileValue):
            raise TypeError("This file scope cannot serialize file values it did not create.")

        # Just return the file name.
        typed_file_var = cast(NonManagingFileScope.NonManagingFileValue, file_var)
        if typed_file_var.actual_content_file_name is None:
            return ""
        return str(typed_file_var.actual_content_file_name)

    @overrides
    def from_api_object(
        self, api_object: Dict[str, Optional[str]], load_context: ILoadContext
    ) -> FileValue:
        if FileValue.CONTENTS_KEY in api_object:
            content: Optional[PathLike] = load_context.load_file(
                api_object.get(FileValue.CONTENTS_KEY)
            )
            if content is not None:
                return NonManagingFileScope.NonManagingFileValue(
                    content,
                    api_object.get(FileValue.MIMETYPE_KEY),
                    api_object.get(FileValue.ENCODING_KEY),
                )
            else:
                return EMPTY_FILE
        else:
            return EMPTY_FILE

    @overrides
    def save_file(self, source: Union[PathLike, str], content_id: Optional[str]) -> str:
        if content_id is not None:
            return content_id

        else:
            return str(source)

    @overrides
    def load_file(self, content_id: Optional[str]) -> Optional[PathLike]:
        if content_id:
            return Path(content_id)
        else:
            return None

    @overrides
    def flush(self) -> None:
        pass

    @overrides
    def close(self) -> None:
        pass
