"""Definition of FileValue."""
from __future__ import annotations

from abc import ABC, abstractmethod
from configparser import ConfigParser
import json
from os import PathLike, path
from typing import Dict, Final, Optional, TypeVar
from uuid import UUID, uuid4

from anyio import Path, open_file
from anyio.streams.file import FileReadStream, FileWriteStream
from overrides import overrides

import ansys.common.variableinterop.isave_context as isave_context
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar('T')

RESOURCE_PARSER = ConfigParser()
RESOURCE_PARSER.read(path.join(path.dirname(__file__), "strings.properties"))


class FileValue(variable_value.IVariableValue, ABC):
    """Abstract base class for a file variable. To create instances, \
    use a `FileScope`."""

    def __init__(self,
                 original_path: Optional[PathLike],
                 mime_type: Optional[str],
                 encoding: Optional[str],
                 value_id: Optional[UUID]):
        """
        Construct a new FileValue.

        Parameters
        ----------
        original_path Path to the file to wrap.
        mime_type Mime type of the file.
        encoding The encoding of the file.
        value_id The id that uniquely identifies this file. Auto-generated\
            if not supplied.
        """
        self._id: UUID = uuid4() if (value_id is None) else value_id
        self._mime_type: str = "" if (mime_type is None) else mime_type
        self._file_encoding: Optional[str] = encoding
        self._original_path: Optional[PathLike] = original_path
        self._bom: str = ""

    @overrides
    def __eq__(self, other):
        return isinstance(other, FileValue) and self._id == other._id

    @overrides
    def __hash__(self):
        return hash(self._id)

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_file(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.FILE

    @overrides
    def to_display_string(self, locale_name: str) -> str:
        if self._has_content():
            return RESOURCE_PARSER.get("DisplayFormats", "FILE_CONTENTS_FORMAT").format(
                self._original_path if self._original_path\
                                    else RESOURCE_PARSER.get("DisplayFormats",
                                                             "FILE_LOCATION_UNKNOWN"))
        else:
            return RESOURCE_PARSER.get("DisplayFormats", "FILE_EMPTY")

    BINARY_MIMETYPE: Final[str] = "application/octet-stream"

    TEXT_MIMETYPE: Final[str] = "text/plain"

    ORIGINAL_FILENAME_KEY: Final[str] = "originalFilename"
    """JSON key for API serialization representing the original file name."""

    MIMETYPE_KEY: Final[str] = "mimeType"

    ENCODING_KEY: Final[str] = "encoding"

    CONTENTS_KEY: Final[str] = "contents"

    _DEFAULT_EXT = ".tmp"

    @property
    @abstractmethod
    def actual_content_file_name(self) -> Optional[PathLike]:
        """
        Get a PathLike to the actual file this FileValue wraps.

        Returns
        -------
        PathLike to the file.
        """
        raise NotImplementedError()

    @property
    def mime_type(self) -> str:
        """
        Get the mimetype of this FileValue.

        Returns
        -------
        The mimetype of the file.
        """
        return self._mime_type

    @property
    def original_file_name(self) -> Optional[PathLike]:
        """
        Get the filename of the file that was wrapped.

        Returns
        -------
        The original filename.
        """
        return self._original_path

    @property
    def extension(self) -> str:
        """
        Get the extension of the file.

        Returns
        -------
        The file's extension.
        """
        # TODO: Implement
        raise NotImplementedError()

    @property
    def file_encoding(self) -> Optional[str]:
        """
        Get the encoding of the file.

        Returns
        -------
        The file's encoding.
        """
        return self._file_encoding

    @property
    def id(self) -> UUID:
        """
        Get the id of this FileValue.

        Returns
        -------
        The UUID that identifies this value.
        """
        return self._id

    @staticmethod
    def read_bom(filename: str) -> str:
        """
        Open a file for reading and detects a byte order mark at the \
        beginning.

        Parameters
        ----------
        filename : str
            The file to read.

        Returns
        -------
        str
            If the file contains a BOM, an appropriate encoding will be
            returned. If the file does not contain a BOM, 'None' is
            returned.
        """
        with open(filename, 'rb') as f:
            bom = f.read(4)
            if bom == b'\x00\x00\xfe\xff':
                return "UTF-32 BE"
            elif bom == b'\xff\xfe\x00\x00':
                return "UTF-32 LE"
            elif bom[0:3] == b'\xef\xbb\xbf':
                return "UTF-8"
            elif bom[0:2] == b'\xff\xfe':
                return "UTF-16 LE"
            elif bom[0:2] == b'\xfe\xff':
                return "UTF-16 BE"
            else:
                return "None"

    async def write_file(self, file_name: PathLike) -> None:
        """
        Write the file's contents to a new file.

        Parameters
        ----------
        file_name PathLike to the file to create.

        Returns
        -------
        None.
        """
        # make the file
        Path(file_name).open('w').close()

        # copy the contents from the actual content file
        file: Optional[PathLike] = self.actual_content_file_name
        async with await FileReadStream.from_path(file) as in_stream:
            async with await FileWriteStream.from_path(file_name) as out_stream:
                async for chunk in in_stream:
                    await out_stream.send(chunk)

    @classmethod
    def is_text_based_static(cls, mimetype: str) -> Optional[bool]:
        """
        Determine if a file is text-based via it's mimetype.

        Parameters
        ----------
        mimetype The file's mimetype.

        Returns
        -------
        True if the mimetype starts with text or is application/json,
        False otherwise.
        """
        return str(mimetype).startswith("text/") or str(mimetype).startswith("application/json")

    @property
    def is_text_based(self) -> Optional[bool]:
        """
        Determine if this file is text-based via it's mimetype.

        Returns
        -------
        True if the mimetype starts with text or is application/json,
        False otherwise.
        """
        return FileValue.is_text_based_static(self.mime_type)

    async def get_contents(self, encoding: Optional[str]) -> str:
        """
        Read the file's contents as a string.

        Parameters
        ----------
        encoding The encoding to use when reading.

        Returns
        -------
        The file contents as a string.
        """
        file: Optional[PathLike] = self.actual_content_file_name
        async with await open_file(file=file, encoding=encoding) as f:
            contents = await f.read()
            return contents

    @abstractmethod
    def _has_content(self) -> bool:
        """
        Check whether or not this file value has content.

        This information is used to decide whether or not to pass
        the file value to the file store.

        Returns
        -------
        True if there is content, false otherwise.
        """

    def to_api_string(self, save_context: isave_context.ISaveContext) -> str:
        """
        Convert this value to an API string using a save context.

        Parameters
        ----------
        save_context The save context to use.

        Returns
        -------
        A string appropriate for use in files and APIs.
        """
        api_obj: Dict[str, Optional[str]] = self.to_api_object(save_context)
        return json.dumps(api_obj)

    def _send_actual_file(self, save_context: isave_context.ISaveContext) -> str:
        return save_context.save_file(self.actual_content_file_name, str(self.id))

    def to_api_object(self, save_context: isave_context.ISaveContext) -> Dict[str, Optional[str]]:
        """
        Convert this file to an api object.

        Parameters
        ----------
        save_context The save context used for the conversion.

        Returns
        -------
        API object that matches this FileValue.
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
        return obj

    # TODO: Async get_contents

    def get_extension(self) -> str:
        """
        Get the file extension of the file value held, if known, including the period.

        If the file extension is not known, ".tmp" is returned.
        Returns
        -------
        The file extension of the file value held if known, otherwise, ".tmp"
        """
        ext: str = FileValue._DEFAULT_EXT
        if isinstance(self._original_path, PathLike):
            orig_path, split_ext = path.splitext(self._original_path)
            if split_ext:
                ext = split_ext
        return ext


class EmptyFileValue(FileValue):
    """
    Represents an empty file value.

    Generally speaking, you should not create an instance of this class
    but instead use ansys.common.variableinterop.EMPTY_FILE.
    """

    def __init__(self):
        """
        Construct a new instance.

        Generally speaking you should not create an instance of this
        class but instead use ansys.common.variableinterop.EMPTY_FILE.
        """
        super().__init__(None, None, None, UUID(int=0))

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
