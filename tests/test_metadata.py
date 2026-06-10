# Copyright (C) 2024 - 2026 ANSYS, Inc. and/or its affiliates.
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

from typing import Any

import pytest

from ansys.tools.variableinterop.array_metadata import (
    BooleanArrayMetadata,
    IntegerArrayMetadata,
    RealArrayMetadata,
    StringArrayMetadata,
)
from ansys.tools.variableinterop.file_array_metadata import FileArrayMetadata
from ansys.tools.variableinterop.file_metadata import FileMetadata
from ansys.tools.variableinterop.scalar_metadata import (
    BooleanMetadata,
    IntegerMetadata,
    RealMetadata,
    StringMetadata,
)
from ansys.tools.variableinterop.scalar_values import (
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)

non_numeric_metadata_types = [
    BooleanMetadata.__name__,
    BooleanArrayMetadata.__name__,
    StringMetadata.__name__,
    StringArrayMetadata.__name__,
    FileMetadata.__name__,
    FileArrayMetadata.__name__,
]
"""Names of all non-numeric metadata types."""


numeric_metadata_types = [
    IntegerMetadata.__name__,
    IntegerArrayMetadata.__name__,
    RealMetadata.__name__,
    RealArrayMetadata.__name__,
]
"""Names of all numeric metadata types."""


all_metadata_types = [*numeric_metadata_types, *non_numeric_metadata_types]
"""Names of all metadata types."""


non_numeric_metadata_json_names = [
    "Boolean",
    "BooleanArray",
    "String",
    "StringArray",
    "File",
    "FileArray",
]
"""Names of all non-numeric metadata types when translated to JSON."""


numeric_metadata_json_names = [
    "Integer",
    "IntegerArray",
    "Double",
    "DoubleArray",
]
"""Names of all numeric metadata types when translated to JSON."""


all_metadata_json_names = [*numeric_metadata_json_names, *non_numeric_metadata_json_names]
"""Names of all metadata types when translated to JSON."""


numeric_metadata_enumeration_types = [IntegerValue, IntegerValue, RealValue, RealValue]
"""Scalar types used by all numeric metadata types in enumerated values."""


def assert_equals(metadata1, metadata2) -> None:
    """
    Tests whether passed metadata objects are equal using __eq__ and __ne__ operators
    and specifying each object both, as lhs and rhs operand.

    Parameters
    ----------
    metadata1 First metadata object to compare.
    metadata1 Second metadata object to compare.

    Returns
    -------
    None
    """
    assert metadata1 is not metadata2
    assert metadata1.equals(metadata2)
    assert metadata2.equals(metadata1)
    assert metadata1 == metadata2
    assert metadata2 == metadata1
    assert not metadata1 != metadata2
    assert not metadata2 != metadata1


def assert_are_not_equal(metadata1, metadata2) -> None:
    """
    Tests whether passed metadata objects are not equal using __eq__ and __ne__
    operators and specifying each object both, as lhs and rhs operand.

    Parameters
    ----------
    metadata1 First metadata object to compare.
    metadata1 Second metadata object to compare.

    Returns
    -------
    None
    """
    assert metadata1 is not metadata2
    assert not metadata1.equals(metadata2)
    assert not metadata2.equals(metadata1)
    assert not metadata1 == metadata2
    assert not metadata2 == metadata1
    assert metadata1 != metadata2
    assert metadata2 != metadata1


