from typing import Any

import numpy
import pytest

from ansys.common.variableinterop import BooleanValue


@pytest.mark.parametrize(
    "arg,expect_equality",
    [
        pytest.param(True, numpy.bool_(True), id="true"),
        pytest.param(False, numpy.bool_(False), id="false"),
        pytest.param(None, numpy.bool_(False), id="none"),

        # TODO: Should we even accept strings?
        pytest.param("", numpy.bool_(False), id="empty-string"),
        pytest.param("something", numpy.bool_(True), id="non-empty-string"),
        pytest.param("false", numpy.bool_(True), id="non-empty-string-says-false"),
    ])
def test_construct(arg: Any, expect_equality: numpy.bool_) -> None:
    """Verify that __init__ for BooleanValue correctly instantiates the superclass data"""
    instance: BooleanValue = BooleanValue(arg)
    assert instance == expect_equality
