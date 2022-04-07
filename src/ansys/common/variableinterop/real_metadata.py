"""Definition of RealMetadata."""
from __future__ import annotations

from typing import List, Optional

from .coercion import implicit_coerce
from .numeric_metadata import NumericMetadata
from .real_value import RealValue
from .variable_type import VariableType


class RealMetadata(NumericMetadata):
    """Common metadata for VariableType.REAL and VariableType.REAL_ARRAY."""

    def __init__(self) -> None:
        super().__init__()
        self._lower_bound: Optional[RealValue] = None
        self._upper_bound: Optional[RealValue] = None
        self._enumerated_values: List[RealValue] = []
        self._enumerated_aliases: List[str] = []

    # equality definition here

    # clone here

    # accept here

    def variable_type(self) -> VariableType:
        return VariableType.INTEGER

    @property
    def lower_bound(self) -> Optional[RealValue]:
        """
        A hard lower bound for this variable.

        Systems utilizing this variable should prevent setting the
        value below this lower bound. This is typically used to
        represent physical impossibilities (negative length) or limits
        of the simulation software (values below this will cause an
        error or invalid result). This may not be the soft bounds used
        for an optimization design parameter or DOE exploration.

        Returns
        -------
        The lower bound, or None if no lower bound is specified.
        """
        return self._lower_bound

    @lower_bound.setter  # type: ignore
    @implicit_coerce
    def lower_bound(self, value: Optional[RealValue]) -> None:
        """Set the lower bound."""
        self._lower_bound = value

    @property
    def upper_bound(self) -> Optional[RealValue]:
        """
        A hard upper bound for this variable.

        Systems utilizing this variable should prevent setting the
        value above this upper bound. This is typically used
        to represent physical impossibilities (100%) or limits of the
        simulation software (values above this will cause an error or
        invalid result). This may not be the soft bounds used for an
        optimization design parameter or DOE exploration.

        Returns
        -------
        The upper bound, or None if no upper bound is specified.
        """
        return self._upper_bound

    @upper_bound.setter  # type: ignore
    @implicit_coerce
    def upper_bound(self, value: Optional[RealValue]) -> None:
        """Set the upper bound."""
        self._upper_bound = value

    # TODO need implicit coerce for arrays

    @property
    def enumerated_values(self) -> List[RealValue]:
        """
        Get the list of enumerated values.

        May be empty to imply no enumerated values.
        Returns
        -------
        The list of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[RealValue]) -> None:
        """
        Set the list of enumerated values.

        Parameters
        ----------
        value
        The list of values to set.
        """
        self._enumerated_values = value

    @property
    def enumerated_aliases(self) -> List[str]:
        """
        Get the list of enumerated aliases.

        May be empty to imply no enumerated aliases.
        Returns
        -------
        The list of enumerated aliases.
        """
        return self._enumerated_aliases

    @enumerated_aliases.setter
    def enumerated_aliases(self, value: List[str]) -> None:
        """
        Set the list of enumerated aliases.

        Parameters
        ----------
        value
        The list of aliases to set.
        """
        self._enumerated_aliases = value
