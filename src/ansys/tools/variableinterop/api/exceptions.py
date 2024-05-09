# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

from configparser import ConfigParser
from functools import cached_property
import os


class IncompatibleTypesError(TypeError):
    """Indicates that the types used in a conversion are incompatible."""

    @cached_property
    def _strings(self) -> ConfigParser:
        """Returns a ConfigParser that has read the package strings.properties file."""
        parser = ConfigParser()
        parser.read(os.path.join(os.path.dirname(__file__), "strings.properties"))
        return parser

    def __init__(self, from_type: str, to_type: str) -> None:
        """
        Constructor that builds a default message based on a from and to type as
        strings.

        Parameters
        ----------
        from_type: str
            Name of the type for the source data
        to_type: str
            Name of the type for the destination data
        """
        self.from_type_str = from_type
        self.to_type_str = to_type
        msg = self._strings.get("Errors", "ERROR_INCOMPATIBLE_TYPES").format(from_type, to_type)
        super().__init__(msg)
