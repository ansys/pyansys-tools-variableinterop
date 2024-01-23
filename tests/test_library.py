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

from typing import Any, Type

import numpy as np
import pytest

from ansys.tools import variableinterop as acvi
from test_utils import _create_exception_context


@pytest.mark.parametrize(
    "cons_arg,expect_exception",
    [
        (0, None),
        (9223372036854775807, None),
        (9223372036854775808, OverflowError),
        (-9223372036854775808, None),
        (-9223372036854775809, OverflowError),
        # TODO: Other cases such as passing in non-integers
    ],
)
def test_integer_value_constructor(cons_arg: Any, expect_exception: Type[BaseException]) -> None:
    """
    Tests that the IntegerValue constructor behaves as expected.

    Parameters
    ----------
    cons_arg The argument to pass to the constructor
    expect_exception The exception to expect, or None if no exception should be thrown

    Returns
    -------
    None
    """
    with _create_exception_context(expect_exception):
        a = acvi.IntegerValue(cons_arg)


@pytest.mark.parametrize(
    "left, right, expect_exception",
    [
        (acvi.IntegerValue(0), 0, None),
        (0, acvi.IntegerValue(0), None),
        # TODO: numpy does not overflow in this case:
        # (ansysvars.IntegerValue(9223372036854775807), 1, ValueError),
    ],
)
def test_integer_value_add(left: Any, right: Any, expect_exception: Type[BaseException]) -> None:
    """
    Tests that adding IntegerValue objects together works, and generally degrades into
    numpy objects.

    Parameters
    ----------
    left The left side of the addition
    right The right side of the addition
    expect_exception Any expected exception, or None if it should succeed

    Returns
    -------
    None
    """
    with _create_exception_context(expect_exception):
        result = left + right
        assert np.int64(result) == np.int64(left) + np.int64(right)
        assert isinstance(result, np.int64)


@pytest.mark.parametrize(
    "left, right, expect_exception",
    [
        (acvi.IntegerValue(0), 0, None),
        (acvi.IntegerValue(0), acvi.IntegerValue(-3), None),
        (0, acvi.IntegerValue(1), None),
        # TODO: numpy does not overflow in this case
        # (ansysvars.IntegerValue(9223372036854775807), -1, ValueError),
        (acvi.IntegerValue(2), "a", TypeError),
        # TODO: This will need special handling: (acvi.IntegerValue(2), 3.5, TypeError),
        # TODO: This will need special handling:
        #  (acvi.IntegerValue(2), acvi.RealValue(3.2), TypeError),
    ],
)
def test_integer_value_sub(left: Any, right: Any, expect_exception: Type[BaseException]) -> None:
    """
    Tests that subtraction of IntegerValue works and generally degrades into a numpy
    int64.

    Parameters
    ----------
    left The left side of the subtraction
    right The right side of the subtraction
    expect_exception Any expected exception, or None if it should succeed

    Returns
    -------
    None
    """
    with _create_exception_context(expect_exception):
        result = left - right
        assert np.int64(result) == np.int64(left) - np.int64(right)
        assert isinstance(result, np.int64)