@pytest.mark.parametrize("type_name", all_metadata_types)
def test_equals_empty(type_name: str) -> None:
    """
    Tests whether empty metadata objects of the same type are equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata2 = metadata_type()
    assert_equals(metadata1, metadata2)


def test_different_metadata_types_are_not_equal() -> None:
    """
    Tests whether empty metadata objects of different type are not equal.

    Returns
    -------
    None
    """
    metadata1 = IntegerMetadata()
    metadata2 = RealMetadata()
    assert_are_not_equal(metadata1, metadata2)


@pytest.mark.parametrize("type_name", all_metadata_types)
def test_equals_same_description(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having the same description are
    equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.description = "Some description: ćma na łące patrzy na słońce."
    metadata2 = metadata_type()
    metadata2.description = "Some description: ćma na łące patrzy na słońce."
    assert_equals(metadata1, metadata2)


@pytest.mark.parametrize("type_name", all_metadata_types)
def test_equals_different_description(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having different descriptions
    are not equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.description = "Some description: ćma na łące patrzy na słońce."
    metadata2 = metadata_type()
    metadata2.description = "Some description: ćma na lace patrzy na słońce."
    assert metadata1 is not metadata2
    assert_are_not_equal(metadata1, metadata2)


@pytest.mark.parametrize("type_name", all_metadata_types)
def test_equals_same_custom_metadata(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having the same custom_metadata
    are equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.custom_metadata["key1"] = BooleanValue(1)
    metadata1.custom_metadata["key2"] = BooleanValue(0)
    metadata2 = metadata_type()
    metadata2.custom_metadata["key2"] = BooleanValue(0)
    metadata2.custom_metadata["key1"] = BooleanValue(1)
    assert_equals(metadata1, metadata2)


@pytest.mark.parametrize("type_name", all_metadata_types)
def test_equals_different_custom_metadata(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having different custom_metadata
    are not equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.custom_metadata["key1"] = BooleanValue(1)
    metadata1.custom_metadata["key2"] = BooleanValue(0)
    metadata2 = metadata_type()
    metadata2.custom_metadata["key2"] = BooleanValue(1)
    metadata2.custom_metadata["key1"] = BooleanValue(1)
    assert_are_not_equal(metadata1, metadata2)


# NumericMetadata:

numeric_metadata_types = [
    "IntegerMetadata",
    "IntegerArrayMetadata",
    "RealMetadata",
    "RealArrayMetadata",
]


@pytest.mark.parametrize("type_name", numeric_metadata_types)
def test_equals_same_units(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having the same units are equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.description = "Some description."
    metadata1.units = "km per hr"
    metadata2 = metadata_type()
    metadata2.units = "km per hr"
    metadata2.description = "Some description."
    assert_equals(metadata1, metadata2)


@pytest.mark.parametrize("type_name", numeric_metadata_types)
def test_equals_different_units(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having different units are not
    equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.description = "Some description."
    metadata1.units = "km per hr"
    metadata2 = metadata_type()
    metadata2.units = "km per hour"
    metadata2.description = "Some description."
    assert_are_not_equal(metadata1, metadata2)


@pytest.mark.parametrize("type_name", numeric_metadata_types)
def test_equals_same_display_format(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having the same display format
    are equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.description = "Some description."
    metadata1.units = "seconds"
    metadata1.display_format = "hh:mm:ss"
    metadata2 = metadata_type()
    metadata2.units = "seconds"
    metadata2.description = "Some description."
    metadata2.display_format = "hh:mm:ss"
    assert_equals(metadata1, metadata2)


@pytest.mark.parametrize("type_name", numeric_metadata_types)
def test_equals_different_display_format(type_name: str) -> None:
    """
    Tests whether metadata objects of the same type and having different display format
    are not equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    None
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.description = "Some description."
    metadata1.units = "seconds"
    metadata1.display_format = "hh:mm:ss"
    metadata2 = metadata_type()
    metadata2.units = "seconds"
    metadata2.description = "Some description."
    metadata2.display_format = "hh.mm.ss"
    assert_are_not_equal(metadata1, metadata2)


# bounds:


