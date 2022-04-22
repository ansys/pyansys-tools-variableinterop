"""
Ansys Common VariableInterop.

----------------------------

Optional variable and metadata specifications for interoperability between languages and
capabilities.

This library defines some common types and metadata that enable the platform team to provide common
and consistent behavior across platforms, languages, and Ansys capabilities.

Characteristics
---------------

 - Minimal set of formally defined data types
 - Standard base implementation in each supported language that matches the style and intent of
   the given language
 - Follows the standards in TODO: Add reference to standards doc
 - Most common operations defined following specification

   - to/from "API" string (not intended for UI layer, allows data transfer in human readable format
     across products and regions)
   - to/from human display strings
   - to/from binary blocks
   - implicit conversion to/from language primitives for lossless conversions. Explicit conversion
     for lossy conversions

 - Visitor pattern makes it easy and reliable to add and reuse new operations with compile-time
   semantics
 - In trade, adding new datatypes is not easy
 - Most commonly re-used metadata strongly defined. Generic dictionary provided for custom metadata

Examples
--------
TODO: fill in

Project Background
------------------
After 20 years of working on integration problems a holistic review was performed around the
concept of a variable in some legacy codebases. No less than 2 dozen classes that represent a
variable were found. There were many more switch statements where one datatype needed to be
converted to another. This inconsistency brings about the following problems:

 - The behavior of one capability within the product suite does not match that of other
   capabilities - leading to confusion, bugs, and lost time
 - Switch statements are notorious for introducing bugs. People tend to cut-n-paste them, leading
   to subtle maintenance issues as one is modified and the other diverges. There is no compile-time
   type checking.
 - Slight differences datatypes (int32 vs int64) can lead to unexpected bugs, including disastrous
   "bad data with no error" class issues.
 - Seemingly simple tasks like reliably converting to string or byte buffer and back are
   surprisingly hard to do correct in all the edge cases. Worse, even if you get a "correct"
   implementation, if it doesn't match what is used at an API boundary by a different capability
   or product, errors ensue.

The standards and the standard implementations in several languages came out of this review.

"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from ansys.common.variableinterop.utils.implicit_coercion import (
    implicit_coerce,
    implicit_coerce_single,
)
from ansys.common.variableinterop.utils.string_escaping import escape_string, unescape_string

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
from .file_value import EMPTY_FILE, FileValue
from .from_formatted_string_visitor import FromFormattedStringVisitor
from .get_modelcenter_type_for_value import GetModelCenterTypeForValue
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
from .var_type_array_check import var_type_is_array
from .variable_type import VariableType
from .variable_value import CommonArrayValue, IVariableValue
from .vartype_arrays_and_elements import get_element_type, to_array_type
