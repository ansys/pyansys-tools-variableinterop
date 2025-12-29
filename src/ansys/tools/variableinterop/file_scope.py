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
"""Implements the ``FileScope`` class."""
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

    A file scope helps a program manage the disk space used for file storage and
    enables it to clean up caches and space in a reliable way.
    ``FileValue`` instances (except for ``ansys.tools.variableinterop.EMPTY_FILE``)
    should always be created by a ``FileScope`` instance. ``FileValue`` instances
    created by a ``FileScope`` instance are not valid once the ``FileScope`` instance
    has been closed.

    This abstract base class contains the logic to be a context manager
    for use in ``with`` blocks. Any derived class's ``close`` method is
    automatically called when the ``with`` block is exited.
    """

    def __init__(self):
        """Initialize a new instance."""
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
        """Close the ``FileScope`` instance, cleaning up any files it contains."""
        ...

    @abstractmethod
    def read_from_file(
        self, to_read: PathLike, mime_type: Optional[str] = None, encoding: Optional[str] = None
    ) -> FileValue:
        """
        Read the contents of a file and create a new ``FileValue`` object backed by a
        file in this scope.

        Parameters
        ----------
        to_read : PathLike
            Path to the file to read.
        mime_type : Optional[str], optional
            MIME type of the file. The default is `None`, which indicates that the file
            does not have a MIME type or that the type is not known.
        encoding : Optional[str], optional
            Encoding of the file. The default is `None`, which indicates that the file
            does not have a text encoding (for example, because it is a binary file.)

        Returns
        -------
        FileValue
            New ``FileValue`` object with the contents of the specified file, backed by this scope.
        """
        ...

    @abstractmethod
    def from_api_object(
        self, api_object: Dict[str, Optional[str]], load_context: ILoadContext
    ) -> FileValue:
        """
        Create a ``FileScope`` instance from a map of API strings.

        Parameters
        ----------
        api_object : Dict[str, Optional[str]]
            Map of API strings that define the scope.
        load_context : ILoadContext
            Load context to read the file contents from.
        """
        ...
