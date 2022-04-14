"""Unit tests of IVariableMetadataVisitor, and accept methods of metadata types."""

from typing import Any

import pytest

import ansys.common.variableinterop.boolean_metadata as boolean_metadata
import ansys.common.variableinterop.common_variable_metadata as common_variable_metadata
import ansys.common.variableinterop.integer_metadata as integer_metadata
import ansys.common.variableinterop.ivariablemetadata_visitor as ivariablemetadata_visitor
import ansys.common.variableinterop.real_metadata as real_metadata
import ansys.common.variableinterop.string_metadata as string_metadata


class TestVisitor(ivariablemetadata_visitor.IVariableMetadataVisitor[str]):
    """
    Implementation of IVariableValueVisitor for testing.

    Simply returns the metadata variable type when visited.
    """

    def visit_integer(self, metadata: integer_metadata.IntegerMetadata) -> str:
        return metadata.variable_type.name

    def visit_real(self, metadata: real_metadata.RealMetadata) -> str:
        return metadata.variable_type.name

    def visit_boolean(self, metadata: boolean_metadata.BooleanMetadata) -> str:
        return metadata.variable_type.name

    def visit_string(self, metadata: string_metadata.StringMetadata) -> str:
        return metadata.variable_type.name

    # IntegerArray

    # RealArray

    # BooleanArray

    # StringArray


@pytest.mark.parametrize(
    "metadata,expected",
    [
        pytest.param(real_metadata.RealMetadata(), "REAL", id="Real"),
        pytest.param(integer_metadata.IntegerMetadata(), "INTEGER", id="Integer"),
        pytest.param(boolean_metadata.BooleanMetadata(), "BOOLEAN", id="Boolean"),
        pytest.param(string_metadata.StringMetadata(), "STRING", id="String"),
    ]
)
def test_visiting_a_metadata_should_work(metadata: common_variable_metadata.CommonVariableMetadata,
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
