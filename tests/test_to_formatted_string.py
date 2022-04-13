"""Unit tests of to_formatted_string for all IVariableValues."""

import numpy as np
import pytest

from ansys.common.variableinterop import (
    BooleanArrayValue,
    BooleanValue,
    IntegerValue,
    RealValue,
    StringValue,
)


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(RealValue(0), "en_US.UTF-8", "0", id="0, en_US"),
        pytest.param(RealValue(0), "de_DE.UTF-8", "0", id="0, de_DE"),
        pytest.param(RealValue(3), "en_US.UTF-8", "3", id="3, en_US"),
        pytest.param(RealValue(3), "de_DE.UTF-8", "3", id="3, de_DE"),
        pytest.param(RealValue(3.14), "en_US.UTF-8", "3.14", id="3.14, en_US"),
        pytest.param(RealValue(3.14), "de_DE.UTF-8", "3,14", id="3.14, de_DE"),
        pytest.param(RealValue(1.7976931348623157e+308), "en_US.UTF-8",
                     "1.79769313486232E+308", id="Max Value, en_US"),
        pytest.param(RealValue(1.7976931348623157e+308), "de_DE.UTF-8",
                     "1,79769313486232E+308", id="Max Value, de_DE"),
        pytest.param(RealValue(-1.7976931348623157e+308), "en_US.UTF-8",
                     "-1.79769313486232E+308", id="Min Value, en_US"),
        pytest.param(RealValue(-1.7976931348623157e+308), "de_DE.UTF-8",
                     "-1,79769313486232E+308", id="Min Value, de_DE"),
        pytest.param(RealValue(np.NINF), "en_US.UTF-8", "-INF",
                     id="Neg Infinity, en_US"),
        pytest.param(RealValue(np.NINF), "de_DE.UTF-8", "-INF",
                     id="Neg Infinity, de_DE"),
        pytest.param(RealValue(np.nan), "en_US.UTF-8", "NAN", id="NAN, en_US"),
        pytest.param(RealValue(np.nan), "de_DE.UTF-8", "NAN", id="NAN, de_DE"),
        # Note that epsilon can vary between systems, so this is just testing tiny values
        pytest.param(RealValue(2.2250738585072014e-308), "en_US.UTF-8",
                     "2.2250738585072E-308", id="Epsilon, en_US"),
        pytest.param(RealValue(2.2250738585072014e-308), "de_DE.UTF-8",
                     "2,2250738585072E-308", id="Epsilon, de_DE")
    ]
)
def test_visiting_a_real_formats_correctly(value: RealValue,
                                           locale: str,
                                           expected: np.str_) -> None:
    """
    Verifies the formatting of various RealValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # SUT
    result = value.to_formatted_string(locale)

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(IntegerValue(-1), "en_US.UTF-8", "-1", id="-1, en_US"),
        pytest.param(IntegerValue(-1), "de_DE.UTF-8", "-1", id="-1, de_DE"),
        pytest.param(IntegerValue(0), "en_US.UTF-8", "0", id="0, en_US"),
        pytest.param(IntegerValue(0), "de_DE.UTF-8", "0", id="0, de_DE"),
        pytest.param(IntegerValue(1), "en_US.UTF-8", "1", id="1, en_US"),
        pytest.param(IntegerValue(1), "de_DE.UTF-8", "1", id="1, de_DE"),
        pytest.param(IntegerValue(9223372036854775807), "en_US.UTF-8",
                     "9.22337E+18", id="Max Int, en_US"),
        pytest.param(IntegerValue(9223372036854775807), "de_DE.UTF-8",
                     "9,22337E+18", id="Max Int, de_DE"),
        pytest.param(IntegerValue(-9223372036854775808), "en_US.UTF-8",
                     "-9.22337E+18", id="Min Int, en_US"),
        pytest.param(IntegerValue(-9223372036854775808), "de_DE.UTF-8",
                     "-9,22337E+18", id="Min Int, de_DE")
    ]
)
def test_visiting_a_integer_formats_correctly(value: IntegerValue,
                                              locale: str,
                                              expected: np.str_) -> None:
    """
    Verifies the formatting of various IntegerValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # SUT
    result = value.to_formatted_string(locale)

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(BooleanValue(np.True_), "en_US.UTF-8", "True", id="True, en_US"),
        pytest.param(BooleanValue(np.True_), "de_DE.UTF-8", "True", id="True, de_DE"),
        pytest.param(BooleanValue(np.False_), "en_US.UTF-8", "False",
                     id="False, en_US"),
        pytest.param(BooleanValue(np.False_), "de_DE.UTF-8", "False",
                     id="False, de_DE")
    ]
)
def test_visiting_a_boolean_formats_correctly(value: BooleanValue,
                                              locale: str,
                                              expected: np.str_) -> None:
    """
    Verifies the formatting of various BooleanValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # SUT
    result = value.to_formatted_string(locale)

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(StringValue("foo"), "en_US.UTF-8", "foo", id="foo, en_US"),
        pytest.param(StringValue("foo"), "de_DE.UTF-8", "foo", id="foo, de_DE"),
        pytest.param(StringValue(""), "en_US.UTF-8", "", id="Empty, en_US"),
        pytest.param(StringValue(""), "de_DE.UTF-8", "", id="Empty, de_DE"),
        pytest.param(StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     "en_US.UTF-8", "Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", id="Unicode, en_US"),
        pytest.param(StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     "de_DE.UTF-8", "Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", id="Unicode, de_DE"),
        pytest.param(StringValue("Escapes>\n\r\t\\\"<"), "en_US.UTF-8",
                     "Escapes>\n\r\t\\\"<", id="Escapes, en_US"),
        pytest.param(StringValue("Escapes>\n\r\t\\\"<"), "de_DE.UTF-8",
                     "Escapes>\n\r\t\\\"<", id="Escapes, de_DE")
    ]
)
def test_visiting_a_string_formats_correctly(value: StringValue,
                                             locale: str,
                                             expected: np.str_) -> None:
    """
    Verifies the formatting of various StringValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # SUT
    result = value.to_formatted_string(locale)

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(BooleanArrayValue((1, 3), [np.True_, np.False_, np.True_]), "en_US.UTF-8",
                     "True,False,True", id="True, en_US"),
    ]
)
def test_visiting_a_boolean_array_formats_correctly(value: BooleanArrayValue,
                                              locale: str,
                                              expected: np.str_) -> None:
    """
    Verifies the formatting of various BooleanValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # SUT
    result = value.to_formatted_string(locale)

    # Verification
    assert result == expected