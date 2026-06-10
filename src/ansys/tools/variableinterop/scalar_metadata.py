# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
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
"""Defines scalar metadata types."""
from __future__ import annotations

from typing import Any, List, Optional

from overrides import overrides

from .common_variable_metadata import CommonVariableMetadata
from .ivariablemetadata_visitor import IVariableMetadataVisitor, T
from .numeric_metadata import NumericMetadata
from .scalar_values import IntegerValue, RealValue, StringValue
from .utils.implicit_coercion import implicit_coerce
from .variable_type import VariableType


class BooleanMetadata(CommonVariableMetadata):
    """Provides metadata for ``BOOLEAN`` and ``BOOLEAN_ARRAY`` variable types."""

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.BOOLEAN

    @overrides
    def equals(self, other: Any) -> bool:
        equal: bool = isinstance(other, BooleanMetadata) and super().equals(other)
        return equal

    @overrides
    def to_dict(self) -> dict:
        result = super().to_dict()
        return result

    @classmethod
    @overrides
    def from_dict(cls, data) -> "BooleanMetadata":
        description, custom_metadata = super()._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata
        return result


class IntegerMetadata(NumericMetadata):
    """Provides metadata for ``INTEGER`` and ``INTEGER_ARRAY`` variable types."""

    _lower_bound_json_key = "lowerBound"
    _upper_bound_json_key = "upperBound"
    _enumerated_values_json_key = "enumValues"
    _enumerated_aliases_json_key = "enumAliases"

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
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_integer(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.INTEGER

    @property
    def lower_bound(self) -> Optional[IntegerValue]:
        """
        Hard lower bound for the variable.

        Systems utilizing this variable should prevent setting the
        value below this lower bound. This is typically used to
        represent physical impossibilities (negative length) or limits
        of the simulation software. Values below this hard lower bound
        cause an error or invalid result. This may not be the soft bounds used
        for an optimization design parameter or DOE exploration.

        Returns
        -------
        Optional[IntegerValue]
            Lower bound or ``None`` if no lower bound is specified.
        """
        return self._lower_bound

    @lower_bound.setter  # type: ignore
    @implicit_coerce
    def lower_bound(self, value: Optional[IntegerValue]) -> None:
        self._lower_bound = value

    @property
    def upper_bound(self) -> Optional[IntegerValue]:
        """
        Hard upper bound for the variable.

        Systems utilizing this variable should prevent setting the
        value above this upper bound. This is typically used to
        represent physical impossibilities (100%) or limits of the
        simulation software. Values above this hard upper bound cause
        an error or invalid result. This may not be the soft bounds used for an
        optimization design parameter or DOE exploration.

        Returns
        -------
        Optional[IntegerValue]
            Upper bound or ``None`` if no upper bound is specified.
        """
        return self._upper_bound

    @upper_bound.setter  # type: ignore
    @implicit_coerce
    def upper_bound(self, value: Optional[IntegerValue]) -> None:
        self._upper_bound = value

    @property
    def enumerated_values(self) -> List[IntegerValue]:
        """
        List of enumerated values.

        This list may be empty to imply that there are no enumerated values.

        Returns
        -------
        List[IntegerValue]
            List of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[IntegerValue]) -> None:
        """
        Set the list of enumerated values.

        Parameters
        ----------
        value : List[IntegerValue]
            List of values to set.
        """
        self._enumerated_values = value

    @property
    def enumerated_aliases(self) -> List[str]:
        """
        List of enumerated aliases.

        This list may be empty to imply that there are no enumerated aliases.

        Returns
        -------
        List[str]
            List of enumerated aliases.
        """
        return self._enumerated_aliases

    @enumerated_aliases.setter
    def enumerated_aliases(self, value: List[str]) -> None:
        """
        Set the list of enumerated aliases.

        Parameters
        ----------
        value : List[str]
            List of aliases to set.
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

    @overrides
    def to_dict(self) -> dict:
        from . import VariableValueToJsonVisitor

        visitor = VariableValueToJsonVisitor()

        result = super().to_dict()

        if self._lower_bound is not None:
            result[IntegerMetadata._lower_bound_json_key] = self._lower_bound.accept(visitor)
        if self._upper_bound is not None:
            result[IntegerMetadata._upper_bound_json_key] = self._upper_bound.accept(visitor)
        if len(self._enumerated_values) > 0:
            result[IntegerMetadata._enumerated_values_json_key] = [
                value.accept(visitor) for value in self._enumerated_values
            ]
        if len(self._enumerated_aliases) > 0:
            result[IntegerMetadata._enumerated_aliases_json_key] = self._enumerated_aliases
        return result

    @classmethod
    @overrides
    def from_dict(cls, data: dict) -> "IntegerMetadata":
        description, custom_metadata = CommonVariableMetadata._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata

        units, display_format = NumericMetadata._from_dict(data)
        result.units = units
        result.display_format = display_format

        result.lower_bound = data.get(IntegerMetadata._lower_bound_json_key)
        result.upper_bound = data.get(IntegerMetadata._upper_bound_json_key)
        result.enumerated_values = data.get(IntegerMetadata._enumerated_values_json_key, [])
        result.enumerated_aliases = data.get(IntegerMetadata._enumerated_aliases_json_key, [])

        return result


class RealMetadata(NumericMetadata):
    """Provides metadata for ``REAL`` and ``REAL_ARRAY`` variable types."""

    _lower_bound_json_key = "lowerBound"
    _upper_bound_json_key = "upperBound"
    _enumerated_values_json_key = "enumValues"
    _enumerated_aliases_json_key = "enumAliases"

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
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_real(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.REAL

    @property
    def lower_bound(self) -> Optional[RealValue]:
        """
        Hard lower bound for the variable.

        Systems utilizing this variable should prevent setting the
        value below this lower bound. This is typically used to
        represent physical impossibilities (negative length) or limits
        of the simulation software. Values below this hard lower bound
        cause an error or invalid result. This may not be the soft bounds
        used for an optimization design parameter or DOE exploration.

        Returns
        -------
        Optional[RealValue]
            Lower bound or ``None`` if no lower bound is specified.
        """
        return self._lower_bound

    @lower_bound.setter  # type: ignore
    @implicit_coerce
    def lower_bound(self, value: Optional[RealValue]) -> None:
        self._lower_bound = value

    @property
    def upper_bound(self) -> Optional[RealValue]:
        """
        Hard upper bound for the variable.

        Systems utilizing this variable should prevent setting the
        value above this upper bound. This is typically used
        to represent physical impossibilities (100%) or limits of the
        simulation software. Values above this hard upper bound cause an error or
        invalid result. This may not be the soft bounds used for an
        optimization design parameter or DOE exploration.

        Returns
        -------
        Optional[RealValue]
            Upper bound or ``None`` if no upper bound is specified.
        """
        return self._upper_bound

    @upper_bound.setter  # type: ignore
    @implicit_coerce
    def upper_bound(self, value: Optional[RealValue]) -> None:
        self._upper_bound = value

    @property
    def enumerated_values(self) -> List[RealValue]:
        """
        List of enumerated values.

        This list may be empty to imply that there are no enumerated values.

        Returns
        -------
        List[RealValue]
           List of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[RealValue]) -> None:
        """
        Set the list of enumerated values.

        Parameters
        ----------
        value : List[RealValue]
            List of values to set.
        """
        self._enumerated_values = value

    @property
    def enumerated_aliases(self) -> List[str]:
        """
        List of enumerated aliases.

        This list may be empty to imply that there are no enumerated aliases.

        Returns
        -------
        List[str]
            List of enumerated aliases.
        """
        return self._enumerated_aliases

    @enumerated_aliases.setter
    def enumerated_aliases(self, value: List[str]) -> None:
        """
        Set the list of enumerated aliases.

        Parameters
        ----------
        value : List[str]
            List of aliases to set.
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

    @overrides
    def to_dict(self) -> dict:
        from . import VariableValueToJsonVisitor

        visitor = VariableValueToJsonVisitor()

        result = super().to_dict()

        if self._lower_bound is not None:
            result[RealMetadata._lower_bound_json_key] = self._lower_bound.accept(visitor)
        if self._upper_bound is not None:
            result[RealMetadata._upper_bound_json_key] = self._upper_bound.accept(visitor)
        if len(self._enumerated_values) > 0:
            result[RealMetadata._enumerated_values_json_key] = [
                value.accept(visitor) for value in self._enumerated_values
            ]
        if len(self._enumerated_aliases) > 0:
            result[RealMetadata._enumerated_aliases_json_key] = self._enumerated_aliases
        return result

    @classmethod
    @overrides
    def from_dict(cls, data) -> "RealMetadata":
        description, custom_metadata = CommonVariableMetadata._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata

        units, display_format = NumericMetadata._from_dict(data)
        result.units = units
        result.display_format = display_format

        result.lower_bound = data.get(RealMetadata._lower_bound_json_key)
        result.upper_bound = data.get(RealMetadata._upper_bound_json_key)
        result.enumerated_values = data.get(RealMetadata._enumerated_values_json_key, [])
        result.enumerated_aliases = data.get(RealMetadata._enumerated_aliases_json_key, [])

        return result


class StringMetadata(CommonVariableMetadata):
    """Provides common metadata for ``STRING`` and ``STRING_ARRAY`` variable types."""

    _enumerated_values_json_key = "enumValues"
    _enumerated_aliases_json_key = "enumAliases"

    @overrides
    def __init__(self) -> None:
        super().__init__()
        self._enumerated_values: List[StringValue] = []
        self._enumerated_aliases: List[str] = []

    @overrides
    def __eq__(self, other):
        return self.equals(other)

    @overrides
    def accept(self, visitor: IVariableMetadataVisitor[T]) -> T:
        return visitor.visit_string(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> VariableType:
        return VariableType.STRING

    @property
    def enumerated_values(self) -> List[StringValue]:
        """
        List of enumerated values.

        This list may be empty to imply that there are no enumerated values.

        Returns
        -------
        List[StringValue]
            List of enumerated values.
        """
        return self._enumerated_values

    @enumerated_values.setter
    def enumerated_values(self, value: List[StringValue]) -> None:
        """
        Set the list of enumerated values.

        Parameters
        ----------
        value : List[StringValue]
            List of values to set.
        """
        self._enumerated_values = value

    @property
    def enumerated_aliases(self) -> List[str]:
        """
        List of enumerated aliases.

        This list may be empty to imply that there are no enumerated aliases.

        Returns
        -------
        List[str]
            List of enumerated aliases.
        """
        return self._enumerated_aliases

    @enumerated_aliases.setter
    def enumerated_aliases(self, value: List[str]) -> None:
        """
        Set the list of enumerated aliases.

        Parameters
        ----------
        value : List[str]
            List of aliases to set.
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

    @overrides
    def to_dict(self) -> dict:
        from . import VariableValueToJsonVisitor

        visitor = VariableValueToJsonVisitor()

        result = super().to_dict()
        if len(self._enumerated_values) > 0:
            result[StringMetadata._enumerated_values_json_key] = [
                value.accept(visitor) for value in self._enumerated_values
            ]
        if len(self._enumerated_aliases) > 0:
            result[StringMetadata._enumerated_aliases_json_key] = self._enumerated_aliases
        return result

    @classmethod
    @overrides
    def from_dict(cls, data) -> "StringMetadata":
        description, custom_metadata = super()._from_dict(data)
        result = cls()
        result.description = description
        # result.custom_metadata = custom_metadata

        result.enumerated_values = data.get(StringMetadata._enumerated_values_json_key, [])
        result.enumerated_aliases = data.get(StringMetadata._enumerated_aliases_json_key, [])

        return result
