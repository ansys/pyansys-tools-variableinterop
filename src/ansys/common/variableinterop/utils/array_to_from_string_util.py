"""Definition of ArrayToFromStringUtil."""
from math import prod
import re
from typing import Any, Callable, List, Match, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

from ansys.common.variableinterop.exceptions import FormatException
from ansys.common.variableinterop.variable_value import CommonArrayValue, IVariableValue


class ArrayToFromStringUtil:
    """Utility methods for converting CommonValueArrays to/from string \
    representations."""

    # Regular Expression pattern, as a string, of an array value with the optional curly braces.
    # Captures the list of values, unparsed, in valueList.
    _array_with_curly_braces_regex: str = r'{(?P<valueList>.*)}'
    # Regular Expression pattern, as a string, of an array value with the optional bounds prefix
    # Captures the list of values, unparsed, in valueList and the list of
    # array bounds, unparsed, in boundList.
    _array_with_bounds_regex: str = r'^\s*' + r'BOUNDS\s*\[(?P<boundList>[\d,\s]*)\]\s*' + \
        _array_with_curly_braces_regex + r'\s*$'
    #
    _quoted_value_regex: str = r'^\s*"(?P<value>(([^"\\])|(\\.))*)"\s*(?P<comma>,?)(?P<rest>.*)$'
    #
    _unquoted_value_regex: str = r'^\s*(?P<value>[^,"]*[^,"\s])\s*(?P<comma>,?)(?P<rest>.*)$'

    @staticmethod
    def value_to_string(value: NDArray, stringify_action: Callable) -> str:
        """
        Convert an array value to a string representation of it.

        stringify_action allows converting the value arbitrarily, so
        both API and display strings can use this method.

        Parameters
        ----------
        value : NDArray
            The array value to convert.
        stringify_action : Callable
            The action used to convert each individual value in the array.

        Returns
        -------
        str
            The generated string.
        """
        api_string: str = ""
        # Specify bounds for arrays of more than 1d:
        if value.ndim > 1:
            api_string = "bounds[" + ','.join(map(str, value.shape)) + "]{"
        api_string += ','.join(map(stringify_action, np.nditer(value, flags=['refs_ok'])))
        if value.ndim > 1:
            api_string += "}"
        return api_string

    @staticmethod
    def string_to_value(value: str,
                        create_action: Callable[[Any], CommonArrayValue],
                        valueify_action: Callable[[str], IVariableValue]) -> CommonArrayValue:
        """
        Convert a string into a CommonValueArray object.

        valueify_action allows converting the value arbitrarily, so
        both API and display strings can use this method.

        Parameters
        ----------
        value : str
            The string value to parse.
        create_action : Callable[[Any], CommonArrayValue]
            An action that takes either a shape or a list of initial values, and creates \
            a new array of the correct type.
        valueify_action : Callable[[str], IVariableValue]
            The action used to parse each individual value to the correct type.

        Returns
        -------
        CommonArrayValue
            A new array object with the parsed values.
        """
        array: CommonArrayValue
        value_str: str

        # check for bounds string
        match: Optional[Match[str]] = re.search(ArrayToFromStringUtil._array_with_bounds_regex,
                                                value, flags=re.IGNORECASE)
        if match is not None:  # There are bounds
            value_str = match.groupdict()["valueList"]

            # parse bounds as tuple
            bounds: str = match.groupdict()["boundList"]
            lengths: Tuple = tuple([int(b) for b in bounds.split(',')])

            # parse each value into a flat list
            comma_after_last_value: str = ""
            converted_list: List[IVariableValue] = []
            for i in range(prod(lengths)):
                match = ArrayToFromStringUtil._value_regex_match(value_str)
                if match is not None:
                    converted: IVariableValue = valueify_action(match.groupdict()["value"])
                    converted_list.append(converted)
                    value_str = match.groupdict()["rest"]
                    comma_after_last_value = match.groupdict()["comma"]
                else:
                    raise FormatException
            # ensure there were no extra values
            if comma_after_last_value == ",":
                raise FormatException
            # create the array from the values
            array = create_action(np.reshape(converted_list, lengths).tolist())

        else:  # No bounds
            match = re.search(
                ArrayToFromStringUtil._array_with_curly_braces_regex, value, flags=re.IGNORECASE)
            if match is not None:
                value_str = match.groupdict()["valueList"]
            else:
                value_str = value
            value_list: List = []
            match = ArrayToFromStringUtil._value_regex_match(value_str)
            while match is not None:
                value_list.append(valueify_action(match.groupdict()["value"]))
                value_str = match.groupdict()["rest"]
                match = ArrayToFromStringUtil._value_regex_match(value_str)
            if value_str != "":
                raise FormatException
            array = create_action(value_list)

        return array

    @staticmethod
    def _value_regex_match(value_str: str) -> Optional[Match[str]]:
        """
        Parse a single value, that may be quoted.

        Parameters
        ----------
        value_str : str
            The string to parse.

        Returns
        -------
        Optional[Match[str]]
            The regex match object, or None if not matched.
        """
        match: Optional[Match[str]] = re.search(ArrayToFromStringUtil._quoted_value_regex,
                                                value_str, flags=re.IGNORECASE)
        if match is None:
            match = re.search(ArrayToFromStringUtil._unquoted_value_regex, value_str)
        return match
