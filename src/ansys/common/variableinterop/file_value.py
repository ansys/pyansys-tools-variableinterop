from __future__ import annotations

from abc import ABC, abstractmethod

# when we support Python 3.8
# from typing import Final
from os import PathLike
from typing import Any, Optional
from uuid import UUID

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor
import ansys.common.variableinterop.variable_value as variable_value

from .variable_type import VariableType


class FileValue(variable_value.IVariableValue, ABC):
    """
    Abstract base class for a file variable. To create instances, use a `FileScope`.
    """

    def accept(
        self, visitor: ivariable_visitor.IVariableValueVisitor[variable_value.T]
    ) -> variable_value.T:
        # inheritdoc (What is the correct way to do this?)
        return visitor.visit_file(self)

    @property
    def variable_type(self) -> VariableType:
        return VariableType.FILE

    # TODO: Once we support Python 3.8 minimum, make this Final[str]
    BINARY_MIMETYPE: str = "application/octet-stream"

    # TODO: Once we support Python 3.8 minimum, make this Final[str]
    TEXT_MIMETYPE: str = "text/plain"

    @property
    @abstractmethod
    def actual_content_file_name(self) -> Optional[PathLike]:
        ...

    @property
    @abstractmethod
    def mime_type(self) -> str:
        ...

    @property
    @abstractmethod
    def original_file_name(self) -> Optional[PathLike]:
        ...

    @property
    def extension(self) -> str:
        # TODO: Implement
        raise NotImplementedError()

    # TODO: Figure out how Python handles encodings and make a proper return type.
    #  Maybe codecs.CodecInfo
    @property
    @abstractmethod
    def file_encoding(self) -> Any:
        ...

    # TODO: Maybe this as an ABC could store some of this info without needing to make so many
    # abstract methods?

    @property
    @abstractmethod
    def id(self) -> UUID:
        ...

    @abstractmethod
    def write_file(self, file_name: PathLike) -> None:
        ...

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
        ...

    # TODO: Async get_contents


class EmptyFileValue(FileValue):
    """
    Generally speaking you should not create an instance of this class but instead use
    ansys.variableinterop.EMPTY_FILE
    """

    @property
    def actual_content_file_name(self) -> Optional[PathLike]:
        return None

    @property
    def mime_type(self) -> str:
        return ""

    @property
    def original_file_name(self) -> Optional[PathLike]:
        return None

    @property
    def file_encoding(self) -> Any:
        return None

    _zerouuid: UUID = UUID(int=0)

    @property
    def id(self) -> UUID:
        return EmptyFileValue._zerouuid

    def write_file(self, file_name: PathLike) -> None:
        # TODO: Research correct exception to throw
        raise NotImplementedError()

    def get_contents(self, encoding: Optional[Any]) -> str:
        # TODO: Research correct exception to throw
        raise NotImplementedError()


EMPTY_FILE = EmptyFileValue()