@pytest.mark.parametrize(
    "type_name, bound, value1, value2",
    [
        ("IntegerMetadata", "lower_bound", None, None),
        ("IntegerMetadata", "lower_bound", 10, 10),
        ("IntegerMetadata", "lower_bound", IntegerValue(0), 0),
        ("IntegerMetadata", "lower_bound", IntegerValue(-100), -100),
        ("IntegerMetadata", "upper_bound", None, None),
        ("IntegerMetadata", "upper_bound", IntegerValue(0), 0),
        ("IntegerMetadata", "upper_bound", -100, IntegerValue(-100)),
        ("IntegerArrayMetadata", "lower_bound", 10, 10),
        ("IntegerArrayMetadata", "upper_bound", 200, 200),
        ("RealMetadata", "lower_bound", None, None),
        ("RealMetadata", "lower_bound", 0.1, 0.1),
        ("RealMetadata", "lower_bound", RealValue(0.0), 0.0),
        ("RealMetadata", "lower_bound", RealValue(-0.5), -0.5),
        ("RealArrayMetadata", "lower_bound", 0.1, 0.1),
        ("RealMetadata", "upper_bound", None, None),
        ("RealMetadata", "upper_bound", RealValue(0.0), 0.0),
        ("RealMetadata", "upper_bound", RealValue(-0.5), -0.5),
        ("RealArrayMetadata", "upper_bound", 1.1, 1.1),
    ],
)
def test_equals_same_bound(type_name: str, bound: str, value1: Any, value2: Any) -> None:
    """
    Tests whether metadata objects of the same type and having the same bound value are
    equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.
    bound Name of the bound to test.
    value1 First value of the bound to test.
    value2 Second value of the bound to test.

    Returns
    -------
    nothing
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    setattr(metadata1, bound, value1)
    metadata2 = metadata_type()
    setattr(metadata2, bound, value2)
    assert_equals(metadata1, metadata2)


@pytest.mark.parametrize(
    "type_name, bound, value1, value2",
    [
        ("IntegerMetadata", "lower_bound", None, IntegerValue(0)),
        ("IntegerMetadata", "lower_bound", IntegerValue(0), None),
        ("IntegerMetadata", "lower_bound", IntegerValue(-100), IntegerValue(100)),
        ("IntegerMetadata", "lower_bound", IntegerValue(-100), -99),
        ("IntegerMetadata", "upper_bound", None, IntegerValue(0)),
        ("IntegerMetadata", "upper_bound", IntegerValue(0), None),
        ("IntegerMetadata", "upper_bound", IntegerValue(-100), IntegerValue(100)),
        ("IntegerArrayMetadata", "lower_bound", 1, 2),
        ("IntegerArrayMetadata", "upper_bound", 1, 2),
        ("RealMetadata", "lower_bound", None, RealValue(0.0)),
        ("RealMetadata", "lower_bound", RealValue(0.0), None),
        ("RealMetadata", "lower_bound", RealValue(-0.5), RealValue(0.5)),
        ("RealMetadata", "lower_bound", 3.4, 3.3),
        ("RealMetadata", "upper_bound", None, RealValue(0.0)),
        ("RealMetadata", "upper_bound", RealValue(0.0), None),
        ("RealMetadata", "upper_bound", RealValue(-0.5), RealValue(0.5)),
        ("RealArrayMetadata", "lower_bound", 0.1, -0.1),
        ("RealArrayMetadata", "upper_bound", 1.1, 20.0),
    ],
)
def test_equals_different_bound(type_name: str, bound: str, value1: Any, value2: Any) -> None:
    """
    Tests whether metadata objects of the same type and having different bound values
    are not equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.
    bound Name of the bound to test.
    value1 First value of the bound to test.
    value2 Second value of the bound to test.

    Returns
    -------
    nothing
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    setattr(metadata1, bound, value1)
    metadata2 = metadata_type()
    setattr(metadata2, bound, value2)
    assert_are_not_equal(metadata1, metadata2)


@pytest.mark.parametrize(
    "type_name, value1, value2",
    [
        ("IntegerMetadata", None, None),
        ("IntegerMetadata", [IntegerValue(0)], [0]),
        ("IntegerMetadata", [], []),
        ("IntegerMetadata", [0, 1, 2], [IntegerValue(0), 1, IntegerValue(2)]),
        ("IntegerArrayMetadata", [0, 1, 2], [0, 1, 2]),
        ("RealMetadata", None, None),
        ("RealMetadata", [RealValue(0.2)], [0.2]),
        ("RealMetadata", [RealValue(0.1), 0.2, RealValue(0.3)], [0.1, RealValue(0.2), 0.3]),
        ("RealMetadata", [1.0, 2.1, 2.2], [1.0, 2.1, 2.2]),
        ("RealArrayMetadata", [1.0, 2.1, 2.2], [1.0, 2.1, 2.2]),
        ("StringMetadata", None, None),
        ("StringMetadata", [], []),
        ("StringMetadata", ["uno", "dos", "tres"], ["uno", StringValue("dos"), "tres"]),
        ("StringArrayMetadata", ["uno", "dos", "tres"], ["uno", "dos", "tres"]),
    ],
)
def test_equals_same_enumerated_values(type_name: str, value1: Any, value2: Any) -> None:
    """
    Tests whether metadata objects of the same type and having the same
    enumerated_values value are equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.
    value1 First value of the enumerated_values property to test.
    value2 Second value of the enumerated_values property to test.

    Returns
    -------
    nothing
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.enumerated_values = value1
    metadata2 = metadata_type()
    metadata2.enumerated_values = value2
    assert_equals(metadata1, metadata2)


@pytest.mark.parametrize(
    "type_name, value1, value2",
    [
        ("IntegerMetadata", None, []),
        ("IntegerMetadata", [IntegerValue(0)], [1]),
        ("IntegerMetadata", [0], []),
        ("IntegerMetadata", [0, 1, 2], [IntegerValue(0), 1, IntegerValue(3)]),
        ("IntegerMetadata", [0, 1, 2], [0, 1, 2, 3]),
        ("IntegerArrayMetadata", [0, 1, 2], [0, 1, 2, 3]),
        ("RealMetadata", None, []),
        ("RealMetadata", [RealValue(0.2)], [0.3]),
        ("RealMetadata", [RealValue(0.1), 0.2, RealValue(0.3)], [0.1, RealValue(0.3), 0.3]),
        ("RealMetadata", [1.0, 2.1, 2.2], [1.0, 2.1, 2.3]),
        ("RealArrayMetadata", [1.0, 2.1, 2.2], [1.0, 2.1, 2.3]),
        ("StringMetadata", None, []),
        ("StringMetadata", [], [""]),
        ("StringMetadata", ["uno", "dos", "tres"], ["uno", "tres", "dos"]),
        ("StringArrayMetadata", ["uno", "dos", "tres"], ["uno", "tres", "dos"]),
    ],
)
def test_equals_different_enumerated_values(type_name: str, value1: Any, value2: Any) -> None:
    """
    Tests whether metadata objects of the same type and having different
    enumerated_values value are not equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.
    value1 First value of the enumerated_values property to test.
    value2 Second value of the enumerated_values property to test.

    Returns
    -------
    nothing
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.enumerated_values = value1
    metadata2 = metadata_type()
    metadata2.enumerated_values = value2
    assert_are_not_equal(metadata1, metadata2)


