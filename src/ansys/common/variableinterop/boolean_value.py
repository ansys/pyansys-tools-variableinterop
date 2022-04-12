"""Definition of BooleanValue."""
from __future__ import annotations

from typing import TypeVar, Dict

import numpy as np
from overrides import overrides

import ansys.common.variableinterop.to_bool_visitor as to_bool_visitor
import ansys.common.variableinterop.variable_type as variable_type
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.variable_value as variable_value

T = TypeVar("T")


class BooleanValue(variable_value.IVariableValue):
    """
    Wrapper around a boolean value.

    If you want the variable interop standard conversions, use xxxx (TODO)
    """

    import ansys.common.variableinterop.ivariable_visitor as ivariable_visitor

    @staticmethod
    def int64_to_bool(val: np.int64) -> bool:
        """
        Convert a numpy int64 to a bool value per interchange
        specifications.
        """
        return val != 0

    @staticmethod
    def int_to_bool(val: int) -> bool:
        """
        Convert an int to a bool value per interchange specifications.
        """
        return val != 0

    @staticmethod
    def float_to_bool(val: float) -> bool:
        """
        Convert a float value to a bool per interchange specifications.
        """
        return val != 0.0

    api_str_to_bool: Dict[str, bool] = {
        'yes': True,
        'y': True,
        'true': True,
        'no': False,
        'n': False,
        'false': False
    }
    """
    A mapping of acceptable normalized values for API string conversion
    to their corresponding bool value.
    """

    @staticmethod
    def str_to_bool(val: str) -> bool:
        """
        Convert a str to a bool per interchange specifications.
        """
        _value: str = str.lower(str.strip(val))
        if _value in BooleanValue.api_str_to_bool:
            return BooleanValue.api_str_to_bool[_value]
        else:
            try:
                _f_value: float = float(_value)
                return BooleanValue.float_to_bool(_f_value)
            except ValueError:
                pass
            raise ValueError

    def __init__(self, source: object = None):
        """
        Construct a BooleanValue from various source types. Supported
        types include:
        None: Constructs a False BooleanValue
        bool or numpy.bool_: Constructs a BooleanValue with the given
            Boolean value.
        IVariableValue: Constructs a BooleanValue per the specification
        Others: raises an exception
        """

        import ansys.common.variableinterop.exceptions as exceptions

        if source is None:
            self.__value: bool = False
        elif isinstance(source, bool):
            self.__value: bool = source
        elif isinstance(source, np.bool_):
            self.__value: bool = bool(source)
        elif isinstance(source, variable_value.IVariableValue):
            self.__value: bool = source.accept(to_bool_visitor.ToBoolVisitor())
        else:
            raise exceptions.IncompatibleTypesException(
                type(source).__name__, variable_type.VariableType.BOOLEAN)

    # equality definition here
    def __eq__(self, other):
        """
        Tests that the two objects are equivalent.
        """
        if isinstance(other, BooleanValue):
            return self.__value == other.__value
        elif isinstance(other, (bool, np.bool_)):
            return self.__value == other
        else:
            # TODO: instead of assuming not equal, should we test
            #  against the Python "falseness" of other?
            return False

    def __bool__(self):
        """
        Return the true-ness or false-ness of this object.
        """
        return self.__value

    def __hash__(self):
        """
        Returns a hash code for this object
        """
        return hash(self.__value)

    def __str__(self):
        """
        Return the string representation of this object.
        """
        return str(self.__value)

    def accept(self, visitor: ivariable_visitor.IVariableValueVisitor[T]) -> T:
        return visitor.visit_boolean(self)

    @property  # type: ignore
    @overrides
    def variable_type(self) -> variable_type.VariableType:
        return variable_type.VariableType.BOOLEAN

    @overrides
    def to_api_string(self) -> str:
        return str(self)

    def to_real_value(self) -> real_value.RealValue:
        """
        Convert a given BooleanValue to a RealValue.

        True is converted to 1.0 and False is is converted to 0.0
        (Note: this is temporarily a static until we can get the
        non-numpy64-bool derived version working, since there's currently no way to actually have
        a BooleanValue instance at the moment).

        Parameters
        ----------
        orig the original BooleanValue

        Returns
        -------
        A RealValue with value representing the original BooleanValue.
        """
        if self:
            return real_value.RealValue(1.0)
        else:
            return real_value.RealValue(0.0)

    __api_str_values: Dict[str, bool] = {
        'yes': True,
        'y': True,
        'true': True,
        'no': False,
        'n': False,
        'false': False
    }
    """
    Defines acceptable normalized values for API string conversion.
    """

    @staticmethod
    def from_api_string(value: str) -> BooleanValue:
        """
        Convert an API string back into a value.

        The conversion is performed according to the type
        interoperability specifications.

        Values which are parseable as floating-point numbers
        are parsed in that manner, then converted to boolean.

        Values which are non-numeric are checked to see if they match
        the following values for True: "true", "yes", or "y"; or the
        following values for False: "false", "no", or "n". The
        comparison is case-insensitive.

        Values not otherwise interpretable result in a ValueError.

        Parameters
        ----------
        value
        The string to convert.
        """
        return BooleanValue(BooleanValue.str_to_bool(value))

    # to_formatted_string here

    # from_formatted_string here

    def get_modelcenter_type(self) -> str:
        raise NotImplementedError
