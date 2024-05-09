
from configparser import ConfigParser
from functools import cached_property
import os


class IncompatibleTypesError(TypeError):
    """Indicates that the types used in a conversion are incompatible."""

    @cached_property
    def _strings(self) -> ConfigParser:
        parser = ConfigParser()
        parser.read(os.path.join(os.path.dirname(__file__), "strings.properties"))
        return parser

    def __init__(self, from_type: str, to_type: str) -> None:
        self.from_type_str = from_type
        self.to_type_str = to_type
        msg = self._strings.get("Errors", "ERROR_INCOMPATIBLE_TYPES").format(from_type, to_type)
        super().__init__(msg)