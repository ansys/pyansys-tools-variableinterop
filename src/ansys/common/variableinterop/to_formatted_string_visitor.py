"""Definition of IVariableValueVisitor."""
from __future__ import annotations

import locale
from typing import TYPE_CHECKING

import numpy as np

import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

if TYPE_CHECKING:
    import ansys.common.variableinterop.boolean_value as boolean_value
    import ansys.common.variableinterop.integer_value as integer_value
    import ansys.common.variableinterop.real_value as real_value
    import ansys.common.variableinterop.string_value as string_value


class ToFormattedStringVisitor(ivariable_visitor.IVariableValueVisitor[np.str_]):
    """Converts an IVariableValue to a string formatted for a locale."""

    def __init__(self, locale_name: str):
        """Initialize the object."""
        self._locale_name = locale_name

    def __perform_safe_locale_action(self, action) -> np.str_:
        """
        Switches to the correct locale, performs the specified action, \
        and then switches back safely.

        Parameters
        ----------
        action The action to perform.

        Returns
        -------
        The numpy string returned by the action.
        """
        restore_local = locale.getlocale(locale.LC_ALL)
        locale.setlocale(locale.LC_ALL, self._locale_name)
        try:
            result = action()
        finally:
            locale.setlocale(locale.LC_ALL, restore_local)
        return result

    def visit_integer(self, value: integer_value.IntegerValue) -> np.str_:
        """
        Will be called if accept is called on an IntegerValue.

        Parameters
        ----------
        value The IntegerValue being visited.

        Returns
        -------
        The result.
        """
        result: np.str_ = self.__perform_safe_locale_action(
            lambda: locale.format_string("%G", value))
        return result

    def visit_real(self, value: real_value.RealValue) -> np.str_:
        """
        Will be called if accept is called on a RealValue.

        Parameters
        ----------
        value The RealValue being visited.

        Returns
        -------
        The result.
        """
        result: np.str_ = self.__perform_safe_locale_action(
            lambda: locale.format_string("%.15G", value))
        return result

    def visit_boolean(self, value: boolean_value.BooleanValue) -> np.str_:
        """
        Will be called if accept is called on a BooleanValue.

        Parameters
        ----------
        value The BooleanValue being visited.

        Returns
        -------
        The result.
        """
        result: np.str_ = self.__perform_safe_locale_action(
            lambda: locale.format_string("%s", value))
        return result

    def visit_string(self, value: string_value.StringValue) -> np.str_:
        """
        Will be called if accept is called on a StringValue.

        Parameters
        ----------
        value The StringValue being visited.

        Returns
        -------
        The result.
        """
        return value

    # IntegerArray

    # RealArray

    # BooleanArray

    # StringArray
