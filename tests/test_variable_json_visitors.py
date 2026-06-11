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
import pytest

from ansys.tools.variableinterop import (
    BooleanArrayValue,
    BooleanValue,
    FileArrayValue,
    IntegerArrayValue,
    IntegerValue,
    IVariableValue,
    JsonToVariableValueVisitor,
    RealArrayValue,
    RealValue,
    StringArrayValue,
    StringValue,
    VariableType,
    VariableTypeToJsonVisitor,
    VariableValueToJsonVisitor,
    vartype_accept,
)
from ansys.tools.variableinterop.file_value import EmptyFileValue


@pytest.mark.parametrize(
    "var_type,expected",
    [
        pytest.param(VariableType.UNKNOWN, "Unknown"),
        pytest.param(VariableType.INTEGER, "Integer"),
        pytest.param(VariableType.REAL, "Double"),
        pytest.param(VariableType.BOOLEAN, "Boolean"),
        pytest.param(VariableType.STRING, "String"),
        pytest.param(VariableType.FILE, "File"),
        pytest.param(VariableType.INTEGER_ARRAY, "IntegerArray"),
        pytest.param(VariableType.REAL_ARRAY, "DoubleArray"),
        pytest.param(VariableType.BOOLEAN_ARRAY, "BooleanArray"),
        pytest.param(VariableType.STRING_ARRAY, "StringArray"),
        pytest.param(VariableType.FILE_ARRAY, "FileArray"),
        pytest.param(None, "Unknown"),
    ],
)
def test_variable_type_to_json(var_type: VariableType, expected: str) -> None:
    visitor = VariableTypeToJsonVisitor()

    result = vartype_accept(visitor, var_type)

    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(BooleanValue(True), True),
        pytest.param(IntegerValue(12345), 12345),
        pytest.param(RealValue(0.12345), 0.12345),
        pytest.param(StringValue("test"), "test"),
        pytest.param(BooleanArrayValue(values=[True, False, True]), "True,False,True"),
        pytest.param(IntegerArrayValue(values=[1, 2, 3]), "1,2,3"),
        pytest.param(RealArrayValue(values=[0.1, 2.3, 4.5]), "0.1,2.3,4.5"),
        pytest.param(StringArrayValue(values=["a", "b", "c"]), '"a","b","c"'),
    ],
)
def test_variable_value_to_json(value: IVariableValue, expected: str) -> None:
    visitor = VariableValueToJsonVisitor()

    result = value.accept(visitor)

    assert result == expected


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(EmptyFileValue()),
        pytest.param(FileArrayValue()),
    ],
)
def test_unsupported_variable_type_to_json(value: IVariableValue) -> None:
    visitor = VariableValueToJsonVisitor()

    try:
        value.accept(visitor)
        assert False
    except Exception as e:
        assert isinstance(e, NotImplementedError)


@pytest.mark.parametrize(
    "expected,value",
    [
        pytest.param(BooleanValue(True), True),
        pytest.param(IntegerValue(12345), 12345),
        pytest.param(RealValue(0.12345), 0.12345),
        pytest.param(StringValue(" test string"), " test string"),
        pytest.param(BooleanArrayValue(values=[True, False, True]), "True,False,True"),
        pytest.param(IntegerArrayValue(values=[1, 2, 3]), "1,2,3"),
        pytest.param(RealArrayValue(values=[0.1, 2.3, 4.5]), "0.1,2.3,4.5"),
        pytest.param(StringArrayValue(values=["aaa a", "b b b", "cc "]), '"aaa a","b b b","cc "'),
    ],
)
def test_json_variable_value(value: str, expected: IVariableValue) -> None:
    visitor = JsonToVariableValueVisitor(value)

    result = expected.variable_type.construct_variable_metadata().accept(visitor)

    assert result == expected
