"""Unit tests of FromFormattedStringVisitor."""

import numpy as np
import pytest

import ansys.common.variableinterop.boolean_value as boolean_value
import ansys.common.variableinterop.from_formatted_string_visitor as from_fmt_visitor
import ansys.common.variableinterop.integer_value as integer_value
import ansys.common.variableinterop.real_value as real_value
import ansys.common.variableinterop.string_value as string_value


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("-1", "en_US", integer_value.IntegerValue(-1), id="-1, en_US"),
        pytest.param("-1", "de-DE", integer_value.IntegerValue(-1), id="-1, de-DE"),
        pytest.param("+1", "en_US", integer_value.IntegerValue(1), id="1, en_US"),
        pytest.param("+1", "de-DE", integer_value.IntegerValue(1), id="1, de-DE"),
        pytest.param("9.22337E+18", "en_US", integer_value.IntegerValue(9223370000000000000),
                     id="Max Int, en_US"),
        pytest.param("9,22337E+18", "de-DE", integer_value.IntegerValue(9223370000000000000),
                     id="Max Int, de-DE"),
        pytest.param("-9.22337E+18", "en_US",
                     integer_value.IntegerValue(-9223370000000000000), id="Min Int, en_US"),
        pytest.param("-9,22337E+18", "de-DE",
                     integer_value.IntegerValue(-9223370000000000000), id="Min Int, de-DE")
    ]
)
def test_converting_from_an_integer(value: str,
                                    locale: str,
                                    expected: integer_value.IntegerValue) -> None:
    """
    Verifies the conversion of various strings to IntegerValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = from_fmt_visitor.FromFormattedStringVisitor(value, locale)

    # SUT
    result: integer_value.IntegerValue = visitor.visit_int()

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("0", "en_US", real_value.RealValue(0), id="0, en_US"),
        pytest.param("0", "de-DE", real_value.RealValue(0), id="0, de-DE"),
        pytest.param("3", "en_US", real_value.RealValue(3), id="3, en_US"),
        pytest.param("3", "de-DE", real_value.RealValue(3), id="3, de-DE"),
        pytest.param("3.14", "en_US", real_value.RealValue(3.14), id="3.14, en_US"),
        pytest.param("3,14", "de-DE", real_value.RealValue(3.14), id="3.14, de-DE"),
        pytest.param("1.79769313486232E+308", "en_US",
                     real_value.RealValue(1.79769313486232e+308), id="Max Value, en_US"),
        pytest.param("1,79769313486232E+308", "de-DE",
                     real_value.RealValue(1.79769313486232e+308), id="Max Value, de-DE"),
        pytest.param("-1.79769313486232E+308", "en_US",
                     real_value.RealValue(-1.79769313486232e+308), id="Min Value, en_US"),
        pytest.param("-1,79769313486232E+308", "de-DE",
                     real_value.RealValue(-1.79769313486232e+308), id="Min Value, de-DE"),
        pytest.param("-INF", "en_US", real_value.RealValue(np.NINF),
                     id="Neg Infinity, en_US"),
        pytest.param("-INF", "de-DE", real_value.RealValue(np.NINF),
                     id="Neg Infinity, de-DE"),
        pytest.param("NAN", "en_US", real_value.RealValue(np.nan), id="NAN, en_US"),
        pytest.param("NAN", "de-DE", real_value.RealValue(np.nan), id="NAN, de-DE"),
        # Note that epsilon can vary between systems, so this is just testing tiny values
        pytest.param("2.2250738585072E-308", "en_US",
                     real_value.RealValue(2.2250738585072e-308), id="Epsilon, en_US"),
        pytest.param("2,2250738585072E-308", "de-DE",
                     real_value.RealValue(2.2250738585072e-308), id="Epsilon, de-DE")
    ]
)
def test_converting_from_a_real(value: str,
                                locale: str,
                                expected: real_value.RealValue) -> None:
    """
    Verifies the conversion of various strings to RealValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = from_fmt_visitor.FromFormattedStringVisitor(value, locale)

    # SUT
    result: real_value.RealValue = visitor.visit_real()

    # Verification
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("True", "en_US", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("True", "de-DE", boolean_value.BooleanValue(np.True_), id="True, de-DE"),
        pytest.param("False", "en_US", boolean_value.BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("False", "de-DE", boolean_value.BooleanValue(np.False_),
                     id="False, de-DE"),
        pytest.param("Yes", "en_US", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("Yes", "de-DE", boolean_value.BooleanValue(np.True_), id="True, de-DE"),
        pytest.param("On", "en_US", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("On", "de-DE", boolean_value.BooleanValue(np.True_), id="True, de-DE"),
        pytest.param("1", "en_US", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("1", "de-DE", boolean_value.BooleanValue(np.True_), id="True, de-DE"),
        pytest.param("No", "en_US", boolean_value.BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("No", "de-DE", boolean_value.BooleanValue(np.False_),
                     id="False, de-DE"),
        pytest.param("Off", "en_US", boolean_value.BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("Off", "de-DE", boolean_value.BooleanValue(np.False_),
                     id="False, de-DE"),
        pytest.param("0", "en_US", boolean_value.BooleanValue(np.False_), id="False, en_US"),
        pytest.param("0", "de-DE", boolean_value.BooleanValue(np.False_), id="False, de-DE")
    ]
)
def test_converting_from_a_boolean(value: str,
                                   locale: str,
                                   expected: boolean_value.BooleanValue) -> None:
    """
    Verifies the conversion of various strings to BooleanValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = from_fmt_visitor.FromFormattedStringVisitor(value, locale)

    # SUT
    result: boolean_value.BooleanValue = visitor.visit_boolean()

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("foo", "en_US", string_value.StringValue("foo"), id="foo, en_US"),
        pytest.param("foo", "de-DE", string_value.StringValue("foo"), id="foo, de-DE"),
        pytest.param("", "en_US", string_value.StringValue(""), id="Empty, en_US"),
        pytest.param("", "de-DE", string_value.StringValue(""), id="Empty, de-DE"),
        pytest.param("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", "en_US",
                     string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     id="Unicode, en_US"),
        pytest.param("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", "de-DE",
                     string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     id="Unicode, de-DE"),
        pytest.param("Escapes>\n\r\t\\\"<", "en_US",
                     string_value.StringValue("Escapes>\n\r\t\\\"<"), id="Escapes, en_US"),
        pytest.param("Escapes>\n\r\t\\\"<", "de-DE",
                     string_value.StringValue("Escapes>\n\r\t\\\"<"), id="Escapes, de-DE")
    ]
)
def test_converting_from_a_string(value: str,
                                  locale: str,
                                  expected: string_value.StringValue) -> None:
    """
    Verifies the conversion of various strings to StringValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = from_fmt_visitor.FromFormattedStringVisitor(value, locale)

    # SUT
    result: string_value.StringValue = visitor.visit_string()

    # Verification
    assert result == expected
