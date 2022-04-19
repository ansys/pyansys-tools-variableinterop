import pytest

from ansys.common.variableinterop import (
    BooleanArrayValue,
    BooleanValue,
    GetModelCenterTypeForValue,
    IntegerArrayValue,
    IntegerValue,
    IVariableValue,
    RealArrayValue,
    RealValue,
    StringArrayValue,
    StringValue,
    VariableType,
)
from ansys.common.variableinterop import ivariable_visitor as ivariable_visitor
from ansys.common.variableinterop import variable_type as variable_type_lib


class TestUnknownValue(IVariableValue):

    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[
            ivariable_visitor.T]) -> ivariable_visitor.T:
        pass

    @property
    def variable_type(self) -> variable_type_lib.VariableType:
        return VariableType.UNKNOWN

    def to_api_string(self) -> str:
        pass

    def from_api_string(self, value: str) -> None:
        pass

    def to_display_string(self, locale_name: str) -> str:
        pass

    def get_modelcenter_type(self) -> str:
        pass


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(TestUnknownValue(), "none"),
        pytest.param(BooleanValue(True), "bool"),
        pytest.param(BooleanArrayValue(1, [True]), "bool[]"),
        pytest.param(IntegerValue(0), "int"),
        pytest.param(IntegerArrayValue(1, [0]), "int[]"),
        pytest.param(RealValue(0), "double"),
        pytest.param(RealArrayValue(1, [0]), "double[]"),
        pytest.param(StringValue("0"), "string"),
        pytest.param(StringArrayValue(1, ["0"]), "string[]"),
        # pytest.param(FileValue(), "file"),
        # pytest.param(FileArrayValue(0, []), "file[]")
    ]
)
def test_get_modelcenter_type_for_value(value: IVariableValue, expected: str) -> None:
    """
    Verifies the correct ModelCenter type string is returned for each \
    IVariableValue.

    Parameters
    ----------
    value The value to use.
    expected The expected output.
    """
    # SUT
    result = GetModelCenterTypeForValue.get_modelcenter_type(value)

    # Verification
    assert result == expected
