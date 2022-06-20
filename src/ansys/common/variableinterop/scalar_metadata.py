"""Definition of scalar metadata types."""
from __future__ import annotations

from typing import Any, List, Optional, TypeVar

from overrides import overrides

import ansys.common.variableinterop.common_variable_metadata as common_variable_metadata
import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.variable_type as variable_type

from .numeric_metadata import NumericMetadata
from .scalar_values import IntegerValue, RealValue, StringValue
from .utils.implicit_coercion import implicit_coerce

T = TypeVar("T")


class BooleanMetadata(common_variable_metadata.CommonVariableMetadata):
    """Common metadata for VariableType.BOOLEAN and VariableType.BOOLEAN_ARRAY."""

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def accept(self, visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    @overrides
    def equals(self, other: Any) -> bool:
        equal: bool = isinstance(other, BooleanMetadata) and super().equals(other)
        return equal


class IntegerMetadata(NumericMetadata):
    """Common metadata for VariableType.INTEGER and VariableType.INTEGER_ARRAY."""

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._lower_bound: Optional[IntegerValue] = None
        self._upper_bound: Optional[IntegerValue] = None
        self._enumerated_values: List[IntegerValue] = []
        self._enumerated_aliases: List[str] = []

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def accept(self, visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_integer(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.INTEGER

    @property
    def lower_bound(self) -> Optional[IntegerValue]:
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
    def lower_bound(self, value: Optional[IntegerValue]) -> None:
        """Set the lower bound."""
        self._lower_bound = value

    @property
    def upper_bound(self) -> Optional[IntegerValue]:
        """
        Hard upper bound for this variable.

        Systems utilizing this variable should prevent setting the
        value above this upper bound. This is typically used to
        represent physical impossibilities (100%) or limits of the
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
    def upper_bound(self, value: Optional[IntegerValue]) -> None:
        """Set the upper bound."""
        self._upper_bound = value

    @property
    def enumerated_values(self) -> List[IntegerValue]:
        """
        Get the list of enumerated values.

        May be empty to imply no enumerated values.
        Returns
        -------
        The list of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[IntegerValue]) -> None:
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

    @overrides
    def equals(self, other: Any) -> bool:
        equal: bool = (
            isinstance(other, IntegerMetadata)
            and super().equals(other)
            and self._lower_bound == other._lower_bound
            and self._upper_bound == other._upper_bound
            and self._enumerated_values == other._enumerated_values
            and self._enumerated_aliases == other._enumerated_aliases
        )
        return equal


class RealMetadata(NumericMetadata):
    """Common metadata for VariableType.REAL and VariableType.REAL_ARRAY."""

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._lower_bound: Optional[RealValue] = None
        self._upper_bound: Optional[RealValue] = None
        self._enumerated_values: List[RealValue] = []
        self._enumerated_aliases: List[str] = []

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def accept(self, visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_real(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.REAL

    @property
    def lower_bound(self) -> Optional[RealValue]:
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
    def lower_bound(self, value: Optional[RealValue]) -> None:
        """Set the lower bound."""
        self._lower_bound = value

    @property
    def upper_bound(self) -> Optional[RealValue]:
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
    def upper_bound(self, value: Optional[RealValue]) -> None:
        """Set the upper bound."""
        self._upper_bound = value

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

    @overrides
    def equals(self, other: Any) -> bool:
        equal: bool = (
            isinstance(other, RealMetadata)
            and super().equals(other)
            and self._lower_bound == other._lower_bound
            and self._upper_bound == other._upper_bound
            and self._enumerated_values == other._enumerated_values
            and self._enumerated_aliases == other._enumerated_aliases
        )
        return equal


class StringMetadata(common_variable_metadata.CommonVariableMetadata):
    """Common metadata for VariableType.STRING and VariableType.STRING_ARRAY."""

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._enumerated_values: List[StringValue] = []
        self._enumerated_aliases: List[str] = []

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def accept(self, visitor: ivariablemetadata_visitor.IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_string(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.STRING

    @property
    def enumerated_values(self) -> List[StringValue]:
        """
        Get the list of enumerated values.

        May be empty to imply no enumerated values.
        Returns
        -------
        The list of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[StringValue]) -> None:
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

    @overrides
    def equals(self, other: Any) -> bool:
        equal: bool = (
            isinstance(other, StringMetadata)
            and super().equals(other)
            and self._enumerated_values == other._enumerated_values
            and self._enumerated_aliases == other._enumerated_aliases
        )
        return equal
