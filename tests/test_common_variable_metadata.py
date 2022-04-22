"""
Unit tests of the methods on
common_variable_metadata.CommonVariableMetadata.
"""
from typing import List, Tuple, Type, TypeVar, Union

import pytest

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.variable_value import CommonArrayValue
from tests.test_utils import _create_exception_context


M = TypeVar(
    'M',
    acvi.IntegerMetadata, acvi.RealMetadata, acvi.IntegerArrayMetadata, acvi.RealArrayMetadata)
N = TypeVar('N', int, float)


def get_test_num_meta(
        meta_type: Type[M],
        value_type: Type,
        lower: N = None,
        upper: N = None,
        enums: List[N] = None) -> M:
    """
    Get a test meta_type object with optional lower and/or upper
    #bounds, and optional enumerated values.

    Parameters
    ----------
    meta_type : Type
        The type of the metadata to construct.
    value_type : Type
        The type of the bounds and enums in the meta_type.
    lower : int or float
        Lower bound value to set into constructed metadata.
    upper :
        Upper bound value to set into constructed metadata.
    enums : List[int] or List[float]
        Enumerated values to set into constructed metadata.

    Returns
    -------
    Newly constructed test metadata with the given property values.
    """
    meta = meta_type()
    if lower is not None:
        meta.lower_bound = value_type(lower)
    if upper is not None:
        meta.upper_bound = value_type(upper)
    if enums is not None:
        meta.enumerated_values = list(map(lambda v: value_type(v), enums))
    return meta


def get_test_int_meta(
        lower: int = None,
        upper: int = None,
        enums: List[int] = None) -> acvi.IntegerMetadata:
    """Get a test IntegerMetadata with optional lower and/or upper
    bounds, and optional enumerated values."""
    return get_test_num_meta(acvi.IntegerMetadata, acvi.IntegerValue, lower, upper, enums)


def get_test_real_meta(
        lower: float = None,
        upper: float = None,
        enums: List[float] = None) -> acvi.RealMetadata:
    """Get a test RealMetadata with optional lower and/or upper
    bounds, and optional enumerated values."""
    return get_test_num_meta(acvi.RealMetadata, acvi.RealValue, lower, upper, enums)


def get_test_int_array_meta(
        lower: int = None,
        upper: int = None,
        enums: List[int] = None) -> acvi.IntegerArrayMetadata:
    """Get a test IntegerArrayMetadata with optional lower and/or
    upper bounds, and optional enumerated values."""
    return get_test_num_meta(acvi.IntegerArrayMetadata, acvi.IntegerValue, lower, upper, enums)


def get_test_real_array_meta(
        lower: float = None,
        upper: float = None,
        enums: List[float] = None) -> acvi.RealArrayMetadata:
    """Get a test RealArrayMetadata with optional lower and/or
    upper bounds, and optional enumerated values."""
    return get_test_num_meta(acvi.RealArrayMetadata, acvi.RealValue, lower, upper, enums)


S = TypeVar('S', acvi.StringMetadata, acvi.StringArrayMetadata)


def get_test_str_meta(
        enums: List[str],
        meta_type: Type[S] = acvi.StringMetadata,
        value_type: Type = acvi.StringValue) -> S:
    """
    Get a test StringMetadata with enumerated values.

    Parameters
    ----------
    enums : List[int] or List[float]
        Enumerated values to set into constructed metadata.
    meta_type : Type
        The type of the metadata to construct.
    value_type : Type
        The type of the bounds and enums in the meta_type.

    Returns
    -------
    Newly constructed test metadata with the given property values.
    """
    meta = meta_type()
    meta.enumerated_values = list(map(lambda i: value_type(i), enums))
    return meta


def get_test_str_array_meta(
        enums: List[str]) -> acvi.StringArrayMetadata:
    """Get a test StringArrayMetadata with enumerated values."""
    return get_test_str_meta(
        enums,
        meta_type=acvi.StringArrayMetadata,
        value_type=acvi.StringValue)


