"""Definition of ArrayToFromStringUtil."""

from typing import Callable, Match, AnyStr, List, Tuple, Any

import numpy as np
import re
from numpy.typing import NDArray

from ansys.common.variableinterop.variable_value import CommonArrayValue, IVariableValue


class ArrayToFromStringUtil:
    """"""

    # Regular Expression pattern, as a string, of an array value with the optional curly braces.
    # Captures the list of values, unparsed, in valueList.
    _array_with_curly_braces_regex: str = r'{(?P<valueList>.*)}'
    # Regular Expression pattern, as a string, of an array value with the optional bounds prefix
    # Captures the list of values, unparsed, in valueList and the list of
    # array bounds, unparsed, in boundList.
    _array_with_bounds_regex: str = r'^\s*' + r'BOUNDS\s*\[(?P<boundList>[\d,\s]*)\]\s' + \
        _array_with_curly_braces_regex + r'\s*$'
    #
    _quoted_value_regex: str = r'^\s*""(?P<value>(([^""\\])|(\\.))*)""\s*(?P<comma>,?)(?P<rest>.*)$'
    #
    _unquoted_value_regex: str = r'^\s*(?P<value>[^,""]*[^,""\s])\s*(?P<comma>,?)(?P<rest>.*)$'

    @staticmethod
    def value_to_string(value: NDArray, stringify_action: Callable) -> str:
        """
        Convert an array value to a string representation of it.

        stringify_action allows converting the value arbitrarily, so
        both API and display strings can use this method.

        Parameters
        ----------
        value The array value to convert.
        stringify_action The action used to convert each individual
        value in the array.

        Returns
        -------
        The generated string.
        """
        api_string: str = ""
        # Specify bounds for arrays of more than 1d:
        if value.ndim > 1:
            api_string = "bounds[" + ','.join(map(str, value.shape)) + "]{"
        api_string += ','.join(map(stringify_action, np.nditer(value)))
        if value.ndim > 1:
            api_string += "}"
        return api_string

    @staticmethod
    def string_to_value(value: str,
                        create_action: Callable[[Any], CommonArrayValue],
                        valueify_action: Callable[[str], IVariableValue]) -> CommonArrayValue:
        """

        Parameters
        ----------
        value
        create_action
        valueify_action

        Returns
        -------

        """

        array: CommonArrayValue

        # check for bounds string
        match: Match[AnyStr] = re.search(ArrayToFromStringUtil._array_with_bounds_regex, value)
        # TODO: Why is regex not matching?
        if match is not None:  # There are bounds
            value_str: str = match.groupdict()["valueList"]

            # parse bounds
            bounds: str = match.groupdict()["boundList"]
            lengths: List[int] = [int(b) for b in bounds.split(',')]
            array = create_action(lengths)  # TODO: prolly wrong format

            comma_after_last_value: str = ""
            for i in []:  # TODO: loop over all array indexes
                match = ArrayToFromStringUtil._value_regex_match(value_str)
                if match is not None:
                    array[i] = valueify_action(match.groupdict()["value"])
                    value_str = match.groupdict()["rest"]
                    comma_after_last_value = match.groupdict()["comma"]
                else:
                    raise Exception  # TODO: FormatException
            if comma_after_last_value == ",":
                raise Exception  # TODO: FormatException

        else:  # No bounds
            match = re.search(ArrayToFromStringUtil._array_with_curly_braces_regex, value)
            value_str: str
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
                raise Exception  # TODO: FormatException
            array = create_action(value_list)

        return array

    @staticmethod
    def _value_regex_match(value_str: str) -> Match[AnyStr]:
        match: Match[AnyStr] = re.search(ArrayToFromStringUtil._quoted_value_regex, value_str)
        if match is None:
            match = re.search(ArrayToFromStringUtil._unquoted_value_regex, value_str)
        return match
