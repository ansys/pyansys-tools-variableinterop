"""Provides functions for ModelCenter-standard string escaping."""
from typing import Dict, List


def escape_string(unescaped: str) -> str:
    """
    Escape a string according to ModelCenter conventions.

    The following characters are escaped: backslash, newline,
    carriage return, tab, double-quote, and null. Backslash is itself
    used as an escape character.

    Parameters
    ----------
    unescaped : str
        Unescaped string.

    Returns
    -------
    str
        String with the specified characters escaped.
    """
    return (
        unescaped.replace("\\", r"\\")
        .replace("\n", r"\n")
        .replace("\r", r"\r")
        .replace("\t", r"\t")
        .replace('"', r"\"")
        .replace("\0", r"\0")
    )


__unescape_map: Dict[str, str] = {"n": "\n", "r": "\r", "t": "\t", "0": "\0"}
"""
This map contains characters escaped by the :meth:`escape_string` method that require
special handling.

Note that some of the characters actually escaped by the :meth:`escape_string` method
are not present in this map. In those cases, the correct unescaping behavior is to
insert the character after the backslash unchanged (backslash and double quotation marks).
"""


def unescape_string(escaped: str) -> str:
    r"""
    Unescape a string according to ``ModelCenter`` conventions.

    The escape sequences ``\n``, ``\r``, ``\t``, and ``\0`` are transformed into
    newline, carriage return, tab, and null respectively. In other
    cases where a backslash appears, it is simply removed
    and the following character is allowed to remain. (Note that this
    also results in the correct behavior for double-quotatoin marks and
    the backslash itself, even though those characters are escaped by
    the :meth:`escape_string` method.)

    Parameters
    ----------
    escaped : str
        String with the escape sequences.

    Returns
    -------
    str
        String with the escape sequences undone.
    """
    unescaped: List[str] = []
    str_index: int = 0
    str_length: int = len(escaped)

    # As long as our index in the string is less than the length,
    while str_index < str_length:
        # Examine the character at the current index,
        current_char: str = escaped[str_index]
        # and increment the index by one.
        str_index += 1
        # If the current character is a backslash,
        if current_char == "\\":
            # look at the next character in the string (if available),
            if str_index < str_length:
                current_char = escaped[str_index]
                # incrementing the index to move past the backslash.
                str_index += 1
                # Check to see if the character after the backslash should be replaced
                # with something besides itself:
                if current_char in __unescape_map:
                    current_char = __unescape_map[current_char]
                # Then append the current character to the unescaped string.
                unescaped.append(current_char)
        # Non-backslash characters should just be appended to the unescaped string.
        else:
            unescaped.append(current_char)

    return "".join(unescaped)
