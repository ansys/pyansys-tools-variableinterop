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
"""Defines the ``VariableType`` type."""
from typing import Dict, Type

from ..array_values import BooleanArrayValue, IntegerArrayValue, RealArrayValue, StringArrayValue
from ..scalar_values import BooleanValue, IntegerValue, RealValue, StringValue
from ..variable_type import VariableType


def to_type(var_type: VariableType):
    """Get the associated ``IVariableValue`` type."""
    __class_map: Dict[VariableType, Type] = {
        VariableType.STRING: StringValue,
        VariableType.REAL: RealValue,
        VariableType.INTEGER: IntegerValue,
        VariableType.BOOLEAN: BooleanValue,
        VariableType.STRING_ARRAY: StringArrayValue,
        VariableType.REAL_ARRAY: RealArrayValue,
        VariableType.INTEGER_ARRAY: IntegerArrayValue,
        VariableType.BOOLEAN_ARRAY: BooleanArrayValue,
    }
    return __class_map[var_type]


def to_type_name(var_type: VariableType):
    """Get the name of the associated ``IVariableValue`` type."""
    return to_type(var_type).__name__
