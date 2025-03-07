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
"""
This library contains definitions of the basic variables, types, metadata, and values
intended to provide interoperability between all products that optionally choose to
participate.

For high-level project documentation with examples and installation instructions, see
http://variableinterop.docs.pyansys.com.
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("pyansys-tools-variableinterop")
"""ansys.tools.variableinterop version."""

from .api_serialization import from_api_string, to_api_string
from .array_metadata import (
    BooleanArrayMetadata,
    IntegerArrayMetadata,
    RealArrayMetadata,
    StringArrayMetadata,
)
from .array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from .common_variable_metadata import CommonVariableMetadata
from .exceptions import IncompatibleTypesException, ValueDeserializationUnsupportedException
from .file_array_metadata import FileArrayMetadata
from .file_array_value import FileArrayValue
from .file_metadata import FileMetadata
from .file_scope import FileScope
from .file_value import (
    EMPTY_FILE,
    AsyncLocalFileContentContext,
    FileValue,
    LocalFileContentContext,
    LocalFileValue,
)
from .from_formatted_string_visitor import FromFormattedStringVisitor
from .isave_context import ILoadContext, ISaveContext
from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from .ivariable_visitor import IVariableValueVisitor
from .ivariablemetadata_visitor import IVariableMetadataVisitor
from .non_managing_file_scope import NonManagingFileScope
from .numeric_metadata import NumericMetadata
from .scalar_metadata import BooleanMetadata, IntegerMetadata, RealMetadata, StringMetadata
from .scalar_value_conversion import (
    to_boolean_value,
    to_integer_value,
    to_real_value,
    to_string_value,
)
from .scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from .utils.implicit_coercion import implicit_coerce, implicit_coerce_single
from .utils.string_escaping import escape_string, unescape_string
from .var_type_array_check import var_type_is_array
from .variable_state import VariableState
from .variable_type import VariableType
from .variable_value import CommonArrayValue, IVariableValue, VariableValueInvalidError
from .vartype_arrays_and_elements import get_element_type, to_array_type
