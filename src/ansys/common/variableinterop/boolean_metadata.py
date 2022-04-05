"""Definition of BooleanMetadata."""
from __future__ import annotations

from . import CommonVariableMetadata
from .variable_type import VariableType


class BooleanMetadata(CommonVariableMetadata):
    """Common metadata for VariableType.BOOLEAN and VariableType.BOOLEAN_ARRAY."""

    # equality definition here

    # clone here

    # accept here

    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN

    # TODO need implicit coerce for arrays