@pytest.mark.parametrize(
    "type_name, value1, value2",
    [
        ("IntegerMetadata", None, None),
        ("IntegerMetadata", "", ""),
        ("IntegerMetadata", [], []),
        ("IntegerMetadata", ["one", "two", "three"], ["one", "two", "three"]),
        ("IntegerArrayMetadata", ["one", "two", "three"], ["one", "two", "three"]),
        ("RealMetadata", None, None),
        ("RealMetadata", "", ""),
        ("RealMetadata", [], []),
        ("RealMetadata", ["pi", "e", "sigma"], ["pi", "e", "sigma"]),
        ("RealArrayMetadata", ["pi", "e", "sigma"], ["pi", "e", "sigma"]),
        ("StringMetadata", None, None),
        ("StringMetadata", [], []),
        ("StringMetadata", ["uno", "dos", "tres"], ["uno", "dos", "tres"]),
        ("StringArrayMetadata", ["uno", "dos", "tres"], ["uno", "dos", "tres"]),
    ],
)
def test_equals_same_enumerated_aliases(type_name: str, value1: Any, value2: Any) -> None:
    """
    Tests whether metadata objects of the same type and having the same
    enumerated_values value are equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.
    value1 First value of the enumerated_aliases property to test.
    value2 Second value of the enumerated_aliases property to test.

    Returns
    -------
    nothing
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.enumerated_aliases = value1
    metadata2 = metadata_type()
    metadata2.enumerated_aliases = value2
    assert_equals(metadata1, metadata2)


@pytest.mark.parametrize(
    "type_name, value1, value2",
    [
        ("IntegerMetadata", None, []),
        ("IntegerMetadata", [], ""),
        ("IntegerMetadata", [""], []),
        ("IntegerMetadata", ["one", "two", "three"], ["one", "two", "four"]),
        ("IntegerArrayMetadata", ["one", "two", "three"], ["one", "two", "four"]),
        ("RealMetadata", None, []),
        ("RealMetadata", [], [""]),
        ("RealMetadata", ["pi", "e", "sigma"], ["pi", "e", "delta"]),
        ("RealArrayMetadata", ["pi", "e", "sigma"], ["pi", "e", "delta"]),
        ("StringMetadata", None, []),
        ("StringMetadata", [], [""]),
        ("StringMetadata", ["uno", "dos", "tres"], ["uno", "tres", "dos"]),
        ("StringArrayMetadata", ["uno", "dos", "tres"], ["uno", "tres", "dos"]),
    ],
)
def test_equals_different_enumerated_aliases(type_name: str, value1: Any, value2: Any) -> None:
    """
    Tests whether metadata objects of the same type and having different
    enumerated_values value are not equal.

    Parameters
    ----------
    type_name Name of the metadata type to test.
    value1 First value of the enumerated_aliases property to test.
    value2 Second value of the enumerated_aliases property to test.

    Returns
    -------
    nothing
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.enumerated_aliases = value1
    metadata2 = metadata_type()
    metadata2.enumerated_aliases = value2
    assert_are_not_equal(metadata1, metadata2)


