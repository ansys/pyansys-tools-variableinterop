"""Unit tests of ToFormattedStringVisitor."""

import numpy as np
import pytest

import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_value as string_value
import ansys.common.variableinterop.to_formatted_string_visitor as to_fmt_visitor


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(real_value.RealValue(0), "en_US", "0", id="0, en_US"),
        pytest.param(real_value.RealValue(0), "de_DE", "0", id="0, de_DE"),
        pytest.param(real_value.RealValue(3), "en_US", "3", id="3, en_US"),
        pytest.param(real_value.RealValue(3), "de_DE", "3", id="3, de_DE"),
        pytest.param(real_value.RealValue(3.14), "en_US", "3.14", id="3.14, en_US"),
        pytest.param(real_value.RealValue(3.14), "de_DE", "3,14", id="3.14, de_DE"),
        pytest.param(real_value.RealValue(1.7976931348623157e+308), "en_US",
                     "1.79769313486232E+308", id="Max Value, en_US"),
        pytest.param(real_value.RealValue(1.7976931348623157e+308), "de_DE",
                     "1,79769313486232E+308", id="Max Value, de_DE"),
        pytest.param(real_value.RealValue(-1.7976931348623157e+308), "en_US",
                     "-1.79769313486232E+308", id="Min Value, en_US"),
        pytest.param(real_value.RealValue(-1.7976931348623157e+308), "de_DE",
                     "-1,79769313486232E+308", id="Min Value, de_DE"),
        pytest.param(real_value.RealValue(np.NINF), "en_US", "-INF",
                     id="Neg Infinity, en_US"),
        pytest.param(real_value.RealValue(np.NINF), "de_DE", "-INF",
                     id="Neg Infinity, de_DE"),
        pytest.param(real_value.RealValue(np.nan), "en_US", "NAN", id="NAN, en_US"),
        pytest.param(real_value.RealValue(np.nan), "de_DE", "NAN", id="NAN, de_DE"),
        # Note that epsilon can vary between systems, so this is just testing tiny values
        pytest.param(real_value.RealValue(2.2250738585072014e-308), "en_US",
                     "2.2250738585072E-308", id="Epsilon, en_US"),
        pytest.param(real_value.RealValue(2.2250738585072014e-308), "de_DE",
                     "2,2250738585072E-308", id="Epsilon, de_DE")
    ]
)
def test_visiting_a_real_formats_correctly(value: real_value.RealValue,
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
    # Setup
    visitor = to_fmt_visitor.ToFormattedStringVisitor(locale)

    # SUT
    result = visitor.visit_real(value)

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(integer_value.IntegerValue(-1), "en_US", "-1", id="-1, en_US"),
        pytest.param(integer_value.IntegerValue(-1), "de_DE", "-1", id="-1, de_DE"),
        pytest.param(integer_value.IntegerValue(0), "en_US", "0", id="0, en_US"),
        pytest.param(integer_value.IntegerValue(0), "de_DE", "0", id="0, de_DE"),
        pytest.param(integer_value.IntegerValue(1), "en_US", "1", id="1, en_US"),
        pytest.param(integer_value.IntegerValue(1), "de_DE", "1", id="1, de_DE"),
        pytest.param(integer_value.IntegerValue(9223372036854775807), "en_US",
                     "9.22337E+18", id="Max Int, en_US"),
        pytest.param(integer_value.IntegerValue(9223372036854775807), "de_DE",
                     "9,22337E+18", id="Max Int, de_DE"),
        pytest.param(integer_value.IntegerValue(-9223372036854775808), "en_US",
                     "-9.22337E+18", id="Min Int, en_US"),
        pytest.param(integer_value.IntegerValue(-9223372036854775808), "de_DE",
                     "-9,22337E+18", id="Min Int, de_DE")
    ]
)
def test_visiting_a_integer_formats_correctly(value: integer_value.IntegerValue,
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
    # Setup
    visitor = to_fmt_visitor.ToFormattedStringVisitor(locale)

    # SUT
    result = visitor.visit_integer(value)

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(boolean_value.BooleanValue(np.True_), "en_US", "True", id="True, en_US"),
        pytest.param(boolean_value.BooleanValue(np.True_), "de_DE", "True", id="True, de_DE"),
        pytest.param(boolean_value.BooleanValue(np.False_), "en_US", "False",
                     id="False, en_US"),
        pytest.param(boolean_value.BooleanValue(np.False_), "de_DE", "False",
                     id="False, de_DE")
    ]
)
def test_visiting_a_boolean_formats_correctly(value: boolean_value.BooleanValue,
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
    # Setup
    visitor = to_fmt_visitor.ToFormattedStringVisitor(locale)

    # SUT
    result = visitor.visit_boolean(value)

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param(string_value.StringValue("foo"), "en_US", "foo", id="foo, en_US"),
        pytest.param(string_value.StringValue("foo"), "de_DE", "foo", id="foo, de_DE"),
        pytest.param(string_value.StringValue(""), "en_US", "", id="Empty, en_US"),
        pytest.param(string_value.StringValue(""), "de_DE", "", id="Empty, de_DE"),
        pytest.param(string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     "en_US", "Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", id="Unicode, en_US"),
        pytest.param(string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     "de_DE", "Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", id="Unicode, de_DE"),
        pytest.param(string_value.StringValue("Escapes>\n\r\t\\\"<"), "en_US",
                     "Escapes>\n\r\t\\\"<", id="Escapes, en_US"),
        pytest.param(string_value.StringValue("Escapes>\n\r\t\\\"<"), "de_DE",
                     "Escapes>\n\r\t\\\"<", id="Escapes, de_DE")
    ]
)
def test_visiting_a_string_formats_correctly(value: string_value.StringValue,
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
    # Setup
    visitor = to_fmt_visitor.ToFormattedStringVisitor(locale)

    # SUT
    result = visitor.visit_string(value)

    # Verification
    assert result == expected
