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
"""Defines and implements a pseudo-visitor pattern for variable types."""
from abc import ABC, abstractmethod
from typing import Callable, Dict, Generic, TypeVar

from .variable_type import VariableType

T = TypeVar("T")


class IVariableTypePseudoVisitor(ABC, Generic[T]):
    """
    Defines an interface for pseudo-visitors of the ``VariableType`` enumeration.

    This interface defines a pseudo-visitor for possible ``VariableType`` values.
    Although this pattern ultimately requires the use of a single "switch-statement
    equivalent" (see the following ``__accept_map``), it confines the said switch to a single
    instance and allows it to essentially be reused with ``mypy`` "typesafety."
    """

    @abstractmethod
    def visit_unknown(self) -> T:
        """
        Visit the ``UNKNOWN`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_int(self) -> T:
        """
        Visit the ``INTEGER`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real(self) -> T:
        """
        Visit the ``REAL`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_boolean(self) -> T:
        """
        Visit the ``BOOLEAN`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string(self) -> T:
        """
        Visit the ``STRING`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file(self) -> T:
        """
        Visit the ``FILE`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_int_array(self) -> T:
        """
        Visit the ``INTEGER_ARRAY`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_real_array(self) -> T:
        """
        Visit the ``REAL_ARRAY`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_bool_array(self) -> T:
        """
        Visit the ``BOOLEAN_ARRAY`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_string_array(self) -> T:
        """
        Visit the ``STRING_ARRAY`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_file_array(self) -> T:
        """
        Visit the ``FILE_ARRAY`` variable type.

        Returns
        -------
        T
            Result, as documented by the implementing class.
        """
        raise NotImplementedError


def __accept_unknown(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the UNKNOWN variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_unknown()


def __accept_int(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``INTEGER`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_int()


def __accept_real(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``REAL`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_real()


def __accept_boolean(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``BOOLEAN`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_boolean()


def __accept_string(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``STRING`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_string()


def __accept_file(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``FILE`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_file()


def __accept_int_array(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``INTEGER_ARRAY`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_int_array()


def __accept_real_array(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``REAL_ARRAY`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_real_array()


def __accept_boolean_array(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``BOOLEAN_ARRAY`` variable type.

    Returns
    -------
    T
        Visitor's result.
    """
    return visitor.visit_bool_array()


def __accept_string_array(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``STRING_ARRAY`` variable type.

    Returns
    -------
    The visitor's result.
    """
    return visitor.visit_string_array()


def __accept_file_array(visitor: "IVariableTypePseudoVisitor[T]") -> T:
    """
    Accept a visitor to the ``FILE_ARRAY`` variable type.

    Returns
    -------
    The visitor's result.
    """
    return visitor.visit_file_array()


__accept_map: Dict["VariableType", Callable[["IVariableTypePseudoVisitor[T]"], T]] = {
    VariableType.UNKNOWN: __accept_unknown,
    VariableType.INTEGER: __accept_int,
    VariableType.REAL: __accept_real,
    VariableType.BOOLEAN: __accept_boolean,
    VariableType.STRING: __accept_string,
    VariableType.FILE: __accept_file,
    VariableType.INTEGER_ARRAY: __accept_int_array,
    VariableType.REAL_ARRAY: __accept_real_array,
    VariableType.BOOLEAN_ARRAY: __accept_boolean_array,
    VariableType.STRING_ARRAY: __accept_string_array,
    VariableType.FILE_ARRAY: __accept_file_array,
}
"""
A map of the variable types to the actual "accept" implementations that correspond to
them.

This allows Python to quickly and correctly find the right "accept" implementation.
"""


def vartype_accept(visitor: "IVariableTypePseudoVisitor[T]", var_type: VariableType) -> T:
    """
    Accept a visitor to the specified variable type.

    Parameters
    ----------
    visitor : T
        Visitor to accept.
    var_type : VariableType
        Variable type that the visitor should visit.

    Returns
    -------
    T
        Visitor's result.
    """
    if var_type in __accept_map:
        # If the type is in the enum mapping, run
        return __accept_map[var_type](visitor)
    else:
        return visitor.visit_unknown()
