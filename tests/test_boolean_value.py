from typing import Any

import pytest
from test_utils import _create_exception_context

from ansys.common.variableinterop import BooleanValue, IncompatibleTypesException, VariableType


@pytest.mark.parametrize(
    "arg,expect_equality,expect_exception",
    [
        pytest.param(True, True, None, id="true"),
        pytest.param(False, False, None, id="false"),
        pytest.param(None, False, None, id="none"),

        # TODO: Should we even accept strings?
#       pytest.param(
#           "",
#           None,
#           IncompatibleTypesException("str", VariableType.BOOLEAN),
#           id="empty-string"),
#       pytest.param(
#           "something",
#           None,
#           IncompatibleTypesException("str", VariableType.BOOLEAN),
#           id="non-empty-string"),
#       pytest.param(
#           "false",
#           None,
#           IncompatibleTypesException("str", VariableType.Boolean),
#           id="non-empty-string-says-false"),
    ])
def test_construct(arg: Any, expect_equality: bool, expect_exception: BaseException) -> None:
    """Verify that __init__ for BooleanValue correctly instantiates the superclass data"""
    with _create_exception_context(expect_exception):
        instance: BooleanValue = BooleanValue(arg)
        assert instance == expect_equality
