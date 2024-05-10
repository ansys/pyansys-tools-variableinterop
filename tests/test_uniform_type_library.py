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

import numpy as np
import pytest

from abstract_type_library_compatibility_tests import AbstractTypeLibraryCompatibilityTests
from ansys.tools.variableinterop import RealArrayValue, RealValue, StringValue, UniformTypeLibrary
from ansys.tools.variableinterop.api import IncompatibleTypesError
from ansys.tools.variableinterop.api.itype_library import ITypeLibrary

# TODO: Better defined tests for UniformTypeLibrary


def test_runtime_convert_stringvalue_to_realvalue() -> None:
    sut = UniformTypeLibrary()
    sv = StringValue("3.2")
    rv: RealValue = sut.runtime_convert(sv, StringValue, RealValue)
    assert rv == 3.2


def test_runtime_convert_bad_string_to_realvalue() -> None:
    sut = UniformTypeLibrary()
    sv = StringValue("abc")
    with pytest.raises(ValueError):
        rv: RealValue = sut.runtime_convert(sv, StringValue, RealValue)


def test_runtime_convert_incompatible_types() -> None:
    sut = UniformTypeLibrary()
    sv = RealArrayValue(values=[1.1, 2.2])
    bla = RealValue("2.2")
    with pytest.raises(IncompatibleTypesError):
        rv: RealValue = sut.runtime_convert(sv, RealArrayValue, RealValue)


def test_runtime_convert_to_native_str() -> None:
    sut = UniformTypeLibrary()
    sv = StringValue("3.2")
    rv: str = sut.runtime_convert(sv, StringValue, str)
    assert rv == "3.2"
    assert type(rv) == str


def test_runtime_convert_from_native_str() -> None:
    sut = UniformTypeLibrary()
    sv = "3.2"
    rv: StringValue = sut.runtime_convert(sv, str, StringValue)
    assert rv == "3.2"
    assert type(rv) == StringValue


def test_runtime_convert_invalid_stringvalue_to_np_float() -> None:
    sut = UniformTypeLibrary()
    sv = StringValue("3.2")
    with pytest.raises(IncompatibleTypesError):
        rv: str = sut.runtime_convert(sv, StringValue, np.float64)


def test_runtime_convert_invalid_np_float_to_stringvalue() -> None:
    sut = UniformTypeLibrary()
    sv = np.float64(3.2)
    with pytest.raises(IncompatibleTypesError):
        rv: str = sut.runtime_convert(sv, np.float64, StringValue)


def test_runtime_convert_invalid_native_float_to_realvalue() -> None:
    sut = UniformTypeLibrary()
    sv = 3.2
    with pytest.raises(IncompatibleTypesError):
        rv: str = sut.runtime_convert(sv, type(sv), RealValue)


class TestUniformTypeLibrary(AbstractTypeLibraryCompatibilityTests):
    """Add the compatibility tests for the ``UniformTypeLibrary``"""

    def create_sut(self) -> ITypeLibrary:
        return UniformTypeLibrary()
