# Copyright (C) 2024 - 2025 ANSYS, Inc. and/or its affiliates.
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

import ansys.tools.variableinterop as acvi

__value_cases = [
    pytest.param(acvi.IntegerValue(47), True, id="valid integer"),
    pytest.param(acvi.IntegerValue(47), False, id="invalid integer"),
    pytest.param(acvi.RealValue(-867.5309), True, id="valid real"),
    pytest.param(acvi.RealValue(867.5309), True, id="invalid real"),
]

__coerce_cases = [
    pytest.param(47, acvi.IntegerValue(47), id="integer"),
    pytest.param(-867.5309, acvi.RealValue(-867.5309), id="real"),
    pytest.param(True, acvi.BooleanValue(True), id="bool"),
    pytest.param("word", acvi.StringValue("word"), id="string"),
]


@pytest.mark.parametrize("value,is_valid", __value_cases)
def test_construct(value: acvi.IVariableValue, is_valid: bool):
    """Verify that the constructor works correctly."""
    # Execute
    sut = acvi.VariableState(value, is_valid)

    assert sut.value is value
    assert sut.is_valid == is_valid


@pytest.mark.parametrize("value,is_valid", __value_cases)
def test_clone(value: acvi.IVariableValue, is_valid: bool):
    """Verify that cloning works correctly."""
    # Setup
    original = acvi.VariableState(value, is_valid)

    # Execute
    clone = original.clone()

    # Verify
    assert isinstance(clone, acvi.VariableState)
    assert clone is not original
    assert clone.value is not original.value
    assert type(clone.value) == type(original.value)
    assert clone.value == original.value
    assert clone.is_valid == original.is_valid
    assert clone == original


@pytest.mark.parametrize("value,expected_value", __coerce_cases)
def test_implicit_coerce(value: Any, expected_value: acvi.IVariableValue):
    """Verify that the constructor implicitly coerces values."""
    # Execute
    sut = acvi.VariableState(value, True)

    assert isinstance(sut.value, acvi.IVariableValue)
    assert sut.value == expected_value
