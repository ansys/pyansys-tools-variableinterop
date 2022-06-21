"""Implementation of FileScope."""
from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from os import PathLike
from types import TracebackType
from typing import Dict, Optional, Type

from overrides import overrides

from .file_value import FileValue
from .isave_context import ILoadContext


class FileScope(AbstractContextManager, ABC):
    """
    Abstract base class that represents a file scope.

    A file scope helps a program manage disk use for file storage and
    enables it to clean up caches and space in a reliable way.
    `FileValue` instances except for
    `ansys.common.variableinterop.EMPTY_FILE` should always be created
    by a `FileScope` instance. `FileValue` instances created by a
    `FileScope` are not valid once the `FileScope` has been closed.

    This abstract base class contains the logic to be a Context Manager
    for use in `with` blocks. Any derived class's `close` method will be
    automatically called when the `with` block is exited.
    """

    def __init__(self):
        """Initialize."""
        pass

    @overrides
    def __exit__(
        self,
        __exc_type: Type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        self.close()
        return None

    @abstractmethod
    def close(self) -> None:
        """TODO."""
        ...

    @abstractmethod
    def read_from_file(
        self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]
    ) -> FileValue:
        """TODO."""
        ...

    @abstractmethod
    def from_api_object(
        self, api_object: Dict[str, Optional[str]], load_context: ILoadContext
    ) -> FileValue:
        """TODO."""
        ...
