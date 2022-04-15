"""Unit tests of IVariableMetadataVisitor, and accept methods of metadata types."""

from typing import Any, TypeVar
import pytest

import ansys.common.variableinterop as acvi


class TestVisitor(acvi.IVariableMetadataVisitor[str]):
    """
    Implementation of IVariableValueVisitor for testing.

    Simply returns the metadata variable type when visited.
    """

    T = TypeVar("T")

    def visit_integer(self, metadata: acvi.IntegerMetadata) -> str:
        return metadata.variable_type.name

    def visit_real(self, metadata: acvi.RealMetadata) -> str:
        return metadata.variable_type.name

    def visit_boolean(self, metadata: acvi.BooleanMetadata) -> str:
        return metadata.variable_type.name

    def visit_string(self, metadata: acvi.StringMetadata) -> str:
        return metadata.variable_type.name

    def visit_integer_array(self, metadata: acvi.IntegerArrayMetadata) -> str:
        return metadata.variable_type.name

    def visit_real_array(self, metadata: acvi.RealArrayMetadata) -> str:
        return metadata.variable_type.name

    def visit_boolean_array(self, metadata: acvi.BooleanArrayMetadata) -> str:
        return metadata.variable_type.name

    def visit_string_array(self, metadata: acvi.StringArrayMetadata) -> str:
        return metadata.variable_type.name


@pytest.mark.parametrize(
    "metadata,expected",
    [
        pytest.param(acvi.RealMetadata(), "REAL", id="Real"),
        pytest.param(acvi.IntegerMetadata(), "INTEGER", id="Integer"),
        pytest.param(acvi.BooleanMetadata(), "BOOLEAN", id="Boolean"),
        pytest.param(acvi.StringMetadata(), "STRING", id="String"),
        pytest.param(acvi.RealArrayMetadata(), "REAL_ARRAY", id="RealArray"),
        pytest.param(acvi.IntegerArrayMetadata(), "INTEGER_ARRAY", id="IntegerArray"),
        pytest.param(acvi.BooleanArrayMetadata(), "BOOLEAN_ARRAY", id="BooleanArray"),
        pytest.param(acvi.StringArrayMetadata(), "STRING_ARRAY", id="StringArray"),
    ]
)
def test_visiting_a_metadata_should_work(metadata: acvi.CommonVariableMetadata,
                                         expected: Any) -> None:
    """
    Verifies that the visitor pattern is working for CommonVariableMetadata.

    Parameters
    ----------
    metadata The CommonVariableMetadata to visit.
    expected The string representation of the variable type.
    """
    # Setup
    visitor = TestVisitor()

    # SUT
    result = metadata.accept(visitor)

    # Verification
    assert result == expected
