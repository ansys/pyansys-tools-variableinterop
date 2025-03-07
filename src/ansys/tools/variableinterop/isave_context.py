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
"""Defines the ``ISaveContext`` class."""
from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from os import PathLike
from types import TracebackType
from typing import Optional, Type, Union

from overrides import overrides


class ISaveContext(AbstractContextManager, ABC):
    """
    Defines an abstraction for a save medium.

    This interface was defined to separate the concerns of being able to save large
    associated content in other transfer mediums. It allows out-of-bound data to be
    transferred. Examples include saving to a ZIP file or using an SCP side-channel on
    an SSH connection to send files or other large data objects.
    """

    @overrides
    def __exit__(
        self,
        __exc_type: Type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        """Magic method exit."""
        self.close()
        return None

    @abstractmethod
    def save_file(self, source: Union[PathLike, str], content_id: Optional[str] = None) -> str:
        """
        Save a file to the save medium.

        It is up to the ``ISaveContext`` implementation to decide how or when to send the actual
        data. Some ``ISaveContext`` implementations may merely collect metadata as part of this
        call and send the data on flush.

        Parameters
        ----------
        source : Union[PathLike, str]
            File on disk to send or include in the save.
        content_id : Optional[str], optional
            Unique ID for the file. The default value is ``None``, in which case an ID
            is automatically generated and returned. This ID can be used with an equivalent
            ``ILoadContext`` instance to load the contents on deserialization.

        Returns
        -------
        str
            ID, either the one provided or the one otherwise generated.
        """
        ...

    # TODO: What stream API to use?
    # TODO: Async?

    # TODO: Uncomment once we know what stream API to use
    #    @abstractmethod
    #   def save_file_stream(self, source: Union[PathLike, str], id: Optional[str]) \
    #            -> Tuple[Stream, str]:
    #        ...

    @abstractmethod
    def flush(self) -> None:
        """Flush any changes in the context to the underlying stream or file."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close the context."""
        ...


class ILoadContext(AbstractContextManager, ABC):
    """
    Defines an abstraction for a load medium.

    This interface was defined to separate the concerns of being able to save large
    associated content in other transfer mediums. It allows out-of-bound data to be
    transferred. Examples include saving to a ZIP file or using an SCP side-channel on
    an SSH connection to send files or other large data objects.
    """

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
    def load_file(self, content_id: Optional[str]) -> Optional[PathLike]:
        """
        Load a file from the load medium.

        The ``ILoadContext`` implementation decides how or when to send the actual
        data. Some ``ILoadContexts`` implementations may merely collect metadata as
        part of this call and send the data on flush.

        Parameters
        ----------
        content_id : Optional[str]
            ID generated by an equivalent ``ISaveContext`` instance to save a file into this
            context.

        Returns
        -------
        Optional[PathLike]
            Path to the loaded file.
        """
        ...

    # TODO: Uncomment once we know what stream API to use
    #    @abstractmethod
    #    def load_file_stream(self, source: Union[PathLike, str], id: Optional[str]) \
    #            -> Tuple[Stream, str]:
    #        ...

    @abstractmethod
    def flush(self) -> None:
        """Flush any changes in the context to the underlying stream or file."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close the context."""
        ...
