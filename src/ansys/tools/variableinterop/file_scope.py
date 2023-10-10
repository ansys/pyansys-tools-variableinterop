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
    Provides an abstract base for file scopes.

    A file scope helps a program manage disk use for file storage and
    enables it to clean up caches and space in a reliable way.
    `FileValue` instances except for
    `ansys.tools.variableinterop.EMPTY_FILE` should always be created
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
        """Close the file scope, cleaning up any files it contains."""
        ...

    @abstractmethod
    def read_from_file(
        self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]
    ) -> FileValue:
        """
        Read the contents of a file and create a new ``FileValue`` backed by a file in this
        scope.

        Parameters
        ----------
        to_read : PathLike
            Path to the file to read.
        mime_type : str, optional
            Mime type of the file.
        encoding : str, optional
            Encoding of the file.

        Returns
        -------
        FileValue
            New ``FileValue`` with the contents of the specified file, backed by this scope.
        """
        ...

    @abstractmethod
    def from_api_object(
        self, api_object: Dict[str, Optional[str]], load_context: ILoadContext
    ) -> FileValue:
        """
        Create a ``FileScope`` from a map of API strings.

        Parameters
        ----------
        api_object : Dict[str, Optional[str]]
            Map of API strings that define the scope.
        load_context : ILoadContext
            Load context to read the file contents from.
        """
        ...
