"""
Ansys Common VariableInterop
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

from .boolean_array_metadata import BooleanArrayMetadata
from .boolean_array_value import BooleanArrayValue
from .boolean_metadata import BooleanMetadata
from .boolean_value import BooleanValue
from .coercion import implicit_coerce, implicit_coerce_single
from .common_variable_metadata import CommonVariableMetadata
from .integer_array_metadata import IntegerArrayMetadata
from .integer_array_value import IntegerArrayValue
from .integer_metadata import IntegerMetadata
from .integer_value import IntegerValue
from .ivariable_type_pseudovisitor import IVariableTypePseudoVisitor, vartype_accept
from .ivariable_visitor import IVariableValueVisitor
from .ivariablemetadata_visitor import IVariableMetadataVisitor
from .numeric_metadata import NumericMetadata
from .real_array_metadata import RealArrayMetadata
from .real_array_value import RealArrayValue
from .real_metadata import RealMetadata
from .real_value import RealValue
from .string_array_metadata import StringArrayMetadata
from .string_array_value import StringArrayValue
from .string_metadata import StringMetadata
from .string_value import StringValue
from .value_from_api_string import from_api_string
from .variable_type import VariableType
from .variable_value import IVariableValue

# TODO: Get rid of star
