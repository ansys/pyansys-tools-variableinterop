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
        pytest.param("-1", "en_US.UTF-8", integer_value.IntegerValue(-1), id="-1, en_US"),
        pytest.param("-1", "deu_deu.UTF-8", integer_value.IntegerValue(-1), id="-1, deu_deu"),
        pytest.param("+1", "en_US.UTF-8", integer_value.IntegerValue(1), id="1, en_US"),
        pytest.param("+1", "deu_deu.UTF-8", integer_value.IntegerValue(1), id="1, deu_deu"),
        pytest.param("9.22337E+18", "en_US.UTF-8", integer_value.IntegerValue(9223370000000000000),
                     id="Max Int, en_US"),
        pytest.param("9,22337E+18", "deu_deu.UTF-8", integer_value.IntegerValue(9223370000000000000),
                     id="Max Int, deu_deu"),
        pytest.param("-9.22337E+18", "en_US.UTF-8",
                     integer_value.IntegerValue(-9223370000000000000), id="Min Int, en_US"),
        pytest.param("-9,22337E+18", "deu_deu.UTF-8",
                     integer_value.IntegerValue(-9223370000000000000), id="Min Int, deu_deu")
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
        pytest.param("0", "en_US.UTF-8", real_value.RealValue(0), id="0, en_US"),
        pytest.param("0", "deu_deu.UTF-8", real_value.RealValue(0), id="0, deu_deu"),
        pytest.param("3", "en_US.UTF-8", real_value.RealValue(3), id="3, en_US"),
        pytest.param("3", "deu_deu.UTF-8", real_value.RealValue(3), id="3, deu_deu"),
        pytest.param("3.14", "en_US.UTF-8", real_value.RealValue(3.14), id="3.14, en_US"),
        pytest.param("3,14", "deu_deu.UTF-8", real_value.RealValue(3.14), id="3.14, deu_deu"),
        pytest.param("1.79769313486232E+308", "en_US.UTF-8",
                     real_value.RealValue(1.79769313486232e+308), id="Max Value, en_US"),
        pytest.param("1,79769313486232E+308", "deu_deu.UTF-8",
                     real_value.RealValue(1.79769313486232e+308), id="Max Value, deu_deu"),
        pytest.param("-1.79769313486232E+308", "en_US.UTF-8",
                     real_value.RealValue(-1.79769313486232e+308), id="Min Value, en_US"),
        pytest.param("-1,79769313486232E+308", "deu_deu.UTF-8",
                     real_value.RealValue(-1.79769313486232e+308), id="Min Value, deu_deu"),
        pytest.param("-INF", "en_US.UTF-8", real_value.RealValue(np.NINF),
                     id="Neg Infinity, en_US"),
        pytest.param("-INF", "deu_deu.UTF-8", real_value.RealValue(np.NINF),
                     id="Neg Infinity, deu_deu"),
        pytest.param("NAN", "en_US.UTF-8", real_value.RealValue(np.nan), id="NAN, en_US"),
        pytest.param("NAN", "deu_deu.UTF-8", real_value.RealValue(np.nan), id="NAN, deu_deu"),
        # Note that epsilon can vary between systems, so this is just testing tiny values
        pytest.param("2.2250738585072E-308", "en_US.UTF-8",
                     real_value.RealValue(2.2250738585072e-308), id="Epsilon, en_US"),
        pytest.param("2,2250738585072E-308", "deu_deu.UTF-8",
                     real_value.RealValue(2.2250738585072e-308), id="Epsilon, deu_deu")
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
        pytest.param("True", "en_US.UTF-8", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("True", "deu_deu.UTF-8", boolean_value.BooleanValue(np.True_), id="True, deu_deu"),
        pytest.param("False", "en_US.UTF-8", boolean_value.BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("False", "deu_deu.UTF-8", boolean_value.BooleanValue(np.False_),
                     id="False, deu_deu"),
        pytest.param("Yes", "en_US.UTF-8", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("Yes", "deu_deu.UTF-8", boolean_value.BooleanValue(np.True_), id="True, deu_deu"),
        pytest.param("On", "en_US.UTF-8", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("On", "deu_deu.UTF-8", boolean_value.BooleanValue(np.True_), id="True, deu_deu"),
        pytest.param("1", "en_US.UTF-8", boolean_value.BooleanValue(np.True_), id="True, en_US"),
        pytest.param("1", "deu_deu.UTF-8", boolean_value.BooleanValue(np.True_), id="True, deu_deu"),
        pytest.param("No", "en_US.UTF-8", boolean_value.BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("No", "deu_deu.UTF-8", boolean_value.BooleanValue(np.False_),
                     id="False, deu_deu"),
        pytest.param("Off", "en_US.UTF-8", boolean_value.BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("Off", "deu_deu.UTF-8", boolean_value.BooleanValue(np.False_),
                     id="False, deu_deu"),
        pytest.param("0", "en_US.UTF-8", boolean_value.BooleanValue(np.False_), id="False, en_US"),
        pytest.param("0", "deu_deu.UTF-8", boolean_value.BooleanValue(np.False_), id="False, deu_deu")
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
        pytest.param("foo", "en_US.UTF-8", string_value.StringValue("foo"), id="foo, en_US"),
        pytest.param("foo", "deu_deu.UTF-8", string_value.StringValue("foo"), id="foo, deu_deu"),
        pytest.param("", "en_US.UTF-8", string_value.StringValue(""), id="Empty, en_US"),
        pytest.param("", "deu_deu.UTF-8", string_value.StringValue(""), id="Empty, deu_deu"),
        pytest.param("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", "en_US.UTF-8",
                     string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     id="Unicode, en_US"),
        pytest.param("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", "deu_deu.UTF-8",
                     string_value.StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     id="Unicode, deu_deu"),
        pytest.param("Escapes>\n\r\t\\\"<", "en_US.UTF-8",
                     string_value.StringValue("Escapes>\n\r\t\\\"<"), id="Escapes, en_US"),
        pytest.param("Escapes>\n\r\t\\\"<", "deu_deu.UTF-8",
                     string_value.StringValue("Escapes>\n\r\t\\\"<"), id="Escapes, deu_deu")
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
