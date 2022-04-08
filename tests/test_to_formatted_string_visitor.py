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
        pytest.param(real_value.RealValue(0), "en_US.UTF-8", "0", id="0, en_US"),
        pytest.param(real_value.RealValue(0), "deu_deu.UTF-8", "0", id="0, deu_deu"),
        pytest.param(real_value.RealValue(3), "en_US.UTF-8", "3", id="3, en_US"),
        pytest.param(real_value.RealValue(3), "deu_deu.UTF-8", "3", id="3, deu_deu"),
        pytest.param(real_value.RealValue(3.14), "en_US.UTF-8", "3.14", id="3.14, en_US"),
        pytest.param(real_value.RealValue(3.14), "deu_deu.UTF-8", "3,14", id="3.14, deu_deu"),
        pytest.param(real_value.RealValue(1.7976931348623157e+308), "en_US.UTF-8",
                     "1.79769313486232E+308", id="Max Value, en_US"),
        pytest.param(real_value.RealValue(1.7976931348623157e+308), "deu_deu.UTF-8",
                     "1,79769313486232E+308", id="Max Value, deu_deu"),
        pytest.param(real_value.RealValue(-1.7976931348623157e+308), "en_US.UTF-8",
                     "-1.79769313486232E+308", id="Min Value, en_US"),
        pytest.param(real_value.RealValue(-1.7976931348623157e+308), "deu_deu.UTF-8",
                     "-1,79769313486232E+308", id="Min Value, deu_deu"),
        pytest.param(real_value.RealValue(np.NINF), "en_US.UTF-8", "-INF",
                     id="Neg Infinity, en_US"),
        pytest.param(real_value.RealValue(np.NINF), "deu_deu.UTF-8", "-INF",
                     id="Neg Infinity, deu_deu"),
        pytest.param(real_value.RealValue(np.nan), "en_US.UTF-8", "NAN", id="NAN, en_US"),
        pytest.param(real_value.RealValue(np.nan), "deu_deu.UTF-8", "NAN", id="NAN, deu_deu"),
        # Note that epsilon can vary between systems, so this is just testing tiny values
        pytest.param(real_value.RealValue(2.2250738585072014e-308), "en_US.UTF-8",
                     "2.2250738585072E-308", id="Epsilon, en_US"),
        pytest.param(real_value.RealValue(2.2250738585072014e-308), "deu_deu.UTF-8",
                     "2,2250738585072E-308", id="Epsilon, deu_deu")
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
        pytest.param(integer_value.IntegerValue(-1), "en_US.UTF-8", "-1", id="-1, en_US"),
        pytest.param(integer_value.IntegerValue(-1), "deu_deu.UTF-8", "-1", id="-1, deu_deu"),
        pytest.param(integer_value.IntegerValue(0), "en_US.UTF-8", "0", id="0, en_US"),
        pytest.param(integer_value.IntegerValue(0), "deu_deu.UTF-8", "0", id="0, deu_deu"),
        pytest.param(integer_value.IntegerValue(1), "en_US.UTF-8", "1", id="1, en_US"),
        pytest.param(integer_value.IntegerValue(1), "deu_deu.UTF-8", "1", id="1, deu_deu"),
        pytest.param(integer_value.IntegerValue(9223372036854775807), "en_US.UTF-8",
                     "9.22337E+18", id="Max Int, en_US"),
        pytest.param(integer_value.IntegerValue(9223372036854775807), "deu_deu.UTF-8",
                     "9,22337E+18", id="Max Int, deu_deu"),
        pytest.param(integer_value.IntegerValue(-9223372036854775808), "en_US.UTF-8",
                     "-9.22337E+18", id="Min Int, en_US"),
        pytest.param(integer_value.IntegerValue(-9223372036854775808), "deu_deu.UTF-8",
                     "-9,22337E+18", id="Min Int, deu_deu")
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
        pytest.param(boolean_value.BooleanValue(np.True_), "en_US.UTF-8", "True", id="True, en_US"),
        pytest.param(boolean_value.BooleanValue(np.True_), "deu_deu.UTF-8", "True", id="True, deu_deu"),
        pytest.param(boolean_value.BooleanValue(np.False_), "en_US.UTF-8", "False",
                     id="False, en_US"),
        pytest.param(boolean_value.BooleanValue(np.False_), "deu_deu.UTF-8", "False",
                     id="False, deu_deu")
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
        pytest.param(string_value.StringValue("foo"), "en_US.UTF-8", "foo", id="foo, en_US"),
        pytest.param(string_value.StringValue("foo"), "deu_deu.UTF-8", "foo", id="foo, deu_deu"),
        pytest.param(string_value.StringValue(""), "en_US.UTF-8", "", id="Empty, en_US"),
        pytest.param(string_value.StringValue(""), "deu_deu.UTF-8", "", id="Empty, deu_deu"),
        pytest.param(string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     "en_US.UTF-8", "Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", id="Unicode, en_US"),
        pytest.param(string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     "deu_deu.UTF-8", "Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", id="Unicode, deu_deu"),
        pytest.param(string_value.StringValue("Escapes>\n\r\t\\\"<"), "en_US.UTF-8",
                     "Escapes>\n\r\t\\\"<", id="Escapes, en_US"),
        pytest.param(string_value.StringValue("Escapes>\n\r\t\\\"<"), "deu_deu.UTF-8",
                     "Escapes>\n\r\t\\\"<", id="Escapes, deu_deu")
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