@pytest.mark.parametrize("type_name", all_metadata_types)
def test_clone_custom_metadata(type_name: str) -> None:
    """
    Tests whether metadata objects are properly cloned.

    Parameters
    ----------
    type_name Name of the metadata type to test.

    Returns
    -------
    nothing
    """
    metadata_type = globals()[type_name]
    metadata1 = metadata_type()
    metadata1.custom_metadata["key1"] = IntegerValue(1)
    metadata1.custom_metadata["key2"] = IntegerValue(0)
    metadata2 = metadata1.clone()
    assert_equals(metadata1, metadata2)
    assert metadata1.custom_metadata["key1"] is not metadata2.custom_metadata["key1"]
    assert metadata1.custom_metadata["key2"] is not metadata2.custom_metadata["key2"]


@pytest.mark.parametrize(
    "type_name,expected_typename", zip(all_metadata_types, all_metadata_json_names)
)
def test_default_metadata_to_dict(type_name: str, expected_typename: str) -> None:
    """Tests that no extra keys are added for metadata values that are not set."""
    metadata_type = globals()[type_name]
    metadata = metadata_type()

    result = metadata.to_dict()

    expected_empty_metadata = {
        "type": expected_typename,
    }
    assert result == expected_empty_metadata


@pytest.mark.parametrize(
    "type_name,expected_typename", zip(non_numeric_metadata_types, non_numeric_metadata_json_names)
)
def test_non_numeric_metadata_to_dict(type_name: str, expected_typename: str) -> None:
    """Tests that all non-numeric metadata values are serialized correctly."""
    metadata_type = globals()[type_name]
    metadata = metadata_type()
    metadata.description = "djmike"
    if "String" in expected_typename:
        metadata.enumerated_aliases = ["a", "b", "c", "d", "e"]
        metadata.enumerated_values = [
            StringValue("v"),
            StringValue("w"),
            StringValue("x"),
            StringValue("y"),
            StringValue("z"),
        ]

    result = metadata.to_dict()

    expected_non_numeric_metadata: dict = {
        "type": expected_typename,
        "description": "djmike",
    }
    if "String" in expected_typename:
        expected_non_numeric_metadata["enumAliases"] = ["a", "b", "c", "d", "e"]
        expected_non_numeric_metadata["enumValues"] = ["v", "w", "x", "y", "z"]
    assert result == expected_non_numeric_metadata


@pytest.mark.parametrize(
    "type_name,expected_typename,enum_type",
    zip(numeric_metadata_types, numeric_metadata_json_names, numeric_metadata_enumeration_types),
)
def test_numeric_metadata_to_dict(type_name: str, expected_typename: str, enum_type: type) -> None:
    """Tests that all numeric metadata values are serialized correctly."""
    metadata_type = globals()[type_name]
    metadata = metadata_type()
    metadata.description = "djmike"
    metadata.units = "tacos/hr"
    metadata.display_format = "oough"
    metadata.lower_bound = enum_type(1)
    metadata.upper_bound = enum_type(5)
    metadata.enumerated_aliases = ["a", "b", "c", "d", "e"]
    metadata.enumerated_values = [
        enum_type(1),
        enum_type(2),
        enum_type(3),
        enum_type(4),
        enum_type(5),
    ]

    result = metadata.to_dict()

    expected_non_numeric_metadata = {
        "type": expected_typename,
        "description": "djmike",
        "units": "tacos/hr",
        "format": "oough",
        "lowerBound": 1,
        "upperBound": 5,
        "enumAliases": ["a", "b", "c", "d", "e"],
        "enumValues": [1, 2, 3, 4, 5],
    }
    assert result == expected_non_numeric_metadata


@pytest.mark.parametrize(
    "type_name,expected_typename,enum_type",
    zip(
        all_metadata_types,
        all_metadata_json_names,
        [*numeric_metadata_enumeration_types, *[None] * len(non_numeric_metadata_json_names)],
    ),
)
def test_metadata_to_from_dict(type_name: str, expected_typename: str, enum_type: type):
    metadata_type = globals()[type_name]
    metadata = metadata_type()
    metadata.description = "djmike"
    if enum_type is not None:
        metadata.units = "tacos/hr"
        metadata.display_format = "oough"
        metadata.lower_bound = enum_type(1)
        metadata.upper_bound = enum_type(5)
        metadata.enumerated_aliases = ["a", "b", "c", "d", "e"]
        metadata.enumerated_values = [
            enum_type(1),
            enum_type(2),
            enum_type(3),
            enum_type(4),
            enum_type(5),
        ]

    value = metadata.to_dict()
    result = metadata_type.from_dict(value)

    assert result == metadata
