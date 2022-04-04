from __future__ import annotations

from typing import List, Optional

from .coercion import implicit_coerce
from .integer_value import IntegerValue
from .numeric_metadata import NumericMetadata
from .variable_type import VariableType


class IntegerMetadata(NumericMetadata):
    """Common metadata for VariableType.INTEGER and VariableType.INTEGERL_ARRAY"""

    def __init__(self) -> None:
        self._lower_bound: Optional[IntegerValue] = None
        self._upper_bound: Optional[IntegerValue] = None
        self._enumerated_values: List[IntegerValue] = []
        self._enumerated_aliases: List[str] = []

    def variable_type(self) -> VariableType:
        return VariableType.INTEGER

    @property
    def lower_bound(self) -> Optional[IntegerValue]:
        """
        A hard lower bound for this variable. Systems utilizing this variable should
        prevent setting the value below this lower bound. This is typically used to
        represent physical impossibilities (negative length) or limits of the simulation
        software (values below this will cause an error or invalid result). This may not
        be the soft bounds used for an optimization design parameter or DOE exploration.

        Returns
        -------
        The lower bound, or None if no lower bound is specified.
        """
        return self._lower_bound

    @lower_bound.setter  # type: ignore
    @implicit_coerce
    def lower_bound(self, value: Optional[IntegerValue]) -> None:
        # TODO: How does documentation for properties work?
        self._lower_bound = value

    @property
    def upper_bound(self) -> Optional[IntegerValue]:
        """
        A hard upper bound for this variable. Systems utilizing this variable should
        prevent setting the value above this upper bound. This is typically used to
        represent physical impossibilities (100%) or limits of the simulation
        software (values above this will cause an error or invalid result). This may not
        be the soft bounds used for an optimization design parameter or DOE exploration.

        Returns
        -------
        The upper bound, or None if no upper bound is specified.
        """
        return self._upper_bound

    @upper_bound.setter  # type: ignore
    @implicit_coerce
    def upper_bound(self, value: Optional[IntegerValue]) -> None:
        # TODO: How does documentation for properties work?
        self._upper_bound = value

    # TODO need implicit coerce for arrays

    @property
    def enumerated_values(self) -> List[IntegerValue]:
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[IntegerValue]) -> None:
        self._enumerated_values = value

    @property
    def enumerated_aliases(self) -> List[str]:
        return self._enumerated_aliases

    @enumerated_aliases.setter
    def enumerated_aliases(self, value: List[str]) -> None:
        self._enumerated_aliases = value
