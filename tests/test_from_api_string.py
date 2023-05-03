from typing import Type

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.tools.variableinterop import (
    BooleanArrayValue,
    BooleanValue,
    IntegerArrayValue,
    IntegerValue,
    IVariableValue,
    RealArrayValue,
    RealValue,
    StringArrayValue,
    StringValue,
    VariableType,
    from_api_string,
)


@pytest.mark.parametrize(
    "var_type,source,expected_result",
    [
        pytest.param(VariableType.REAL, "4.5", RealValue(4.5), id="basic real, positive"),
        pytest.param(VariableType.REAL, "-4.5", RealValue(-4.5), id="basic real, negative"),
        pytest.param(VariableType.REAL, "0", RealValue(0), id="zero"),
        pytest.param(
            VariableType.REAL,
            "2.8E8",
            RealValue(2.8e8),
            id="sci notation real, positive, capital E",
        ),
        pytest.param(
            VariableType.REAL,
            "-2.8E8",
            RealValue(-2.8e8),
            id="sci notation real, negative, capital E",
        ),
        pytest.param(
            VariableType.REAL,
            "2.8e8",
            RealValue(2.8e8),
            id="sci notation real, positive, lowercase e",
        ),
        pytest.param(
            VariableType.REAL,
            "2.8e-8",
            RealValue(2.8e-8),
            id="sci notation real, negative-exponent",
        ),
        pytest.param(VariableType.REAL, ".4", RealValue(0.4), id="real, no leading zero"),
        pytest.param(VariableType.REAL, "4.0", RealValue(4.0), id="real, whole number, point zero"),
        pytest.param(
            VariableType.REAL, "4.", RealValue(4.0), id="real, whole number, decimal, no zero"
        ),
        pytest.param(VariableType.REAL, "4", RealValue(4), id="real, whole number, no decimal"),
        pytest.param(VariableType.REAL, "+4.7", RealValue(4.7), id="real, explicit positive"),
        pytest.param(
            VariableType.REAL,
            "1.7976931348623157e+308",
            RealValue(1.7976931348623157e308),
            id="real, absolute maximum",
        ),
        pytest.param(
            VariableType.REAL,
            "-1.7976931348623157e+308",
            RealValue(-1.7976931348623157e308),
            id="real, absolute minimum",
        ),
        pytest.param(
            VariableType.REAL,
            "2.2250738585072014e-308",
            RealValue(2.2250738585072014e-308),
            id="real, epsilon",
        ),
        pytest.param(VariableType.REAL, "Inf", RealValue(numpy.float64("inf")), id="real, Inf"),
        pytest.param(VariableType.REAL, "inf", RealValue(numpy.float64("inf")), id="real, inf"),
        pytest.param(VariableType.REAL, "INF", RealValue(numpy.float64("inf")), id="real, INF"),
        pytest.param(
            VariableType.REAL, "Infinity", RealValue(numpy.float64("inf")), id="real, Infinity"
        ),
        pytest.param(
            VariableType.REAL, "infinity", RealValue(numpy.float64("inf")), id="real, infinity"
        ),
        pytest.param(
            VariableType.REAL, "INFINITY", RealValue(numpy.float64("inf")), id="real, INFINITY"
        ),
        pytest.param(
            VariableType.REAL, "-Inf", RealValue(numpy.float64("-inf")), id="negative Inf"
        ),
        pytest.param(
            VariableType.REAL, "-inf", RealValue(numpy.float64("-inf")), id="negative inf"
        ),
        pytest.param(
            VariableType.REAL, "-INF", RealValue(numpy.float64("-inf")), id="negative INF"
        ),
        pytest.param(
            VariableType.REAL, "-Infinity", RealValue(numpy.float64("-inf")), id="negative Infinity"
        ),
        pytest.param(
            VariableType.REAL, "-infinity", RealValue(numpy.float64("-inf")), id="negative infinity"
        ),
        pytest.param(
            VariableType.REAL, "-INFINITY", RealValue(numpy.float64("-inf")), id="negative INFINITY"
        ),
        pytest.param(
            VariableType.REAL,
            "1.7976931348623157e+309",
            RealValue(numpy.float64("Inf")),
            id="real, over maximum",
        ),
        pytest.param(
            VariableType.REAL,
            "-1.7976931348623157e+309",
            RealValue(numpy.float64("-Inf")),
            id="real, under minimum",
        ),
        pytest.param(VariableType.REAL, "NaN", RealValue(numpy.float64("NaN")), id="real, NaN"),
        pytest.param(VariableType.REAL, "nan", RealValue(numpy.float64("NaN")), id="real, nan"),
        pytest.param(VariableType.INTEGER, "0", IntegerValue(0), id="integer, zero"),
        pytest.param(VariableType.INTEGER, "1", IntegerValue(1), id="integer, one"),
        pytest.param(VariableType.INTEGER, "-1", IntegerValue(-1), id="integer, negative one"),
        pytest.param(
            VariableType.INTEGER, "+42", IntegerValue(42), id="integer, explicit positive"
        ),
        pytest.param(VariableType.INTEGER, "8675309", IntegerValue(8675309), id="integer, larger"),
        pytest.param(VariableType.INTEGER, "047", IntegerValue(47), id="integer, leading zero"),
        pytest.param(
            VariableType.INTEGER,
            "1.2E2",
            IntegerValue(120),
            id="integer, scientific notation, whole",
        ),
        pytest.param(
            VariableType.INTEGER,
            "-1.2E2",
            IntegerValue(-120),
            id="integer, scientific notation, whole, negative",
        ),
        pytest.param(
            VariableType.INTEGER,
            "1.2e+2",
            IntegerValue(120),
            id="integer, scientific notation, lowercase e, explicit positive exponent",
        ),
        pytest.param(
            VariableType.INTEGER,
            "\t\n\r 8675309",
            IntegerValue(8675309),
            id="integer, leading whitespace",
        ),
        pytest.param(
            VariableType.INTEGER,
            "8675309 \t\n\r",
            IntegerValue(8675309),
            id="integer, trailing whitespace",
        ),
        pytest.param(
            VariableType.INTEGER,
            "\r\n\t 8675309 \t\n\r",
            IntegerValue(8675309),
            id="integer, leading and trailing whitespace",
        ),
        pytest.param(
            VariableType.INTEGER,
            "9223372036854775807",
            IntegerValue(9223372036854775807),
            id="integer, max 64 bit",
        ),
        pytest.param(
            VariableType.INTEGER,
            "-9223372036854775808",
            IntegerValue(-9223372036854775808),
            id="integer, min 64 bit",
        ),
        pytest.param(
            VariableType.INTEGER,
            "9.223372036854775200E+18",
            IntegerValue(9223372036854774784),
            id="integer, largest float",
        ),
        pytest.param(
            VariableType.INTEGER,
            "-9.223372036854776000E+18",
            IntegerValue(-9223372036854775808),
            id="integer, smallest float",
        ),
        # non-integral numbers with decimals should be rounded
        pytest.param(VariableType.INTEGER, "1.5", IntegerValue(2), id="integer, rounding, to even"),
        # rounding should occur away from zero, not to the nearest even
        pytest.param(VariableType.INTEGER, "2.5", IntegerValue(3), id="integer, rounding, to odd"),
        # rounding should occur away from zero, not strictly up
        pytest.param(
            VariableType.INTEGER, "-1.5", IntegerValue(-2), id="integer, rounding, to odd, negative"
        ),
        # rounding should occur away from zero, not to the nearest even
        pytest.param(
            VariableType.INTEGER,
            "-2.5",
            IntegerValue(-3),
            id="integer, rounding, to even, negative",
        ),
        pytest.param(VariableType.BOOLEAN, "True", BooleanValue(True), id="boolean, True"),
        pytest.param(VariableType.BOOLEAN, "TRUE", BooleanValue(True), id="boolean, TRUE"),
        pytest.param(VariableType.BOOLEAN, "true", BooleanValue(True), id="boolean, true"),
        pytest.param(VariableType.BOOLEAN, "TrUe", BooleanValue(True), id="boolean, TrUe"),
        pytest.param(VariableType.BOOLEAN, "False", BooleanValue(False), id="boolean, False"),
        pytest.param(VariableType.BOOLEAN, "FALSE", BooleanValue(False), id="boolean, FALSE"),
        pytest.param(VariableType.BOOLEAN, "false", BooleanValue(False), id="boolean, false"),
        pytest.param(VariableType.BOOLEAN, "FaLsE", BooleanValue(False), id="boolean, FaLsE"),
        pytest.param(VariableType.BOOLEAN, "Yes", BooleanValue(True), id="boolean, Yes"),
        pytest.param(VariableType.BOOLEAN, "YES", BooleanValue(True), id="boolean, YES"),
        pytest.param(VariableType.BOOLEAN, "y", BooleanValue(True), id="boolean, y"),
        pytest.param(VariableType.BOOLEAN, "Y", BooleanValue(True), id="boolean, Y"),
        pytest.param(VariableType.BOOLEAN, "No", BooleanValue(False), id="boolean, No"),
        pytest.param(VariableType.BOOLEAN, "no", BooleanValue(False), id="boolean, no"),
        pytest.param(VariableType.BOOLEAN, "n", BooleanValue(False), id="boolean, n"),
        pytest.param(VariableType.BOOLEAN, "N", BooleanValue(False), id="boolean, N"),
        pytest.param(VariableType.BOOLEAN, "0", BooleanValue(False), id="boolean, zero"),
        pytest.param(
            VariableType.BOOLEAN, "0.0", BooleanValue(False), id="boolean, zero point zero"
        ),
        pytest.param(VariableType.BOOLEAN, "1", BooleanValue(True), id="boolean, one point zero"),
        pytest.param(VariableType.BOOLEAN, "1.0", BooleanValue(True), id="boolean, one point zero"),
        pytest.param(
            VariableType.BOOLEAN,
            "true \r\n\t",
            BooleanValue(True),
            id="boolean, trailing whitespace true",
        ),
        pytest.param(
            VariableType.BOOLEAN,
            "false \r\n\t",
            BooleanValue(False),
            id="boolean, trailing whitespace false",
        ),
        pytest.param(
            VariableType.BOOLEAN,
            "\r\n\t true",
            BooleanValue(True),
            id="boolean, leading whitespace true",
        ),
        pytest.param(
            VariableType.BOOLEAN,
            "\r\n\t false",
            BooleanValue(False),
            id="boolean, leading whitespace false",
        ),
        pytest.param(VariableType.BOOLEAN, "NaN", BooleanValue(True), id="boolean, NaN"),
        pytest.param(VariableType.BOOLEAN, "Infinity", BooleanValue(True), id="boolean, infinity"),
        pytest.param(
            VariableType.BOOLEAN, "-Infinity", BooleanValue(True), id="boolean, negative infinity"
        ),
        pytest.param(VariableType.STRING, "", StringValue(""), id="string, empty"),
        pytest.param(
            VariableType.STRING, " \t\r\n", StringValue(" \t\r\n"), id="string, whitespace only"
        ),
        pytest.param(
            VariableType.STRING,
            "ASCII-only",
            StringValue("ASCII-only"),
            id="string, ascii-codespace",
        ),
        pytest.param(
            VariableType.STRING,
            "(ノ-_-)ノ ミᴉᴉɔsɐ-uou",
            StringValue("(ノ-_-)ノ ミᴉᴉɔsɐ-uou"),
            id="string, unicode-codespace",
        ),
        pytest.param(
            VariableType.STRING,
            'Escapes>\n\r\t\\"<',
            StringValue('Escapes>\n\r\t\\"<'),
            id="string, characters escaped in formatted string unmodified",
        ),
        pytest.param(
            VariableType.BOOLEAN_ARRAY,
            "True",
            BooleanArrayValue(values=[True]),
            id="boolean array, 0d",
        ),
        pytest.param(
            VariableType.BOOLEAN_ARRAY,
            "False,True,False",
            BooleanArrayValue(values=[False, True, False]),
            id="boolean array, 1d",
        ),
        pytest.param(
            VariableType.BOOLEAN_ARRAY,
            "bounds[2,1]{True,False}",
            BooleanArrayValue(values=[[True], [False]]),
            id="boolean array, 2d",
        ),
        pytest.param(
            VariableType.BOOLEAN_ARRAY,
            " bounds [ 2 , 1 ] { True , False } ",
            BooleanArrayValue(values=[[True], [False]]),
            id="boolean array, 2d with spaces",
        ),
        pytest.param(
            VariableType.BOOLEAN_ARRAY,
            "Bounds[2,1]{true,FALSE}",
            BooleanArrayValue(values=[[True], [False]]),
            id="boolean array, 2d case variations",
        ),
        pytest.param(
            VariableType.BOOLEAN_ARRAY,
            "bounds[2,2,3]{False,True,False,True,False,True,False,False,True,True,False,\
                     False}",
            BooleanArrayValue(
                values=[
                    [[False, True, False], [True, False, True]],
                    [[False, False, True], [True, False, False]],
                ]
            ),
            id="boolean array, 3d",
        ),
        pytest.param(
            VariableType.INTEGER_ARRAY, "42", IntegerArrayValue(values=[42]), id="int array, 0d"
        ),
        pytest.param(
            VariableType.INTEGER_ARRAY,
            "1,2,3",
            IntegerArrayValue(values=[1, 2, 3]),
            id="int array, 1d",
        ),
        pytest.param(
            VariableType.INTEGER_ARRAY,
            "bounds[2,2]{1,2,3,4}",
            IntegerArrayValue(values=[[1, 2], [3, 4]]),
            id="int array, 2d",
        ),
        pytest.param(
            VariableType.INTEGER_ARRAY,
            "bounds[2,2,3]{1,2,3,4,5,6,7,8,9,10,-11,-12}",
            IntegerArrayValue(values=[[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, -11, -12]]]),
            id="int array, 3d",
        ),
        pytest.param(
            VariableType.INTEGER_ARRAY,
            "-9223372036854775808,9223372036854775807",
            IntegerArrayValue(values=[-9223372036854775808, 9223372036854775807]),
            id="int array, 1d, min/max 64 bit",
        ),
        pytest.param(
            VariableType.REAL_ARRAY, "4.2", RealArrayValue(values=[4.2]), id="real array, 0d"
        ),
        pytest.param(
            VariableType.REAL_ARRAY,
            "3.14,4.25,5.36",
            RealArrayValue(values=[3.14, 4.25, 5.36]),
            id="real array, 1d",
        ),
        pytest.param(
            VariableType.REAL_ARRAY,
            "bounds[2,1]{1.7976931348623157e+308,-1.7976931348623157e+308}",
            RealArrayValue(values=[[1.7976931348623157e308], [-1.7976931348623157e308]]),
            id="real array, 2d",
        ),
        pytest.param(
            VariableType.REAL_ARRAY,
            "bounds[2,2,3]{1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,10.0,-11.1,-12.2}",
            RealArrayValue(
                values=[[[1.1, 2.2, 3.3], [4.4, 5.5, 6.6]], [[7.7, 8.8, 9.9], [10.0, -11.1, -12.2]]]
            ),
            id="real array, 3d",
        ),
        pytest.param(
            VariableType.STRING_ARRAY,
            '"uno","dos","tres"',
            StringArrayValue(values=["uno", "dos", "tres"]),
            id="string array, 1d",
        ),
        pytest.param(
            VariableType.STRING_ARRAY,
            'bounds[2,1]{"asdf","qwerty"}',
            StringArrayValue(values=[["asdf"], ["qwerty"]]),
            id="string array, 2d",
        ),
        pytest.param(
            VariableType.STRING_ARRAY,
            'bounds[2,2,3]{"あ","い","う","え","お","か",' + '"き","く","け","こ","が","ぎ"}',
            StringArrayValue(
                values=[[["あ", "い", "う"], ["え", "お", "か"]], [["き", "く", "け"], ["こ", "が", "ぎ"]]]
            ),
            id="string array, 3d",
        ),
    ],
)
def test_from_api_string_valid(
    var_type: VariableType, source: str, expected_result: IVariableValue
) -> None:
    """
    Verify that the static IVariableValue.from_api_string correctly produces values
    from valid input.

    Parameters
    ----------
    var_type : VariableType
        The variable type to pass.
    source : str
        The string to convert.
    expected_result : IVariableValue
        The expected result.
    """
    # Execute
    actual_result: IVariableValue = from_api_string(var_type, source)

    # Verify
    assert type(actual_result) is type(expected_result)

    if type(expected_result) is RealValue and numpy.isnan(expected_result):
        assert numpy.isnan(expected_result)
    else:
        assert actual_result == expected_result


