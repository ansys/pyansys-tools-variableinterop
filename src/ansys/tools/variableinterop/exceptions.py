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
"""Provides custom exception types."""


from .utils.locale_utils import Strings


class FormatException(BaseException):
    """Indicates that the string used to create a variable value was incorrectly
    formatted."""

    def __init__(self):
        """Construct exception."""
        message: str = Strings.get("Errors", "ERROR_FORMAT")
        super().__init__(message)


class ValueDeserializationUnsupportedException(Exception):
    """Indicates that deserializing a value is not allowed."""

    def __init__(self, message: str):
        """Construct a new instance."""
        super().__init__(message)


class VariableTypeUnknownError(Exception):
    """Indicates that `VariableType.UNKNOWN` was used when a type was needed."""
