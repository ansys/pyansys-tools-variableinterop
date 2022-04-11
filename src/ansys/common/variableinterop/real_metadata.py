"""Definition of RealMetadata."""
from __future__ import annotations

from typing import List, Optional, TypeVar

from overrides import overrides

import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.numeric_metadata as variable_metadata
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.variable_type as variable_type

from .coercion import implicit_coerce

T = TypeVar("T")


class RealMetadata(variable_metadata.NumericMetadata):
    """Common metadata for VariableType.REAL and VariableType.REAL_ARRAY."""

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._lower_bound: Optional[real_value.RealValue] = None
        self._upper_bound: Optional[real_value.RealValue] = None
        self._enumerated_values: List[real_value.RealValue] = []
        self._enumerated_aliases: List[str] = []

    # equality definition here

    # clone here

    @overrides
    def accept(self, visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_real(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.REAL

    @property
    def lower_bound(self) -> Optional[real_value.RealValue]:
        """
        Hard lower bound for this variable.

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
    def lower_bound(self, value: Optional[real_value.RealValue]) -> None:
        """Set the lower bound."""
        self._lower_bound = value

    @property
    def upper_bound(self) -> Optional[real_value.RealValue]:
        """
        Hard upper bound for this variable.

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
    def upper_bound(self, value: Optional[real_value.RealValue]) -> None:
        """Set the upper bound."""
        self._upper_bound = value

    # TODO need implicit coerce for arrays

    @property
    def enumerated_values(self) -> List[real_value.RealValue]:
        """
        Get the list of enumerated values.

        May be empty to imply no enumerated values.
        Returns
        -------
        The list of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[real_value.RealValue]) -> None:
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
