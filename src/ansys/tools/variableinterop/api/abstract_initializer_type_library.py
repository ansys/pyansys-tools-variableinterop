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

from abc import ABC
from functools import cached_property
from typing import Any, Optional, Type

from ansys.tools.variableinterop.api.exceptions import IncompatibleTypesError
from ansys.tools.variableinterop.api.itype_library import (
    ITypeInformation,
    ITypeLibrary,
    TypesRequired,
)


class AbstractInitializerTypeLibrary(ITypeLibrary, ABC):
    """
    Abstract base class for a type library implementation that uses regular initializers
    to convert types.

    If a type library ensures that all conversions can be made by passing the source data to the
    destination type's initializer, then this ABC will provide a default implementation of
    ``runtime_convert``.

    If the conversion is between two types declared in ``ITypeLibrary.allowed_types``, then
    ``ITypeLibrary.is_linking_allowed()` is used to validate the conversion, then the source
    is passed to the initializer for the destination type.

    If the conversion is between a type declared in ``RequiredTypes`` and the type
    declared by ``ITypeLibrary.getType()`` for the given name, then it is allowed.

    All other conversions are rejected with an ``IncompatibleTypesError``.
    """

    @cached_property
    def type_to_typeinfo(self) -> dict[Type, ITypeInformation]:
        """Map of the value type declared for each ``ITypeLibrary.allowed_types`` to the
        associated ``ITypeInformation``."""
        return {t.value_type: t for (t) in self.allowed_types}

    def runtime_convert(self, source: Any, source_type: Type, dest_type: Type) -> Any:
        # Try to look up the given types in the allowed types
        source_ti: Optional[ITypeInformation] = self.type_to_typeinfo.get(source_type)
        dest_ti: Optional[ITypeInformation] = self.type_to_typeinfo.get(dest_type)

        if source_ti is None or dest_ti is None:
            # If either side is not an allowed_type, look it up the type in the RequiredTypes list
            if source_ti is None:
                source_name: Optional[str] = TypesRequired.get(source_type)
                if source_name is None:
                    raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)
                source_ti = self.get_type(source_name)
            if dest_ti is None:
                dest_name: Optional[str] = TypesRequired.get(dest_type)
                if dest_name is None:
                    raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)
                dest_ti = self.get_type(dest_name)

            # Only allow the conversion if one side is the required type and the other the
            # associated native type.
            if source_ti.canonical_name != dest_ti.canonical_name:
                raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)
        # If both sides are in allowed_type, just test is_linking_allowed
        elif not self.is_linking_allowed(source_ti.canonical_name, dest_ti.canonical_name).allowed:
            raise IncompatibleTypesError(source_type.__name__, dest_type.__name__)

        return dest_type(source)