get_default_value_tests: List[Tuple[str, acvi.CommonVariableMetadata, acvi.IVariableValue]] = [
    # IntegerMetadata to IntegerValue
    # no restriction, use default
    ("Integer default", acvi.IntegerMetadata(), acvi.IntegerValue(0)),
    # default not allowed by lower bound, use lower bound
    ("Integer to lower", get_test_int_meta(lower=5), acvi.IntegerValue(5)),
    # default allowed by lower bound, use default
    ("Integer not to lower", get_test_int_meta(lower=-5), acvi.IntegerValue(0)),
    # default not allowed by upper bound, use upper bound
    ("Integer to upper", get_test_int_meta(upper=-5), acvi.IntegerValue(-5)),
    # default allowed by upper bound, use default
    ("Integer not to upper", get_test_int_meta(upper=5), acvi.IntegerValue(0)),
    # default in enum values, use default
    ("Integer in enum", get_test_int_meta(enums=[5, 0, -4, 9]), acvi.IntegerValue(0)),
    # default not in enum values, use first enum value
    ("Integer not in enum", get_test_int_meta(enums=[5, -4, 9]), acvi.IntegerValue(5)),
    (
        "Integer lower & enum",
        get_test_int_meta(lower=1, enums=[-5, -3, -1, 1, 3, 5]),
        acvi.IntegerValue(1)
    ),
    (
        "Integer lower & enum with default",
        get_test_int_meta(lower=1, enums=[-5, -3, -1, 0, 1, 3, 5]),
        acvi.IntegerValue(1)
    ),
    (
        "Integer lower & enum including default",
        get_test_int_meta(lower=-1, enums=[-5, -3, -1, 0, 1, 3, 5]),
        acvi.IntegerValue(0)
    ),
    (
        "Integer lower & enum w/o default",
        get_test_int_meta(lower=-1, enums=[-5, -3, -1, 1, 3, 5]),
        acvi.IntegerValue(-1)
    ),
    (
        "Integer upper & enum",
        get_test_int_meta(upper=-1, enums=[-5, -3, -1, 1, 3, 5]),
        acvi.IntegerValue(-5)
    ),
    (
        "Integer upper & enum with default",
        get_test_int_meta(upper=-1, enums=[-5, -3, -1, 0, 1, 3, 5]),
        acvi.IntegerValue(-5)
    ),
    (
        "Integer upper & enum including default",
        get_test_int_meta(upper=1, enums=[-5, -3, -1, 0, 1, 3, 5]),
        acvi.IntegerValue(0)
    ),
    (
        "Integer upper & enum w/o default",
        get_test_int_meta(upper=1, enums=[-5, -3, -1, 1, 3, 5]),
        acvi.IntegerValue(-5)
    ),

    # RealMetadata to RealValue
    # no restriction, use default
    ("Real default", acvi.RealMetadata(), acvi.RealValue(0.0)),
    # default not allowed by lower bound, use lower bound
    ("Real to lower", get_test_real_meta(lower=5.0), acvi.RealValue(5.0)),
    # default allowed by lower bound, use default
    ("Real not to lower", get_test_real_meta(lower=-5.0), acvi.RealValue(0.0)),
    # default not allowed by upper bound, use upper bound
    ("Real to upper", get_test_real_meta(upper=-5.0), acvi.RealValue(-5.0)),
    # default allowed by upper bound, use default
    ("Real not to upper", get_test_real_meta(upper=5.0), acvi.RealValue(0.0)),
    # default in enum values, use default
    ("Real in enum", get_test_real_meta(enums=[5.0, 0.0, -4.0, 9.0]), acvi.RealValue(0.0)),
    # default not in enum values, use first enum value
    ("Real not in enum", get_test_real_meta(enums=[5.0, -4.0, 9.0]), acvi.RealValue(5.0)),
    (
        "Real lower & enum",
        get_test_real_meta(lower=1.0, enums=[-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(1.0)
    ),
    (
        "Real lower & enum with default",
        get_test_real_meta(lower=1.0, enums=[-5.0, -3.0, -1.0, 0.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(1.0)
    ),
    (
        "Real lower & enum including default",
        get_test_real_meta(lower=-1.0, enums=[-5.0, -3.0, -1.0, 0.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(0.0)
    ),
    (
        "Real lower & enum w/o default",
        get_test_real_meta(lower=-1.0, enums=[-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(-1.0)
    ),
    (
        "Real upper & enum",
        get_test_real_meta(upper=-1.0, enums=[-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(-5.0)
    ),
    (
        "Real upper & enum with default",
        get_test_real_meta(upper=-1.0, enums=[-5.0, -3.0, -1.0, 0.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(-5.0)
    ),
    (
        "Real upper & enum including default",
        get_test_real_meta(upper=1.0, enums=[-5.0, -3.0, -1.0, 0.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(0.0)
    ),
    (
        "Real upper & enum w/o default",
        get_test_real_meta(upper=1.0, enums=[-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]),
        acvi.RealValue(-5.0)
    ),

    # StringMetadata to StringValue
    # no restriction, use default
    ("String default", acvi.StringMetadata(), acvi.StringValue("")),
    # default in enum values, use default
    ("String in enum", get_test_str_meta(["1st", "", "3rd", "last"]), acvi.StringValue("")),
    # default not in enum values, use first enum value
    ("String not in enum", get_test_str_meta(["1st", "2nd", "last"]), acvi.StringValue("1st")),

    # Other types, metadata has no effect, always get default

    # Simple cases
    ("Boolean", acvi.BooleanMetadata(), acvi.BooleanValue(False)),
    ("File", acvi.FileMetadata(), acvi.EMPTY_FILE),

    # IntegerArrayMetadata to IntegerArray
    ("Integer[]", acvi.IntegerArrayMetadata(), acvi.IntegerArrayValue([])),
    # not effected by bounds or enum
    ("Integer[] w/ lower", get_test_int_array_meta(lower=5), acvi.IntegerArrayValue([])),
    ("Integer[] w/ upper", get_test_int_array_meta(upper=-5), acvi.IntegerArrayValue([])),
    ("Integer[] w/ enums", get_test_int_array_meta(enums=[5, -4, 9]), acvi.IntegerArrayValue([])),

    # RealArrayMetadata to RealArray
    ("Real[]", acvi.RealArrayMetadata(), acvi.RealArrayValue([])),
    # not effected by bounds or enum
    ("Real[] w/ lower", get_test_real_array_meta(lower=5.0), acvi.RealArrayValue([])),
    ("Real[] w/ upper", get_test_real_array_meta(upper=-5.0), acvi.RealArrayValue([])),
    ("Real[] w/ enums", get_test_real_array_meta(enums=[5.0, -4.0, 9.0]), acvi.RealArrayValue([])),

    # StringArrayMetadata to StringArray
    ("String[]", acvi.StringArrayMetadata(), acvi.StringArrayValue([])),
    # not effected by enum
    ("String[]", get_test_str_array_meta(["1st", "2nd", "last"]), acvi.StringArrayValue([])),

    # Simple array cases
    ("Boolean[]", acvi.BooleanArrayMetadata(), acvi.BooleanArrayValue([])),
    ("File[]", acvi.FileArrayMetadata(), acvi.FileArrayValue([])),
]
"""List of test cases for meta.get_default_values. Each entry is a tuple
containing in order:
* identifier: a string to aid in identifying a unit test.
* source: a test metadata object to call get_default_values on.
* expected: the expected return value from get_default_values call."""


@pytest.mark.parametrize("_,source,expected", get_default_value_tests)
def test_meta_get_default_value(
        _: str, source: acvi.CommonVariableMetadata, expected: acvi.IVariableValue) -> None:
    """
    Tests the CommonVariableMetadata.get_default_value() on all child
    types of CommonVariableMetadata.

    Parameters
    ----------
    _ : str
        A string to aid in identifying the unit test
    source : CommonVariableMetadata
        Source value to test
    expected : IVariableValue
        Expected results from get_default_value()
    """
    # SUT
    result = source.get_default_value()

    # Verify
    assert type(result) == type(expected)
    if isinstance(result, CommonArrayValue):
        # to avoid an issue with default constructed numpy arrays not being equal to each other
        assert len(result.shape) == 0
    else:
        assert result == expected


def get_test_bool_array(vals: List[bool]) -> acvi.BooleanArrayValue:
    test = acvi.BooleanArrayValue(len(vals))
    for i in range(0, len(vals)):
        test[i] = vals[i]
    return test


def get_test_int_array(vals: List[int]) -> acvi.IntegerArrayValue:
    return acvi.IntegerArrayValue(values=vals)


def get_test_real_array(vals: List[float]) -> acvi.RealArrayValue:
    return acvi.RealArrayValue(values=vals)


def get_test_str_array(vals: List[str]) -> acvi.StringArrayValue:
    return acvi.StringArrayValue(values=vals)


def get_test_file_array(vals: List[acvi.FileValue]) -> acvi.FileArrayValue:
    return acvi.FileArrayValue(values=vals)


runtime_convert_tests = [
    # Boolean to ...
    ["bool -> bool",
     acvi.BooleanMetadata(), acvi.BooleanValue(True), acvi.BooleanValue(True)],
    ["bool -> int",
     acvi.IntegerMetadata(), acvi.BooleanValue(True), acvi.IntegerValue(1)],
    ["bool -> real",
     acvi.RealMetadata(), acvi.BooleanValue(True), acvi.RealValue(1.0)],
    ["bool -> str",
     acvi.StringMetadata(), acvi.BooleanValue(True), acvi.StringValue("True")],
    ["bool -> file",
     acvi.FileMetadata(), acvi.BooleanValue(True), acvi.IncompatibleTypesException],
    ["bool -> bool[]",
     acvi.BooleanArrayMetadata(), acvi.BooleanValue(True), acvi.IncompatibleTypesException],
    ["bool -> int[]",
     acvi.IntegerArrayMetadata(), acvi.BooleanValue(True), acvi.IncompatibleTypesException],
    ["bool -> real[]",
     acvi.RealArrayMetadata(), acvi.BooleanValue(True), acvi.IncompatibleTypesException],
    ["bool -> str[]",
     acvi.StringArrayMetadata(), acvi.BooleanValue(True), acvi.IncompatibleTypesException],
    ["bool -> file[]",
     acvi.FileArrayMetadata(), acvi.BooleanValue(True), acvi.IncompatibleTypesException],

    # Integer to ...
    ["int -> bool",
     acvi.BooleanMetadata(), acvi.IntegerValue(42), acvi.BooleanValue(True)],
    ["int -> int",
     acvi.IntegerMetadata(), acvi.IntegerValue(42), acvi.IntegerValue(42)],
    ["int -> real",
     acvi.RealMetadata(), acvi.IntegerValue(42), acvi.RealValue(42.0)],
    ["int -> str",
     acvi.StringMetadata(), acvi.IntegerValue(42), acvi.StringValue("42")],
    ["int -> file",
     acvi.FileMetadata(), acvi.IntegerValue(42), acvi.IncompatibleTypesException],
    ["int -> bool[]",
     acvi.BooleanArrayMetadata(), acvi.IntegerValue(42), acvi.IncompatibleTypesException],
    ["int -> int[]",
     acvi.IntegerArrayMetadata(), acvi.IntegerValue(42), acvi.IncompatibleTypesException],
    ["int -> real[]",
     acvi.RealArrayMetadata(), acvi.IntegerValue(42), acvi.IncompatibleTypesException],
    ["int -> str[]",
     acvi.StringArrayMetadata(), acvi.IntegerValue(42), acvi.IncompatibleTypesException],
    ["int -> file[]",
     acvi.FileArrayMetadata(), acvi.IntegerValue(42), acvi.IncompatibleTypesException],

    # Real to ...
    ["real -> bool",
     acvi.BooleanMetadata(), acvi.RealValue(42.3), acvi.BooleanValue(True)],
    ["real -> int",
     acvi.IntegerMetadata(), acvi.RealValue(42.3), acvi.IntegerValue(42)],
    ["real -> real",
     acvi.RealMetadata(), acvi.RealValue(42.3), acvi.RealValue(42.3)],
    ["real -> str",
     acvi.StringMetadata(), acvi.RealValue(42.3), acvi.StringValue("42.3")],
    ["real -> file",
     acvi.FileMetadata(), acvi.RealValue(42.3), acvi.IncompatibleTypesException],
    ["real -> bool[]",
     acvi.BooleanArrayMetadata(), acvi.RealValue(42.3), acvi.IncompatibleTypesException],
    ["real -> int[]",
     acvi.IntegerArrayMetadata(), acvi.RealValue(42.3), acvi.IncompatibleTypesException],
    ["real -> real[]",
     acvi.RealArrayMetadata(), acvi.RealValue(42.3), acvi.IncompatibleTypesException],
    ["real -> str[]",
     acvi.StringArrayMetadata(), acvi.RealValue(42.3), acvi.IncompatibleTypesException],
    ["real -> file[]",
     acvi.FileArrayMetadata(), acvi.RealValue(42.3), acvi.IncompatibleTypesException],

    # String to ...
    ["str -> bool",
     acvi.BooleanMetadata(), acvi.StringValue("True"), acvi.BooleanValue(True)],
    ["str -> int",
     acvi.IntegerMetadata(), acvi.StringValue("42"), acvi.IntegerValue(42)],
    ["str -> real",
     acvi.RealMetadata(), acvi.StringValue("42.3"), acvi.RealValue(42.3)],
    ["str -> str",
     acvi.StringMetadata(), acvi.StringValue("Something"), acvi.StringValue("Something")],
    ["str -> file",
     acvi.FileMetadata(), acvi.StringValue("Something"), acvi.IncompatibleTypesException],
    ["str -> bool[]",
     acvi.BooleanArrayMetadata(), acvi.StringValue("Something"), acvi.IncompatibleTypesException],
    ["str -> int[]",
     acvi.IntegerArrayMetadata(), acvi.StringValue("Something"), acvi.IncompatibleTypesException],
    ["str -> real[]",
     acvi.RealArrayMetadata(), acvi.StringValue("Something"), acvi.IncompatibleTypesException],
    ["str -> str[]",
     acvi.StringArrayMetadata(), acvi.StringValue("Something"), acvi.IncompatibleTypesException],
    ["str -> file[]",
     acvi.FileArrayMetadata(), acvi.StringValue("Something"), acvi.IncompatibleTypesException],

    # File to ...
    ["file -> bool",
     acvi.BooleanMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> int",
     acvi.IntegerMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> real",
     acvi.RealMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> str",
     acvi.StringMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> file",
     acvi.FileMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> bool[]",
     acvi.BooleanArrayMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> int[]",
     acvi.IntegerArrayMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> real[]",
     acvi.RealArrayMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> str[]",
     acvi.StringArrayMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],
    ["file -> file[]",
     acvi.FileArrayMetadata(), acvi.EMPTY_FILE, acvi.IncompatibleTypesException],

    # Boolean Array to ...
    [
        "bool[] -> bool",
        acvi.BooleanMetadata(),
        get_test_bool_array([True, False, True]),
        acvi.IncompatibleTypesException
    ],
    [
        "bool[] -> int",
        acvi.IntegerMetadata(),
        get_test_bool_array([True, False, True]),
        acvi.IncompatibleTypesException
    ],
    [
        "bool[] -> real",
        acvi.RealMetadata(),
        get_test_bool_array([True, False, True]),
        acvi.IncompatibleTypesException
    ],
    [
        "bool[] -> str",
        acvi.StringMetadata(),
        get_test_bool_array([True, False, True]),
        acvi.StringValue("True,False,True")
    ],
    [
        "bool[] -> file",
        acvi.FileMetadata(),
        get_test_bool_array([True, False, True]),
        acvi.IncompatibleTypesException
    ],
    [
        "bool[] -> bool[]",
        acvi.BooleanArrayMetadata(),
        get_test_bool_array([True, False, True]),
        get_test_bool_array([True, False, True])
    ],
    [
        "bool[] -> int[]",
        acvi.IntegerArrayMetadata(),
        get_test_bool_array([True, False, True]),
        get_test_int_array([1, 0, 1])
    ],
    [
        "bool[] -> real[]",
        acvi.RealArrayMetadata(),
        get_test_bool_array([True, False, True]),
        get_test_real_array([1.0, 0.0, 1.0])
    ],
    [
        "bool[] -> str[]",
        acvi.StringArrayMetadata(),
        get_test_bool_array([True, False, True]),
        get_test_str_array(["True", "False", "True"])
    ],
    [
        "bool[] -> file[]",
        acvi.FileArrayMetadata(),
        get_test_bool_array([True, False, True]),
        acvi.IncompatibleTypesException
    ],

    # Integer Array to ...
    [
        "int[] -> bool",
        acvi.BooleanMetadata(),
        get_test_int_array([5, 4, 0]),
        acvi.IncompatibleTypesException
    ],
    [
        "int[] -> int",
        acvi.IntegerMetadata(),
        get_test_int_array([5, 4, 0]),
        acvi.IncompatibleTypesException
    ],
    [
        "int[] -> real",
        acvi.RealMetadata(),
        get_test_int_array([5, 4, 0]),
        acvi.IncompatibleTypesException
    ],
    [
        "int[] -> str",
        acvi.StringMetadata(),
        get_test_int_array([5, 4, 0]),
        acvi.StringValue("5,4,0")
    ],
    [
        "int[] -> file",
        acvi.FileMetadata(),
        get_test_int_array([5, 4, 0]),
        acvi.IncompatibleTypesException
    ],
    [
        "int[] -> bool[]",
        acvi.BooleanArrayMetadata(),
        get_test_int_array([5, 4, 0]),
        get_test_bool_array([True, True, False])
    ],
    [
        "int[] -> int[]",
        acvi.IntegerArrayMetadata(),
        get_test_int_array([5, 4, 0]),
        get_test_int_array([5, 4, 0])
    ],
    [
        "int[] -> real[]",
        acvi.RealArrayMetadata(),
        get_test_int_array([5, 4, 0]),
        get_test_real_array([5.0, 4.0, 0.0])
    ],
    [
        "int[] -> str[]",
        acvi.StringArrayMetadata(),
        get_test_int_array([5, 4, 0]),
        get_test_str_array(["5", "4", "0"])
    ],
    [
        "int[] -> file[]",
        acvi.FileArrayMetadata(),
        get_test_int_array([5, 4, 0]),
        acvi.IncompatibleTypesException
    ],

    # Real Array to ...
    [
        "real[] -> bool",
        acvi.BooleanMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        acvi.IncompatibleTypesException
    ],
    [
        "real[] -> int",
        acvi.IntegerMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        acvi.IncompatibleTypesException
    ],
    [
        "real[] -> real",
        acvi.RealMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        acvi.IncompatibleTypesException
    ],
    [
        "real[] -> str",
        acvi.StringMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        acvi.StringValue("0.5,4.0,0.0")
    ],
    [
        "real[] -> file",
        acvi.FileMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        acvi.IncompatibleTypesException
    ],
    [
        "real[] -> bool[]",
        acvi.BooleanArrayMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        get_test_bool_array([True, True, False])],
    [
        "real[] -> int[]",
        acvi.IntegerArrayMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        get_test_int_array([1, 4, 0])],
    [
        "real[] -> real[]",
        acvi.RealArrayMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        get_test_real_array([0.5, 4.0, 0.0])],
    [
        "real[] -> str[]",
        acvi.StringArrayMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        get_test_str_array(["0.5", "4.0", "0.0"])],
    [
        "real[] -> file[]",
        acvi.FileArrayMetadata(),
        get_test_real_array([0.5, 4.0, 0.0]),
        acvi.IncompatibleTypesException],

    # String Array to ...
    [
        "str[] -> bool",
        acvi.BooleanMetadata(),
        get_test_str_array(["True", "False", "True"]),
        acvi.IncompatibleTypesException],
    [
        "str[] -> int",
        acvi.IntegerMetadata(),
        get_test_str_array(["5", "4", "0"]),
        acvi.IncompatibleTypesException],
    [
        "str[] -> real",
        acvi.RealMetadata(),
        get_test_str_array(["0.5", "4.0", "0.0"]),
        acvi.IncompatibleTypesException],
    [
        "str[] -> str",
        acvi.StringMetadata(),
        get_test_str_array(["1st", "2nd", "3rd"]),
        acvi.StringValue('"1st","2nd","3rd"')],
    [
        "str[] -> file",
        acvi.FileMetadata(),
        get_test_str_array(["1st", "2nd", "3rd"]),
        acvi.IncompatibleTypesException],
    [
        "str[] -> bool[]",
        acvi.BooleanArrayMetadata(),
        get_test_str_array(["True", "False", "True"]),
        get_test_bool_array([True, False, True])],
    [
        "str[] -> int[]",
        acvi.IntegerArrayMetadata(),
        get_test_str_array(["5", "4", "0"]),
        get_test_int_array([5, 4, 0])],
    [
        "str[] -> real[]",
        acvi.RealArrayMetadata(),
        get_test_str_array(["0.5", "4.0", "0.0"]),
        get_test_real_array([0.5, 4.0, 0.0])],
    [
        "str[] -> str[]",
        acvi.StringArrayMetadata(),
        get_test_str_array(["1st", "2nd", "3rd"]),
        get_test_str_array(["1st", "2nd", "3rd"])],
    [
        "str[] -> file[]",
        acvi.FileArrayMetadata(),
        get_test_str_array(["1st", "2nd", "3rd"]),
        acvi.IncompatibleTypesException
    ],

    # File Array to ...
    [
        "file[] -> bool",
        acvi.BooleanMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> int",
        acvi.IntegerMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> real",
        acvi.RealMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> str",
        acvi.StringMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> file",
        acvi.FileMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> bool[]",
        acvi.BooleanArrayMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> int[]",
        acvi.IntegerArrayMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> real[]",
        acvi.RealArrayMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> str[]",
        acvi.StringArrayMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
    [
        "file[] -> file[]",
        acvi.FileArrayMetadata(),
        get_test_file_array([acvi.EMPTY_FILE, acvi.EMPTY_FILE]),
        acvi.IncompatibleTypesException
    ],
]


@pytest.mark.parametrize("_,meta,source,expected", runtime_convert_tests)
def test_runtime_convert(
        _: str,
        meta: acvi.CommonVariableMetadata,
        source: acvi.IVariableValue,
        expected: Union[acvi.IVariableValue, Type[BaseException]]) -> None:
    # Setup
    if isinstance(expected, acvi.IVariableValue):
        expected_exception = None
        expected_value = expected
    else:
        expected_exception = expected
        expected_value = None
    with _create_exception_context(expected_exception):

        # SUT
        result = meta.runtime_convert(source)

        # Verify
        assert type(result) == type(expected)
        assert result == expected_value
