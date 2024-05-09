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

from typing import Optional, Set, Type

from ansys.tools.variableinterop.api import (
    DEST_TYPE,
    METADATA_TYPE,
    SOURCE_TYPE,
    AbstractInitializerTypeLibrary,
    ITypeInformation,
    TypeCompatibility,
)

from .linking_rules import is_linking_allowed
from .variable_factory import VariableFactory
from .variable_type import VariableType


class UnifiedTypeLibrary(AbstractInitializerTypeLibrary):
    def __init__(self):
        self._types: Set[ITypeInformation] = set(
            UnifiedTypeLibrary._TypeAdapter(t) for t in VariableType if t != VariableType.UNKNOWN
        )

    @property
    def type_library_identifier(self) -> str:
        return "http://defs.ansys.com/typeLibrary/uniform"

    class _TypeAdapter(ITypeInformation):
        def __init__(self, type: VariableType) -> None:
            self.variable_type: VariableType = type

        @property
        def canonical_name(self) -> str:
            "Canonical name of the type"
            return (
                self.variable_type.to_display_string()
            )  # TODO: A display string is not what is wanted here.

        @property
        def aliases(self) -> Set[str]:
            """Set of aliases for the type."""
            raise NotImplementedError

        @property
        def type_description(self) -> str:
            """Detailed description of the type."""
            raise NotImplementedError

        def get_ui_display_name(self, locale: str) -> str:
            """Detailed description of the type."""
            raise NotImplementedError

        @property
        def value_type(self) -> Type:
            """The Python type used for values of this type."""
            return VariableFactory.associated_type(self.variable_type)

        @property
        def metadata_type(self) -> Type:
            """The Python type used for metadata of this type."""
            raise NotImplementedError

    @property
    def allowed_types(self) -> Set[ITypeInformation]:
        return self._types

    def get_type(self, type_name: str) -> ITypeInformation:
        return UnifiedTypeLibrary._TypeAdapter(VariableFactory.from_string(type_name))

    def is_linking_allowed(self, source_type: str, dest_type: str) -> TypeCompatibility:
        source_vt: VariableType = VariableFactory.from_string(source_type)
        dest_vt: VariableType = VariableFactory.from_string(dest_type)
        return is_linking_allowed(source_vt, dest_vt)

    def compute_safe_default_value(self, metadata: METADATA_TYPE) -> Optional[DEST_TYPE]:
        raise NotImplementedError

    def value_to_byte_array(self, source: SOURCE_TYPE, source_type: str) -> bytes:
        raise NotImplementedError

    def byte_array_to_value(self, dest_type: str, source: bytes) -> DEST_TYPE:
        raise NotImplementedError

    def metadata_to_byte_array(self, source: SOURCE_TYPE) -> bytes:
        raise NotImplementedError

    def byte_array_to_metadata(self, dest_type: str, source: bytes) -> DEST_TYPE:
        raise NotImplementedError
