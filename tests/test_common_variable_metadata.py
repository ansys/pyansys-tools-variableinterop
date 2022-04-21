"""
Unit tests of the methods on
common_variable_metadata.CommonVariableMetadata.
"""
from typing import List, Tuple, Type, TypeVar

import pytest

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.variable_value import CommonArrayValue

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
        meta_type = acvi.StringArrayMetadata,
        value_type = acvi.StringValue)


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

    # Simple cases
    ("Boolean", acvi.BooleanMetadata(), acvi.BooleanValue(False)),
    # ("File", acvi.FileMetadata(), acvi.FileValue.Empty),
    ("Boolean[]", acvi.BooleanArrayMetadata(), acvi.BooleanArrayValue([])),
    # ("File[]", acvi.FileArrayMetadata(), acvi.FileArrayValue([])),
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
