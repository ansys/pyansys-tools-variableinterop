from __future__ import annotations

import json
from abc import ABC, abstractmethod
import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value
import ansys.common.variableinterop.variable_type as variable_type
from os import PathLike
from overrides import overrides
from typing import Any, Callable, Dict, Final, Optional, TypeVar
from uuid import UUID, uuid4

T = TypeVar('T')


class FileValue(variable_value.IVariableValue, ABC):
    """
    Abstract base class for a file variable. To create instances, use a `FileScope`.
    """

    def __init__(self,
                 original_path: Optional[PathLike],
                 mime_type: Optional[str],
                 encoding: Optional[Any],
                 value_id: Optional[UUID]):
        self._id: UUID = uuid4() if (value_id is None) else value_id
        self._mime_type: str = "" if (mime_type is None) else mime_type
        self._file_encoding: Any = encoding
        self._original_path: Optional[PathLike] = original_path

    @overrides
    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        # inheritdoc (What is the correct way to do this?)
        return visitor.visit_file(self)

    @property
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.FILE

    BINARY_MIMETYPE: Final[str] = "application/octet-stream"

    TEXT_MIMETYPE: Final[str] = "text/plain"

    ORIGINAL_FILENAME_KEY: Final[str] = "originalFilename"
    """JSON key for API serialization representing the original file name."""

    ORIGINAL_FILENAME_KEY: Final[str] = "originalFilename"

    MIMETYPE_KEY: Final[str] = "mimeType"

    ENCODING_KEY: Final[str] = "encoding"

    CONTENTS_KEY: Final[str] = "contents"

    @property
    @abstractmethod
    def actual_content_file_name(self) -> Optional[PathLike]:
        raise NotImplementedError()

    @property
    def mime_type(self) -> str:
        return self._mime_type

    @property
    def original_file_name(self) -> Optional[PathLike]:
        return self._original_path

    @property
    def extension(self) -> str:
        # TODO: Implement
        raise NotImplementedError()

    # TODO: Figure out how Python handles encodings and make a proper return type.
    #  Maybe codecs.CodecInfo
    @property
    def file_encoding(self) -> Any:
        return self._file_encoding

    @property
    def id(self) -> UUID:
        return self._id

    @abstractmethod
    def write_file(self, file_name: PathLike) -> None:
        raise NotImplementedError()

    # TODO: Async version?

    @classmethod
    def is_text_based_static(cls, mimetype: str) -> Optional[bool]:
        # TODO: Implement
        raise NotImplementedError()

    @property
    def is_text_based(self) -> Optional[bool]:
        return FileValue.is_text_based_static(self.mime_type)

    # TODO: How does Python handle BOM? implement static and non-static ReadBOM()

    # TODO: Replace Any with correct type for encoding
    @abstractmethod
    def get_contents(self, encoding: Optional[Any]) -> str:
        raise NotImplementedError()

    @overrides
    def get_modelcenter_type(self) -> str:
        raise NotImplementedError

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

    def to_api_string(self, file_store: Callable[[FileValue], str]) -> str:
        api_obj: Dict[str, Optional[str]] = self.to_api_object(file_store)
        return json.dumps(api_obj)

    def to_api_object(self, file_store: Callable[[FileValue], str]) -> Dict[str, Optional[str]]:
        obj: Dict[str, Optional[str]] = {}
        if self._has_content():
            content_marker: str = file_store(self)
            obj[FileValue.CONTENTS_KEY] = content_marker

        if self._original_path:
            obj[FileValue.ORIGINAL_FILENAME_KEY] = self._original_path
        if self._mime_type:
            obj[FileValue.MIMETYPE_KEY] = self._mime_type
        if self._file_encoding:
            obj[FileValue.ENCODING_KEY] = self._file_encoding
        return obj

    # TODO: Async get_contents


class EmptyFileValue(FileValue):
    """
    Represents an empty file value.

    Generally speaking, you should not create an instance of this class but instead use
    ansys.common.variableinterop.EMPTY_FILE.
    """

    def __init__(self):
        """
        Construct a new instance.

        Generally speaking you should not create an instance of this class but instead use
        ansys.common.variableinterop.EMPTY_FILE.
        """
        super().__init__(None, None, None, UUID(int = 0))

    @overrides
    def _has_content(self) -> bool:
        return False

    @property
    @overrides
    def actual_content_file_name(self) -> Optional[PathLike]:
        return None

    def write_file(self, file_name: PathLike) -> None:
        # TODO: Research correct exception to throw
        raise NotImplementedError()

    def get_contents(self, encoding: Optional[Any]) -> str:
        # TODO: Research correct exception to throw
        raise NotImplementedError()


EMPTY_FILE = EmptyFileValue()
