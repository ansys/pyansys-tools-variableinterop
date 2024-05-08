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

from typing import Any, cast
import pytest
from typing_extensions import reveal_type
from ansys.tools.variableinterop.api import ITypeLibrary
from unittest.mock import Mock
from pytest_mock import MockerFixture

from ansys.tools.variableinterop import RealValue, RealArrayValue, StringValue, UnifiedTypeLibrary, IncompatibleTypesException

def test_other_bogus() -> None:
    sut = UnifiedTypeLibrary()
    sv = StringValue("3.2")
    rv: RealValue = sut.runtime_convert(sv, "String", "Real")    
    assert rv == 3.2

def test_other_bogus2() -> None:
    sut = UnifiedTypeLibrary()
    sv = StringValue("abc")
    with pytest.raises(ValueError):
        rv: RealValue = sut.runtime_convert(sv, "String", "Real")    

def test_other_bogus3() -> None:
    sut = UnifiedTypeLibrary()
    sv = RealArrayValue(values=[1.1,2.2])
    bla = RealValue("2.2")
    print(f"ho {type(bla)}")
    with pytest.raises(IncompatibleTypesException):
        rv: RealValue = sut.runtime_convert(sv, "RealArray", "Real")    
    