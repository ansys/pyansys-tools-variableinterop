from typing import Any

import numpy
import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import IntegerValue


@pytest.mark.parametrize(
    "arg,expect_equality,expect_exception",
    [
        pytest.param(0, numpy.int64(0), None, id="zero"),
        pytest.param(1, numpy.int64(1), None, id="one"),
        pytest.param(-1, numpy.int64(-1), None, id="negative-one"),
        pytest.param(9223372036854775807, numpy.int64(9223372036854775807), None, id="max"),
        pytest.param(-9223372036854775808, numpy.int64(-9223372036854775808), None, id="min"),
        pytest.param(9223372036854775808, None, OverflowError, id="max+1"),
        pytest.param(-9223372036854775809, None, OverflowError, id="min-1"),
        pytest.param(1.4, numpy.int64(1), None, id="1.4-to-1"),

        # TODO: Should we override the numpy behavior for any of these cases?
        pytest.param(None, None, TypeError, id="None"),
        pytest.param(1.6, numpy.int64(1), None, id="1.6-to-1"),
        pytest.param(True, numpy.int64(1), None, id="True-to-1"),
        pytest.param(False, numpy.int64(0), None, id="False-to-0"),

        # TODO: Should we support string representations at all?
        # Should we pass-through to numpy, mimic fromAPIString, mimic fromFormattedString?
        pytest.param('some garbage text', None, ValueError, id="garbage-text"),
        pytest.param('-1', numpy.int64(-1), None, id="negative-one-text"),
        pytest.param('1', numpy.int64(1), None, id="one-text"),
    ])
def test_construct(arg: Any, expect_equality: numpy.int64, expect_exception: BaseException) -> None:
    """Verify that __init__ for IntegerValue correctly instantiates the superclass data."""
    with _create_exception_context(expect_exception):
        instance = IntegerValue(arg)

        if expect_exception is None:
            assert instance == expect_equality