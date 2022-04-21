from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from os import PathLike
from typing import Dict, Optional

import ansys.common.variableinterop.file_value as file_value
import ansys.common.variableinterop.isave_context as isave_context

# TODO: What formatting does pydoc use? I'm using back tick for code below.
#  Who knows if that is correct


class FileScope(AbstractContextManager, ABC):
    """
    Abstract base class that represents a file scope. A file scope helps a program manage disk
    use for file storage and enables it to clean up caches and space in a reliable way. `FileValue`
    instances except for `ansys.common.variableinterop.EMPTY_FILE` should always be created by
    a `FileScope` instance. `FileValue` instances created by a `FileScope` are not valid once the
    `FileScope` has been closed.

    This abstract base class contains the logic to be a Context Manager for use in `with` blocks.
    Any derived class's `close` method will be automatically called when the `with` block is exited.
    """

    def __init__(self):
        pass

    # TODO: Proper types for this method
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return None

    @abstractmethod
    def close(self) -> None:
        ...

    # TODO: Proper type for encoding
    @abstractmethod
    def read_from_file(
        self, to_read: PathLike, mime_type: Optional[str], encoding: Optional[str]
    ) -> file_value.FileValue:
        ...

    @abstractmethod
    def from_api_object(self,
                        api_object: Dict[str, Optional[str]],
                        load_context: isave_context.ILoadContext) -> file_value.FileValue:
        ...

    # TODO: All the many static construction methods
