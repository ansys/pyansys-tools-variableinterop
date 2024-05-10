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

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
import pytest

from ansys.tools.variableinterop.api.itype_library import (
    REAL_NAME,
    REAL_TYPE,
    ITypeInformation,
    ITypeLibrary,
)

# TODO: Find a way to host this in a standalone library so that other type library
#       implementations can use it.


class AbstractTypeLibraryCompatibilityTests(ABC):
    """
    Abstract base class that defines a compatibility test suite for an ``ITypeLibrary``
    implementation.

    In your type library implementation test suite, create a subclass of
    this abstract class and implement ``create_sut``.
    """

    @abstractmethod
    def create_sut(self) -> ITypeLibrary:
        """Create an instance of the specific type library implementation to be
        tested."""
        raise NotImplementedError()

    sut: Optional[ITypeLibrary]
    """System under test (SUT)."""

    def setup_method(self) -> None:
        """Setup the tests by creating ``sut`` using ``create_sut``."""
        self.sut = self.create_sut()

    def teardown_method(self) -> None:
        """Clean up the test environment."""
        self.sut = None

    @pytest.mark.parametrize(
        "test_input",
        [
            (np.float64(3.2)),
            (np.float64(0.0)),
            (np.float64(np.inf)),
            (np.float64(np.nan)),
            # TODO: Epsilon, neg infinity, max, 64 bit
        ],
    )
    def test_converts_to_from_np_float64(self, test_input: np.float64) -> None:
        """
        Tests that the type library can convert to and from double values to the type
        library's "Real" type.

        Parameters
        ----------
        test_input: np.float64
            Real value to test.
        """
        # Arrange
        assert self.sut != None
        type_info: ITypeInformation = self.sut.get_type(REAL_NAME)

        # Act
        converted = self.sut.runtime_convert(test_input, REAL_TYPE, type_info.value_type)
        converted_back = self.sut.runtime_convert(converted, type_info.value_type, REAL_TYPE)

        # Assert
        assert type(test_input) == REAL_TYPE
        assert type(converted) == type_info.value_type
        assert type(converted_back) == REAL_TYPE
        assert (np.isnan(converted_back) and np.isnan(test_input)) or converted_back == test_input
