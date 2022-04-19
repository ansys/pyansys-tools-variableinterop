from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from os import PathLike
from typing import Optional, Union


class ISaveContext(AbstractContextManager, ABC):
    """
    An abstraction for a save medium.

    In order to separate the concerns of being able to save large associated content in other
    transfer mediums, this interface was defined which allows out of bound data to be transferred.
    Examples include saving to a ZIP file, or using an SCP side-channel on an SSH connection to send
    files or other large data.
    """

    # TODO: Proper types for this method
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return None

    @abstractmethod
    def save_file(self, source: Union[PathLike, str], id: Optional[str]) -> str:
        """
        Save a file to the save medium

        Note, it is up to the ISaveContext implementation to decide how or when to send the actual
        data. Some ISaveContexts may merely collect metadata as part of this call and actually
        send the data on flush.

        Parameters
        ----------
        source the file on disk to send or include in the save.
        id If a unique ID is already known for the file, include it here. If it is not provided
            one will be generated and returned. This ID can be used with an equivalent
            ILoadContext to load the contents on deserialize.

        Returns
        -------
        If an id was provided, returns that ID, otherwise generates one and returns it.
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
        ...

    @abstractmethod
    def close(self) -> None:
        ...


class ILoadContext(AbstractContextManager, ABC):

    # TODO: Proper types for this method
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return None

    @abstractmethod
    def load_file(self, source: Union[PathLike, str], id: Optional[str]) -> str:
        ...

# TODO: Uncomment once we know what stream API to use
#    @abstractmethod
#    def load_file_stream(self, source: Union[PathLike, str], id: Optional[str]) \
#            -> Tuple[Stream, str]:
#        ...

    @abstractmethod
    def flush(self) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...