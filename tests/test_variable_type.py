import pytest

from ansys.common.variableinterop import VariableType


@pytest.mark.parametrize(
    "inp,expected_result",
    [
        # Scalars
        pytest.param('int,integer,long', VariableType.INTEGER, id='valid INTEGER strings'),
        pytest.param('real,double,float', VariableType.REAL, id='valid REAL strings'),
        pytest.param('bool,boolean', VariableType.BOOLEAN, id='valid BOOLEAN strings'),
        pytest.param('str,string', VariableType.STRING, id='valid STRING strings'),
        pytest.param('file', VariableType.FILE, id='valid FILE strings'),

        # Arrays
        pytest.param('int[],integer[],long[]', VariableType.INTEGER_ARRAY,
                     id='valid INTEGER_ARRAY strings'),
        pytest.param('real[],double[],float[]', VariableType.REAL_ARRAY,
                     id='valid REAL_ARRAY strings'),
        pytest.param('bool[],boolean[]', VariableType.BOOLEAN_ARRAY,
                     id='valid BOOLEAN_ARRAY strings'),
        pytest.param('str[],string[]', VariableType.STRING_ARRAY,
                     id='valid STRING_ARRAY strings'),
        pytest.param('file[]', VariableType.FILE_ARRAY,
                     id='valid FILE_ARRAY strings'),

        # Some unknown examples
        pytest.param('ints,unknown,garbage[]', VariableType.UNKNOWN, id='unknown')
    ]
)
def test_var_type_from_string(inp: str, expected_result: VariableType):
    """
    Tests that VariableType.from_string() returns the correct type.

    Parameters
    ----------
    inp : str
        Input string. Can be a comma separated list to test multiple strings against the same
        expected result.
    expected_result : VariableType
        The expected resulting VariableType.
    """
    # Setup
    inputs = inp.split(',')

    # SUT
    results = (VariableType.from_string(i) for i in inputs)

    # Verify
    for result in results:
        assert result == expected_result
