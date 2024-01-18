"""Defines the ``VariableState`` class."""
from __future__ import annotations

from .utils.implicit_coercion import implicit_coerce
from .variable_value import IVariableValue, VariableValueInvalidError


class VariableState:
    """Bundles a variable value with a validity flag."""

    @implicit_coerce
    def __init__(self, value: IVariableValue, is_valid: bool):
        """
        Initialize a new instance.

        Parameters
        ----------
        value : IVariableValue
            Variable value.
        is_valid : bool
            Whether the flag is valid. ``True`` indicates that the value is valid.
        """
        self.__value = value
        self.__is_valid = is_valid

    def __eq__(self, other) -> bool:
        """
        Check if this object is equal to another object.

        Parameters
        ----------
        other : Any
            Other object to compare.

        Returns
        -------
        bool
            ``True`` if the objects are equal, ``False`` otherwise.
        """
        return (
            isinstance(other, VariableState)
            and self.value == other.value
            and self.is_valid == other.is_valid
        )

    @property
    def value(self) -> IVariableValue:
        """Get the variable value."""
        return self.__value

    @property
    def is_valid(self) -> bool:
        """
        Flag indicating that the object is equal to the other object.

        ``True`` indicates that the objects are equal.
        """
        return self.__is_valid

    @property
    def safe_value(self) -> IVariableValue:
        """
        Variable value.

        ``VariableValueInvalidError`` is raised if the variable value is not valid.
        """
        if self.__is_valid:
            return self.__value
        else:
            raise VariableValueInvalidError()

    def clone(self) -> VariableState:
        """
        Clone the instance.

        The returned instance contains a clone of this instance's value.

        Returns
        -------
        VariableState
            Deep copy of the instance.
        """
        return VariableState(self.__value.clone(), self.__is_valid)
