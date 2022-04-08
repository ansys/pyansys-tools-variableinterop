"""Utilities for dealing with locales."""
import locale
from typing import Any, Callable


class LocaleUtils:
    """
    Contains utilities for dealing with locales.
    """
    @staticmethod
    def perform_safe_locale_action(locale_name: str, action: Callable) -> Any:
        """
        Switches to the correct locale, performs the specified action, \
        and then switches back safely.

        Parameters
        ----------
        action The action to perform.

        Returns
        -------
        The object returned by the action.
        """
        restore_local = locale.getlocale(locale.LC_CTYPE)
        locale.setlocale(locale.LC_ALL, locale_name)
        try:
            result = action()
        finally:
            locale.setlocale(locale.LC_ALL, restore_local)
        return result
