"""Unit tests of FromFormattedStringVisitor."""

import numpy as np
import pytest

from ansys.common.variableinterop import (
    BooleanArrayValue,
    BooleanValue,
    FromFormattedStringVisitor,
    IntegerArrayValue,
    IntegerValue,
    RealArrayValue,
    RealValue,
    StringArrayValue,
    StringValue,
)


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("-1", "en_US.UTF-8", IntegerValue(-1), id="-1, en_US"),
        pytest.param("-1", "de_DE.UTF-8", IntegerValue(-1), id="-1, de_DE"),
        pytest.param("+1", "en_US.UTF-8", IntegerValue(1), id="1, en_US"),
        pytest.param("+1", "de_DE.UTF-8", IntegerValue(1), id="1, de_DE"),
        pytest.param("9.22337E+18", "en_US.UTF-8", IntegerValue(9223370000000000000),
                     id="Max Int, en_US"),
        pytest.param("9,22337E+18", "de_DE.UTF-8", IntegerValue(9223370000000000000),
                     id="Max Int, de_DE"),
        pytest.param("-9.22337E+18", "en_US.UTF-8",
                     IntegerValue(-9223370000000000000), id="Min Int, en_US"),
        pytest.param("-9,22337E+18", "de_DE.UTF-8",
                     IntegerValue(-9223370000000000000), id="Min Int, de_DE")
    ]
)
def test_converting_from_an_integer(value: str,
                                    locale: str,
                                    expected: IntegerValue) -> None:
    """
    Verifies the conversion of various strings to IntegerValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: IntegerValue = visitor.visit_int()

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("0", "en_US.UTF-8", RealValue(0), id="0, en_US"),
        pytest.param("0", "de_DE.UTF-8", RealValue(0), id="0, de_DE"),
        pytest.param("3", "en_US.UTF-8", RealValue(3), id="3, en_US"),
        pytest.param("3", "de_DE.UTF-8", RealValue(3), id="3, de_DE"),
        pytest.param("3.14", "en_US.UTF-8", RealValue(3.14), id="3.14, en_US"),
        pytest.param("3,14", "de_DE.UTF-8", RealValue(3.14), id="3.14, de_DE"),
        pytest.param("1.79769313486232E+308", "en_US.UTF-8",
                     RealValue(1.79769313486232e+308), id="Max Value, en_US"),
        pytest.param("1,79769313486232E+308", "de_DE.UTF-8",
                     RealValue(1.79769313486232e+308), id="Max Value, de_DE"),
        pytest.param("-1.79769313486232E+308", "en_US.UTF-8",
                     RealValue(-1.79769313486232e+308), id="Min Value, en_US"),
        pytest.param("-1,79769313486232E+308", "de_DE.UTF-8",
                     RealValue(-1.79769313486232e+308), id="Min Value, de_DE"),
        pytest.param("-INF", "en_US.UTF-8", RealValue(np.NINF),
                     id="Neg Infinity, en_US"),
        pytest.param("-INF", "de_DE.UTF-8", RealValue(np.NINF),
                     id="Neg Infinity, de_DE"),
        pytest.param("NAN", "en_US.UTF-8", RealValue(np.nan), id="NAN, en_US"),
        pytest.param("NAN", "de_DE.UTF-8", RealValue(np.nan), id="NAN, de_DE"),
        # Note that epsilon can vary between systems, so this is just testing tiny values
        pytest.param("2.2250738585072E-308", "en_US.UTF-8",
                     RealValue(2.2250738585072e-308), id="Epsilon, en_US"),
        pytest.param("2,2250738585072E-308", "de_DE.UTF-8",
                     RealValue(2.2250738585072e-308), id="Epsilon, de_DE")
    ]
)
def test_converting_from_a_real(value: str,
                                locale: str,
                                expected: RealValue) -> None:
    """
    Verifies the conversion of various strings to RealValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: RealValue = visitor.visit_real()

    # Verification
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("True", "en_US.UTF-8", BooleanValue(np.True_), id="True, en_US"),
        pytest.param("True", "de_DE.UTF-8", BooleanValue(np.True_), id="True, de_DE"),
        pytest.param("False", "en_US.UTF-8", BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("False", "de_DE.UTF-8", BooleanValue(np.False_),
                     id="False, de_DE"),
        pytest.param("Yes", "en_US.UTF-8", BooleanValue(np.True_), id="True, en_US"),
        pytest.param("Yes", "de_DE.UTF-8", BooleanValue(np.True_), id="True, de_DE"),
        pytest.param("On", "en_US.UTF-8", BooleanValue(np.True_), id="True, en_US"),
        pytest.param("On", "de_DE.UTF-8", BooleanValue(np.True_), id="True, de_DE"),
        pytest.param("1", "en_US.UTF-8", BooleanValue(np.True_), id="True, en_US"),
        pytest.param("1", "de_DE.UTF-8", BooleanValue(np.True_), id="True, de_DE"),
        pytest.param("No", "en_US.UTF-8", BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("No", "de_DE.UTF-8", BooleanValue(np.False_),
                     id="False, de_DE"),
        pytest.param("Off", "en_US.UTF-8", BooleanValue(np.False_),
                     id="False, en_US"),
        pytest.param("Off", "de_DE.UTF-8", BooleanValue(np.False_),
                     id="False, de_DE"),
        pytest.param("0", "en_US.UTF-8", BooleanValue(np.False_), id="False, en_US"),
        pytest.param("0", "de_DE.UTF-8", BooleanValue(np.False_), id="False, de_DE")
    ]
)
def test_converting_from_a_boolean(value: str,
                                   locale: str,
                                   expected: BooleanValue) -> None:
    """
    Verifies the conversion of various strings to BooleanValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: BooleanValue = visitor.visit_boolean()

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("foo", "en_US.UTF-8", StringValue("foo"), id="foo, en_US"),
        pytest.param("foo", "de_DE.UTF-8", StringValue("foo"), id="foo, de_DE"),
        pytest.param("", "en_US.UTF-8", StringValue(""), id="Empty, en_US"),
        pytest.param("", "de_DE.UTF-8", StringValue(""), id="Empty, de_DE"),
        pytest.param("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", "en_US.UTF-8",
                     StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     id="Unicode, en_US"),
        pytest.param("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪", "de_DE.UTF-8",
                     StringValue("Unicode: AÇĎȄЖउႴ〣倊瀇选뀋퀍𝓝𠀠𢀣𤀤𦀦𨀨𪀪"),
                     id="Unicode, de_DE"),
        pytest.param("Escapes>\n\r\t\\\"<", "en_US.UTF-8",
                     StringValue("Escapes>\n\r\t\\\"<"), id="Escapes, en_US"),
        pytest.param("Escapes>\n\r\t\\\"<", "de_DE.UTF-8",
                     StringValue("Escapes>\n\r\t\\\"<"), id="Escapes, de_DE")
    ]
)
def test_converting_from_a_string(value: str,
                                  locale: str,
                                  expected: StringValue) -> None:
    """
    Verifies the conversion of various strings to StringValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: StringValue = visitor.visit_string()

    # Verification
    assert result == expected


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("1,2,3", "en_US.UTF-8", IntegerArrayValue((1, 3), [1, 2, 3]),
                     id="Single dim, en_US"),
        pytest.param("1,2,3", "de_DE.UTF-8", IntegerArrayValue((1, 3), [1, 2, 3]),
                     id="Single dim, de_DE"),
        pytest.param("bounds[4,1]{100,1000,10000,10}", "en_US.UTF-8",
                     IntegerArrayValue((4, 1), [[100], [1000], [10000], [10]]),
                     id="Multi dim, en_US"),
        pytest.param("bounds[4,1]{100,1000,10000,10}", "de_DE.UTF-8",
                     IntegerArrayValue((4, 1), [[100], [1000], [10000], [10]]),
                     id="Multi dim, de_DE"),
    ]
)
def test_converting_from_an_integer_array(value: str,
                                          locale: str,
                                          expected: IntegerArrayValue) -> None:
    """
    Verifies the conversion of various strings to IntegerArrayValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: IntegerArrayValue = visitor.visit_int_array()

    # Verification
    assert np.array_equal(result, expected)


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("5,4,3.25", "en_US.UTF-8", RealArrayValue((1, 3), [5, 4, 3.25]),
                     id="Single dim, en_US"),
        pytest.param("\"5\",\"4\",\"3,25\"", "de_DE.UTF-8", RealArrayValue((1, 3), [5, 4, 3.25]),
                     id="Single dim, de_DE"),
        pytest.param("bounds[2,3]{50.5,101.1,233.45,1.1,2.2,3.3}",
                     "en_US.UTF-8",
                     RealArrayValue((2, 3), [[50.5, 101.1, 233.45], [1.1, 2.2, 3.3]]),
                     id="Multi dim, en_US"),
        pytest.param("bounds[2,3]{\"50,5\",\"101,1\",\"233,45\",\"1,1\",\"2,2\",\"3,3\"}",
                     "de_DE.UTF-8",
                     RealArrayValue((2, 3), [[50.5, 101.1, 233.45], [1.1, 2.2, 3.3]]),
                     id="Multi dim, de_DE"),
    ]
)
def test_converting_from_a_real_array(value: str,
                                      locale: str,
                                      expected: RealArrayValue) -> None:
    """
    Verifies the conversion of various strings to RealArrayValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: RealArrayValue = visitor.visit_real_array()

    # Verification
    assert np.array_equal(result, expected)


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("True,False,True", "en_US.UTF-8",
                     BooleanArrayValue((1, 3), [np.True_, np.False_, np.True_]),
                     id="Single dim, en_US"),
        pytest.param("True,False,True", "de_DE.UTF-8",
                     BooleanArrayValue((1, 3), [np.True_, np.False_, np.True_]),
                     id="Single dim, de_DE"),
        pytest.param("bounds[3,2]{True,False,False,True,True,True}",
                     "en_US.UTF-8",
                     BooleanArrayValue((3, 2), [[np.True_, np.False_], [np.False_, np.True_],
                                                [np.True_, np.True_]]),
                     id="Multi dim, en_US"),
        pytest.param("bounds[3,2]{True,False,False,True,True,True}",
                     "de_DE.UTF-8",
                     BooleanArrayValue((3, 2), [[np.True_, np.False_], [np.False_, np.True_],
                                                [np.True_, np.True_]]),
                     id="Multi dim, de_DE"),
    ]
)
def test_converting_from_a_boolean_array(value: str,
                                         locale: str,
                                         expected: BooleanArrayValue) -> None:
    """
    Verifies the conversion of various strings to BooleanArrayValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: BooleanArrayValue = visitor.visit_bool_array()

    # Verification
    assert np.array_equal(result, expected)


@pytest.mark.parametrize(
    "value,locale,expected",
    [
        pytest.param("\"one\",\"two\",\"three\"", "en_US.UTF-8",
                     StringArrayValue((1, 3), ["one", "two", "three"]), id="Single dim, en_US"),
        pytest.param("\"one\",\"two\",\"three\"", "de_DE.UTF-8",
                     StringArrayValue((1, 3), ["one", "two", "three"]), id="Single dim, de_DE"),
        pytest.param("bounds[2,2]{\"one_one\",\"one_two\",\"two_one\",\"two_two\"}",
                     "en_US.UTF-8",
                     StringArrayValue((2, 2), [["one_one", "one_two"], ["two_one", "two_two"]]),
                     id="Multi dim, en_US"),
        pytest.param("bounds[2,2]{\"one_one\",\"one_two\",\"two_one\",\"two_two\"}",
                     "de_DE.UTF-8",
                     StringArrayValue((2, 2), [["one_one", "one_two"], ["two_one", "two_two"]]),
                     id="Multi dim, de_DE"),
    ]
)
def test_converting_from_a_string_array(value: str,
                                        locale: str,
                                        expected: StringArrayValue) -> None:
    """
    Verifies the conversion of various strings to StringArrayValues.

    Parameters
    ----------
    value The value to format.
    locale The locale to format in.
    expected The expected output.
    """
    # Setup
    visitor = FromFormattedStringVisitor(value, locale)

    # SUT
    result: StringArrayValue = visitor.visit_string_array()

    # Verification
    assert np.array_equal(result, expected)
