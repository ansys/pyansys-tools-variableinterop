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
"""Defines the ``FileValue`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from configparser import ConfigParser
from contextlib import AbstractAsyncContextManager, AbstractContextManager
import json
from os import PathLike, path
from typing import Callable, Dict, Final, Optional, TypeVar, Union, cast
from uuid import UUID, uuid4

from anyio import Path, open_file
from anyio.streams.file import FileReadStream, FileWriteStream
from overrides import overrides

from .exceptions import _error
from .isave_context import ISaveContext
from .ivariable_visitor import IVariableValueVisitor
from .variable_type import VariableType
from .variable_value import IVariableValue

T = TypeVar("T")

RESOURCE_PARSER = ConfigParser()
RESOURCE_PARSER.read(path.join(path.dirname(__file__), "strings.properties"))


class AsyncLocalFileContentContext(AbstractAsyncContextManager, ABC):
    """
    Represents the context during which a locally available copy of file value content
    should exist.

    This is intended for use with an async implementation.
    """

    @property
    @abstractmethod
    def content_path(self) -> Path:
        """Get the local path to the content."""

    @abstractmethod
    def keep_file_on_exit(self) -> None:
        """Call this method before exiting to prevent deleting the file on exit."""


class LocalFileContentContext(AbstractContextManager, ABC):
    """
    Represents the context during which a locally available copy of file value content
    should exist.

    This is intended for use with a synchronous implementation.
    """

    @property
    @abstractmethod
    def content_path(self) -> Path:
        """Get the local path to the content."""

    @abstractmethod
    def keep_file_on_exit(self) -> None:
        """Call this method before exiting to prevent deleting the file on exit."""


class AlreadyLocalFileContentContext(LocalFileContentContext, AsyncLocalFileContentContext):
    """
    Provides a default local file context for when the file is already hosted locally.

    Because the file is already hosted and managed locally, there is no need to create a
    new copy. Therefore, this implementation basically does nothing but provide a way to
    abstract away the difference between a locally and remotely hosted file content.
    """

    @overrides
    def keep_file_on_exit(self) -> None:
        # Since this implementation does not normally delete the file anyway,
        # nothing needs to be done here.
        pass

    def __init__(self, local_content_path: Optional[Path] = None):
        """
        Initialize a new instance.

        Parameters
        ----------
        local_content_path : Optional[Path], optional
            Path to the local content. The default is ``None``, which indicates that the file
            value is empty.
        """
        self._local_content_path = local_content_path

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context.

        This does nothing as no additional temporary file was created.
        """
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Asynchronously exit the context.

        This does nothing as no additional temporary file was created.
        """
        pass

    @property  # type: ignore
    @overrides
    def content_path(self) -> Optional[PathLike]:
        return self._local_content_path


class FileValue(IVariableValue, ABC):
    """
    Provides an abstract base class for ``FileValue`` implementations.

    To create instances, use the ``FileScope`` class.
    """

    def __init__(
        self,
        original_path: Optional[PathLike] = None,
        mime_type: Optional[str] = None,
        encoding: Optional[str] = None,
        value_id: Optional[UUID] = None,
        file_size: Optional[int] = None,
    ):
        """
        Initialize a new instance.

        Parameters
        ----------
        original_path : Optional[PathLike], optional
            Path to the file to wrap. The default is `None`, which indicates that the original file
            path is not known or does not exist.
        mime_type : Optional[str], optional
            MIME type of the file. The default is `None`, which indicates that the file does
            not have a MIME type.
        encoding : Optional[str], optional
            Encoding of the file. The default is `None`, which indicates that the file does
            not have a text encoding (for example, if it is a binary file).
        value_id : Optional[UUID], optional
            ID that uniquely identifies the file. The default is ``None``, in which case an ID
            is automatically generated.
        file_size : Optional[int], optional
            Size of the file in bytes. The default value is ``None``, which indicates that
            the file size is not known. A file size of ``None`` does not indicate that the file
            is zero bytes.
        """
        self._id: UUID = uuid4() if (value_id is None) else value_id
        self._mime_type: str = "" if (mime_type is None) else mime_type
        self._file_encoding: Optional[str] = encoding
        self._original_path: Optional[PathLike] = original_path
        self._bom: str = ""
        self._size: Optional[int] = file_size

    @overrides
    def __eq__(self, other):
        return isinstance(other, FileValue) and self._id == other._id

    @overrides
    def __hash__(self):
        return hash(self._id)

    @overrides
    def accept(self, visitor: IVariableValueVisitor[T]) -> T:
        return visitor.visit_file(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.FILE

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        if self._has_content():
            return RESOURCE_PARSER.get("DisplayFormats", "FILE_CONTENTS_FORMAT").format(
                self._original_path
                if self._original_path
                else RESOURCE_PARSER.get("DisplayFormats", "FILE_LOCATION_UNKNOWN")
            )
        else:
            return RESOURCE_PARSER.get("DisplayFormats", "FILE_EMPTY")

    BINARY_MIMETYPE: Final[str] = "application/octet-stream"

    TEXT_MIMETYPE: Final[str] = "text/plain"

    ORIGINAL_FILENAME_KEY: Final[str] = "originalFilename"
    """JSON key for API serialization representing the original file name."""

    MIMETYPE_KEY: Final[str] = "mimeType"

    ENCODING_KEY: Final[str] = "encoding"

    CONTENTS_KEY: Final[str] = "contents"

    SIZE_KEY: Final[str] = "size"

    _DEFAULT_EXT = ".tmp"

    @property
    def mime_type(self) -> str:
        """MIME type of the file."""
        return self._mime_type

    @property
    def original_file_name(self) -> Optional[PathLike]:
        """Name of the original file that was wrapped."""
        return self._original_path

    @property
    def extension(self) -> str:
        """Extension of the file."""
        # TODO: Implement
        raise NotImplementedError()

    @property
    def file_encoding(self) -> Optional[str]:
        """Encoding of the file."""
        return self._file_encoding

    @property
    def id(self) -> UUID:
        """
        ID of the file.

        Returns
        -------
        UUID
            ID that identifies the file.
        """
        return self._id

    @property
    def file_size(self) -> Optional[int]:
        """
        Size of the file in bytes if known.

        A value of ``None`` indicates that the file size is not known,
        not that the file size is zero bytes.
        """
        return self._size

    @staticmethod
    def read_bom(filename: str) -> str:
        """
        Open a file for reading and detect a byte order mark at the beginning.

        Parameters
        ----------
        filename : str
            File to read.

        Returns
        -------
        str
            If the file contains a BOM, an appropriate encoding is returned.
            If the file does not contain a BOM, ``None`` is returned.
        """
        with open(filename, "rb") as f:
            bom = f.read(4)
            if bom == b"\x00\x00\xfe\xff":
                return "UTF-32 BE"
            elif bom == b"\xff\xfe\x00\x00":
                return "UTF-32 LE"
            elif bom[0:3] == b"\xef\xbb\xbf":
                return "UTF-8"
            elif bom[0:2] == b"\xff\xfe":
                return "UTF-16 LE"
            elif bom[0:2] == b"\xfe\xff":
                return "UTF-16 BE"
            else:
                return "None"

    async def write_file(self, file_name: PathLike) -> None:
        """
        Write the file's contents to a new file.

        Parameters
        ----------
        file_name : PathLike
            Path to the file to create.

        Returns
        -------
        None
        """
        # make the file
        Path(file_name).open("w").close()

        # copy the contents from the actual content file
        async with await self.get_reference_to_actual_content_file_async() as local_pin:
            file: Optional[PathLike] = local_pin.content_path
            async with await FileReadStream.from_path(file) as in_stream:
                async with await FileWriteStream.from_path(file_name) as out_stream:
                    async for chunk in in_stream:
                        await out_stream.send(chunk)

    @abstractmethod
    async def get_reference_to_actual_content_file_async(
        self, progress_callback: Optional[Callable[[int], None]] = None
    ) -> AsyncLocalFileContentContext:
        """
        Realize the file contents to a local filesystem if needed.

        The ``FileValue`` instance is intended to represent an immutable value. The file
        returned by this call may point to a cached file or even the original file. Callers
        must not modify the file on disk. Otherwise, undefined behaviors, including class 3 errors,
        may occur. If the caller needs to modify the file, consider using the ``write_file``
        method or copying the file before modifying it.

        Parameters
        ----------
        progress_callback : Optional[Callable[[int], None]], optional
            Callback that can be called to indicate progress in realizing the local copy.
            The default is ``None``, in which case this method makes no attempt
            to report its progress. This method may call a provided callback with a
            percentage value between 0 and 100 inclusive. The provided callback may not
            necessarily be called at all, and calls for 0 or 100 percent are not guaranteed,
            even if other calls occur.

        Returns
        -------
        AsyncLocalFileContentContext
            Context manager that, when exited, deletes the local copy
            if it is a temporary file.
        """

    @abstractmethod
    def get_reference_to_actual_content_file(
        self, progress_callback: Optional[Callable[[int], None]] = None
    ) -> LocalFileContentContext:
        """
        Realizes the file contents to a local filesystem if needed.

        The ``FileValue`` instance is intended to represent an immutable value. The file
        returned by this call may point to a cached file or even the original file. Callers
        must not modify the file on disk. Otherwise, undefined behaviors, including class 3 errors,
        may occur. If the caller needs to modify the file, consider using the ``write_file``
        method or copying the file before modifying it.

        Parameters
        ----------
        progress_callback : Optional[Callable[[int], None]], optional
            Callback that can be called to indicate progress in realizing the local copy.
            The default is ``None``, in which case this method makes no attempt
            to report its progress. This method may call a provided callback with a
            percentage value between 0 and 100 inclusive. The provided callback may not
            necessarily be called at all, and calls for 0 or 100 percent are not guaranteed,
            even if other calls occur.

        Returns
        -------
        LocalFileContentContext
            Context manager that, when exited, deletes the local copy
            if it is a temporary file.
        """

    @classmethod
    def is_text_based_static(cls, mimetype: str) -> Optional[bool]:
        """
        Determines if a file is text-based via its MIME type.

        Parameters
        ----------
        mimetype : str
            File's MIME type.

        Returns
        -------
        Optional[bool]
            ``True`` if the MIME type starts with text or is an application (JSON),
            ``False`` otherwise.
        """
        return str(mimetype).startswith("text/") or str(mimetype).startswith("application/json")

    @property
    def is_text_based(self) -> Optional[bool]:
        """
        Flag indicating if this file is text-based via its MIME type.

        Returns
        -------
        bool
            ``True`` if the MIME type starts with ``text`` or is ``application/json``,
            ``False`` otherwise.
        """
        return FileValue.is_text_based_static(self.mime_type)

    async def get_contents(self, encoding: Optional[str] = None) -> str:
        """
        Read the contents of the file as a string.

        Parameters
        ----------
        encoding : Optional[str], optional
            Encoding to use when reading. The default is ``None``, in which case the
            current locale's encoding is used.

        Returns
        -------
        str
            Contents of the file as a string.
        """
        async with await self.get_reference_to_actual_content_file_async() as local_pin:
            file: Optional[PathLike] = local_pin.content_path
            async with await open_file(file=file, encoding=encoding) as f:
                contents = await f.read()
                return contents

    @abstractmethod
    def _has_content(self) -> bool:
        """
        Check whether this file has content.

        You use this method to decide whether to pass the content of the file to the file store.

        Returns
        -------
        bool
            ``True`` if there is content, ``False`` otherwise.
        """

    @overrides
    def to_api_string(self, context: Optional[ISaveContext] = None) -> str:
        """
        Convert the value to an API string using a save context.

        Parameters
        ----------
        context : Optional[ISaveContext], optional
            Save context to use. The default value is ``None``,
            in which case file values are not supported.

        Returns
        -------
        str
            String appropriate for use in files and APIs.
        """
        if context is None:
            raise ValueError(_error("ERROR_FILE_NO_CONTEXT"))
        api_obj: Dict[str, Optional[str]] = self.to_api_object(cast(ISaveContext, context))
        return json.dumps(api_obj)

    def _send_actual_file(self, save_context: ISaveContext) -> str:
        name: Union[PathLike, str] = ""
        with self.get_reference_to_actual_content_file() as local_pin:
            if local_pin.content_path is not None:
                name = cast(PathLike, local_pin)
            return save_context.save_file(name, str(self.id))

    def to_api_object(self, save_context: ISaveContext) -> Dict[str, Optional[str]]:
        """
        Convert this file to an API object.

        Parameters
        ----------
        save_context : ISaveContext
            Save context to use for the conversion.

        Returns
        -------
        Dict[str, Optional[str]]
            API object that matches this ``FileValue`` instance.
        """
        obj: Dict[str, Optional[str]] = {}
        if self._has_content():
            content_marker: str = self._send_actual_file(save_context)
            obj[FileValue.CONTENTS_KEY] = content_marker

        if self._original_path:
            obj[FileValue.ORIGINAL_FILENAME_KEY] = str(self._original_path)
        if self._mime_type:
            obj[FileValue.MIMETYPE_KEY] = self._mime_type
        if self._file_encoding:
            obj[FileValue.ENCODING_KEY] = self._file_encoding
        if not (self._size is None):
            obj[FileValue.SIZE_KEY] = str(self._size)
        return obj

    # TODO: Async get_contents

    def get_extension(self) -> str:
        """
        Get the file extension of the file, including the period.

        If the file extension is not known, ``.tmp`` is returned.

        Returns
        -------
        str
            File extension of the file if known, ``".tmp"`` otherwise.
        """
        ext: str = FileValue._DEFAULT_EXT
        if isinstance(self._original_path, PathLike):
            orig_path, split_ext = path.splitext(self._original_path)
            if split_ext:
                ext = split_ext
        return ext


class LocalFileValue(FileValue, ABC):
    """
    Base class for file values where the file contents already exist on the local disk.

    Generally speaking, clients of this library should not attempt to use this class. It
    is intended for dependents of this library who are attempting to implement a new
    ``FileScope`` instance that always stores the content of a file on the local disk.
    Clients are discouraged from attempting to introspect a ``FileValues``instance to
    determine if they are instances of ``LocalFileValue`` for the purpose of getting a path to the
    locally stored content. Instead, always correctly use the
    ``get_reference_to_actual_content_file`` method for the ``FileValue`` instance to
    allow the code in question to get the local path, even for files that are not
    originally hosted locally. For files that are originally hosted locally, this
    does not produce an additional copy but rather gives a context manager that does
    nothing on enter or exit but still allows access to the actual content path.
    """

    def __init__(
        self,
        original_path: Optional[PathLike] = None,
        mime_type: Optional[str] = None,
        encoding: Optional[str] = None,
        value_id: Optional[UUID] = None,
        file_size: Optional[int] = None,
        actual_content_file_name: Optional[PathLike] = None,
    ):
        """
        Initialize a new instance.

        Parameters
        ----------
        original_path : Optional[PathLike], optional
            Path to the file to wrap. The default is `None`, which indicates that the original file
            path is not known or does not exist.
        mime_type : Optional[str], optional
            MIME type of the file. The default is `None`, which indicates that the file does
            not have a MIME type.
        encoding : Optional[str], optional
            Encoding of the file. The default is `None`, which indicates that the file does
            not have a text encoding (for example, if it is a binary file).
        value_id : Optional[UUID], optional
            ID that uniquely identifies the file. The default is ``None``, in which case an ID
            is automatically generated.
        file_size : Optional[int], optional
            Size of the file in bytes. The default value is `None`, which indicates that
            the file size is not known. A size of `None` does not indicate that the file
            is zero bytes.
        """
        super().__init__(
            original_path=original_path,
            encoding=encoding,
            value_id=value_id,
            mime_type=mime_type,
            file_size=file_size,
        )
        self.__actual_content_file_name = actual_content_file_name

    @property
    def actual_content_file_name(self) -> Optional[PathLike]:
        """
        Get the path to the file that this ``FileValue`` instance wraps.

        Returns
        -------
        Optional[PathLike]
            PathLike to the file.
        """
        return self.__actual_content_file_name

    @overrides
    async def get_reference_to_actual_content_file_async(
        self, progress_callback: Optional[Callable[[int], None]] = None
    ) -> AsyncLocalFileContentContext:
        return AlreadyLocalFileContentContext(self.actual_content_file_name)

    @overrides
    def get_reference_to_actual_content_file(
        self, progress_callback: Optional[Callable[[int], None]] = None
    ) -> LocalFileContentContext:
        return AlreadyLocalFileContentContext(self.actual_content_file_name)


class EmptyFileValue(LocalFileValue):
    """
    Represents an empty file value.

    Generally speaking, you should not create an instance of this class but instead use
    ``ansys.tools.variableinterop.EMPTY_FILE``.
    """

    def __init__(self):
        """
        Construct a new instance.

        Generally speaking you should not create an instance of this class but instead
        use ansys.tools.variableinterop.EMPTY_FILE.
        """
        super().__init__(None, None, None, UUID(int=0), None, None)

    @overrides
    def _has_content(self) -> bool:
        return False

    @property  # type: ignore
    @overrides
    def actual_content_file_name(self) -> Optional[PathLike]:
        return None

    @overrides
    async def write_file(self, file_name: PathLike) -> None:
        # TODO: Research correct exception to throw
        raise NotImplementedError()

    @overrides
    async def get_contents(self, encoding: Optional[str]) -> str:
        # TODO: Research correct exception to throw
        raise NotImplementedError()


EMPTY_FILE = EmptyFileValue()
