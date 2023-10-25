# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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

"""
Provides a variable type pseudo-visitor that parses values from strings.

The pseudo-visitor is constructed with the string to parse, then accepted by the
appropriate variable type. When visiting, it attempts to parse the string into the
visited type. For more information on why this pattern is better than bare switch
statements, see :class:``IVariableTypePseudoVisitor``.
"""
import json
from typing import Optional

from .array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from .file_array_value import FileArrayValue
from .file_scope import FileScope
from .file_value import FileValue
from .isave_context import ILoadContext
from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor
from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue


class APIStringToValueVisitor(IVariableTypePseudoVisitor):
    """Visits variable type enumeration values, producing a variable value from a
    string."""

    def __init__(
        self,
        source: str,
        fscope: Optional[FileScope] = None,
        save_context: Optional[ILoadContext] = None,
    ):
        """
        Create a new instance of this class.

        Parameters
        ----------
        source : str
            String that values should be parsed from.
        fscope : Optional[FileScope], optional
            File scope to use to deserialize file variables. If file variables are
            not needed, the value may be ``None``, which is the default.
        save_context : Optional[ILoadContext], optional
            Save context to read file contents from. If file variables are
            not needed, the value may be ``None``, which is the default.
        """
        self._source: str = source
        self._scope: Optional[FileScope] = fscope
        self._save_context: Optional[ILoadContext] = save_context

    def visit_unknown(self) -> None:
        """
        Visit the UNKNOWN variable type.

        Given that variables of type Unknown cannot actually be produced,
        this method always raises.

        Returns
        -------
        None
            Never returns; always raises ``NotImplementedError``.

        Raises
        ------
        NotImplementedError
            Always.
        """
        raise NotImplementedError("Cannot create values with unknown type.")

    def visit_int(self) -> IntegerValue:
        """
        Produce an IntegerValue from the API string format.

        Returns
        -------
        IntegerValue
            ``IntegerValue`` with a value determined by the specified string.
        """
        return IntegerValue.from_api_string(self._source)

    def visit_real(self) -> RealValue:
        """
        Produce a RealValue from the API string format.

        Returns
        -------
        RealValue
            ``RealValue`` with a value determined by the specified string.
        """
        return RealValue.from_api_string(self._source)

    def visit_boolean(self) -> BooleanValue:
        """
        Produce a BooleanValue from the API string format.

        Returns
        -------
        BooleanValue
            ``BooleanValue`` with a value determined by the specified string.
        """
        return BooleanValue.from_api_string(self._source)

    def visit_string(self) -> StringValue:
        """
        Produce a StringValue from the API string format.

        Returns
        -------
        StringValue
            ``StringValue`` with a value determined by the specified string.
        """
        return StringValue.from_api_string(self._source)

    def visit_file(self) -> FileValue:
        """
        Produce a ``FileValue`` from the API string format.

        Returns
        -------
        FileValue
            ``FileValue`` with a value determined by the specified string.
        """
        if self._scope is None or self._save_context is None:
            raise NotImplementedError(
                "Deserializing a file value requires a file scope and save context."
            )
        else:
            return self._scope.from_api_object(json.loads(self._source), self._save_context)

    def visit_int_array(self) -> IntegerArrayValue:
        """
        Produce an IntegerArrayValue from the API string format.

        Returns
        -------
        IntegerArrayValue
            ``IntegerArrayValue`` with a value determined by the specified string.
        """
        return IntegerArrayValue.from_api_string(self._source)

    def visit_real_array(self) -> RealArrayValue:
        """
        Produce a RealArrayValue from the API string format.

        Returns
        -------
        RealArrayValue
            ``RealArrayValue`` with a value determined by the specified string.
        """
        return RealArrayValue.from_api_string(self._source)

    def visit_bool_array(self) -> BooleanArrayValue:
        """
        Produce a BooleanArrayValue from the API string format.

        Returns
        -------
        BooleanArrayValue
            ``BooleanArrayValue`` with a value determined by the specified string.
        """
        return BooleanArrayValue.from_api_string(self._source)

    def visit_string_array(self) -> StringArrayValue:
        """
        Produce a StringArrayValue from the API string format.

        Returns
        -------
        StringArrayValue
            ``StringArrayValue`` with a value determined by the specified string.
        """
        return StringArrayValue.from_api_string(self._source)

    def visit_file_array(self) -> FileArrayValue:
        """
        Produce a ``FileArrayValue`` from the API string format.

        Returns
        -------
        FileArrayValue
            ``FileArrayValue`` with a value determined by the specified string.
        """
        if self._scope is None or self._save_context is None:
            raise NotImplementedError(
                "Deserializing a file value requires a file scope and save context."
            )
        else:
            return FileArrayValue.from_api_object(
                json.loads(self._source), self._save_context, self._scope
            )
