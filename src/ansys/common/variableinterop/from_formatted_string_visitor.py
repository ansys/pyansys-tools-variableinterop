"""Definition of FromFormattedStringVisitor."""
from __future__ import annotations

import distutils.util
import locale

import numpy as np

import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.ivariable_type_pseudovisitor as pseudo_visitor
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.variable_value as variable_value


class FromFormattedStringVisitor(pseudo_visitor.IVariableTypePseudoVisitor[
                                     variable_value.IVariableValue]):
    """Converts a string formatted for a locale to a IVariableValue."""

    def __init__(self, value: np.str_, locale_name: str):
        """Initialize the object."""
        self._value = value
        self._locale_name = locale_name

    def __perform_safe_locale_action(self, action) -> variable_value.IVariableValue:
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

    def visit_unknown(self) -> variable_value.IVariableValue:
        pass

    def visit_int(self) -> integer_value.IntegerValue:
        # We need to use atof and then convert to int, as atoi does not support scientific notation
        result: variable_value.IVariableValue = self.__perform_safe_locale_action(
            lambda: np.int64(locale.atof(self._value)))
        return result

    def visit_real(self) -> real_value.RealValue:
        result: np.str_ = self.__perform_safe_locale_action(
            lambda: locale.atof(self._value))
        return result

    def visit_boolean(self) -> boolean_value.BooleanValue:
        result: np.str_ = self.__perform_safe_locale_action(
            lambda: bool(distutils.util.strtobool(self._value)))
        return result

    def visit_string(self) -> string_value.StringValue:
        return self._value

    def visit_file(self) -> variable_value.IVariableValue:
        pass

    def visit_int_array(self) -> variable_value.IVariableValue:
        pass

    def visit_real_array(self) -> variable_value.IVariableValue:
        pass

    def visit_bool_array(self) -> variable_value.IVariableValue:
        pass

    def visit_string_array(self) -> variable_value.IVariableValue:
        pass

    def visit_file_array(self) -> variable_value.IVariableValue:
        pass
