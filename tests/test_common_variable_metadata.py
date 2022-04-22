"""
Unit tests of the methods on
common_variable_metadata.CommonVariableMetadata.
"""
from typing import List, Tuple, Type, TypeVar, Union

import pytest

import ansys.common.variableinterop as acvi
from ansys.common.variableinterop.variable_value import CommonArrayValue
from tests.test_utils import _create_exception_context


def get_test_bool_array( vals: List[bool]) -> acvi.BooleanArrayValue:
    test = acvi.BooleanArrayValue(len(vals))
    for i in range(0, len(vals)):
        test[i] = vals[i]
    return test


def get_test_int_array( vals: List[int]) -> acvi.IntegerArrayValue:
    return acvi.IntegerArrayValue(values=vals)
#    test = acvi.IntegerArrayValue(len(vals))
#    for i in range(0, len(vals)):
#        test[i] = vals[i]
#    return test


def get_test_real_array( vals: List[float]) -> acvi.RealArrayValue:
    return acvi.RealArrayValue(values=vals)
#    test = acvi.RealArrayValue(len(vals))
#    for i in range(0, len(vals)):
#        test[i] = vals[i]
#    return test


def get_test_str_array(vals: List[str]) -> acvi.StringArrayValue:
    return acvi.StringArrayValue(values=vals)


def get_test_file_array(vals: List[acvi.FileValue]) -> acvi.FileArrayValue:
    return acvi.FileArrayValue(values=vals)
#    test = acvi.FileArrayValue(len(vals))
#    for i in range(0, len(vals)):
#        test[i] = vals[i]
#    return test


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
        acvi.FileMetadata(),get_test_str_array(["1st", "2nd", "3rd"]),
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

@pytest.mark.parametrize( "_,meta,source,expected", runtime_convert_tests)
def test_runtime_convert(
        _: str,
        meta : acvi.CommonVariableMetadata,
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
