# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Tests for BooleanArrayValue."""
import numpy
import pytest

from ansys.tools.variableinterop.array_values import BooleanArrayValue


def test_default_construct() -> None:
    result = BooleanArrayValue()

    assert type(result) is BooleanArrayValue
    assert numpy.shape(result) == ()


def test_shape_construct() -> None:
    result = BooleanArrayValue(shape_=(2, 4, 9))

    assert type(result) is BooleanArrayValue
    assert numpy.shape(result) == (2, 4, 9)


# @pytest.mark.skip('bool array nditer returning array of bool instead of a bool for each element')
@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param(BooleanArrayValue(values=[True]), "True", id="Single value"),
        pytest.param(
            BooleanArrayValue(values=[False, True, False]), "False,True,False", id="Single dim"
        ),
        pytest.param(
            BooleanArrayValue(values=[[True], [False]]), "bounds[2,1]{True,False}", id="Two dims"
        ),
        pytest.param(
            BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            "bounds[2,2,3]{False,True,False,True,False,True,False,False,True,True,False,False}",
            id="Three dims",
        ),
    ],
)
def test_to_api_string(source: BooleanArrayValue, expected_result: str) -> None:
    """
    Verify to_api_string for BooleanArrayValue with valid cases.

    Parameters
    ----------
    source : BooleanArrayValue
        The original BooleanArrayValue.
    expected_result : str
        The expected API string.
    """
    # Execute
    result: str = source.to_api_string()

    # Verify
    assert type(result) is str
    assert result == expected_result


@pytest.mark.parametrize(
    "source,expected_result",
    [
        pytest.param("True", BooleanArrayValue(values=[True]), id="Single value"),
        pytest.param(
            "False,True,False", BooleanArrayValue(values=[False, True, False]), id="Single dim"
        ),
        pytest.param(
            "bounds[2,1]{True,False}", BooleanArrayValue(values=[[True], [False]]), id="Two dims"
        ),
        pytest.param(
            "bounds[2,2,3]{False,True,False,True,False,True,False,False,True,True,False,False}",
            BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            id="Three dims",
        ),
    ],
)
def test_from_api_string_valid(source: str, expected_result: BooleanArrayValue) -> None:
    """
    Verify that valid cases work on BooleanArrayValue.from_api_string.

    Parameters
    ----------
    source : str
        The string to parse.
    expected_result : BooleanArrayValue
        The expected result.
    """
    # Execute
    result: BooleanArrayValue = BooleanArrayValue.from_api_string(source)

    # Verify
    assert isinstance(result, BooleanArrayValue)
    assert numpy.array_equal(result, expected_result)
