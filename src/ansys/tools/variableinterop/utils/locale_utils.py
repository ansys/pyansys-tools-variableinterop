# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Provides utilities for dealing with locales."""
from configparser import ConfigParser
import locale
import os
from typing import Any, Callable


class LocaleUtils:
    """Provides utilities for dealing with locales."""

    @staticmethod
    def perform_safe_locale_action(locale_name: str, action: Callable) -> Any:
        """
        Switches to the correct locale, performs the specified action, and then switches
        back safely.

        Parameters
        ----------
        locale_name: str
            Name of the locale to perform the action in.
        action : Callable
            Action to perform.

        Returns
        -------
        Any
            Object returned by the action.
        """
        restore_local = locale.getlocale(locale.LC_CTYPE)
        locale.setlocale(locale.LC_ALL, locale_name)
        try:
            result = action()
        finally:
            locale.setlocale(locale.LC_ALL, restore_local)
        return result


class Strings:
    """Provides utilities for obtaining string resources."""

    @staticmethod
    def get(section: str, name: str, *args: object) -> str:
        """
        Get a localized string from ``strings.properties``.

        Parameters
        ----------
        section : str
            Section of ``strings.properties`` to get the localized string from.
        name : str
            Identifier for the string to get.
        args : object
            Optional formatting arguments.

        Returns
        -------
        str
            Localized string.
        """
        parser = ConfigParser()
        parser.read(os.path.join(os.path.dirname(__file__), "../strings.properties"))
        return parser.get(section, name).format(*args)