@pytest.mark.parametrize(
    "var_type,source,expected_exception",
    [
        pytest.param(VariableType.REAL, "60Ɛϛ˙ㄥ98", ValueError, id="real, garbage"),
        pytest.param(VariableType.REAL, "1,204.5", ValueError, id="real, thousands separator"),
        pytest.param(VariableType.REAL, "1 204.5", ValueError, id="real, internal whitespace"),
        pytest.param(VariableType.REAL, "2.2.2", ValueError, id="real, multiple decimals"),
        pytest.param(VariableType.REAL, "true", ValueError, id="real, boolean literal"),
        pytest.param(VariableType.REAL, "", ValueError, id="real, empty string"),
        pytest.param(VariableType.REAL, None, TypeError, id="real, None"),
        pytest.param(
            VariableType.INTEGER, "complete garbage", ValueError, id="integer, complete garbage"
        ),
        pytest.param(VariableType.INTEGER, "", ValueError, id="integer, empty string"),
        pytest.param(VariableType.INTEGER, "    ", ValueError, id="integer, whitespace only"),
        pytest.param(VariableType.INTEGER, "2.2.2", ValueError, id="integer, too many decimals"),
        pytest.param(
            VariableType.INTEGER,
            "9.223372036854775300E+18",
            OverflowError,
            id="integer, valid float over max int",
        ),
        pytest.param(
            VariableType.INTEGER,
            "-9.223372036854777700E+18",
            OverflowError,
            id="integer, valid float under max int",
        ),
        pytest.param(
            VariableType.INTEGER,
            "1.7976931348623157e+309",
            OverflowError,
            id="integer, over max float64",
        ),
        pytest.param(
            VariableType.INTEGER,
            "-1.7976931348623157e+309",
            OverflowError,
            id="integer, under min float64",
        ),
        pytest.param(VariableType.INTEGER, "47b", ValueError, id="integer, extra characters"),
        pytest.param(VariableType.INTEGER, "NaN", ValueError, id="integer, NaN"),
        pytest.param(VariableType.INTEGER, "Infinity", ValueError, id="integer, Infinity"),
        pytest.param(
            VariableType.INTEGER, "-Infinity", ValueError, id="integer, negative Infinity"
        ),
        pytest.param(VariableType.INTEGER, "inf", ValueError, id="integer, inf"),
        pytest.param(VariableType.INTEGER, "-inf", ValueError, id="integer, negative inf"),
        pytest.param(VariableType.INTEGER, None, TypeError, id="integer, None"),
        pytest.param(VariableType.BOOLEAN, "", ValueError, id="boolean, empty"),
        pytest.param(VariableType.BOOLEAN, " \t\n\r", ValueError, id="boolean, all whitespace"),
        pytest.param(
            VariableType.BOOLEAN, "4,555", ValueError, id="boolean, Number with thousands separator"
        ),
        pytest.param(VariableType.BOOLEAN, None, TypeError, id="boolean, None"),
        pytest.param(VariableType.STRING, None, TypeError, id="string, None"),
    ],
)
def test_from_api_string_invalid(
    var_type: VariableType, source: str, expected_exception: Type[BaseException]
) -> None:
    """
    Verify that from_api_string raises the expected exception in

    Parameters
    ----------
    var_type : VariableType
        The variable type to pass.
    source : str
        The string to convert.
    expected_exception : Type[BaseException]
        The exception that is expected to be thrown.
    """
    with _create_exception_context(expected_exception):
        actual_result: IVariableValue = from_api_string(var_type, source)
