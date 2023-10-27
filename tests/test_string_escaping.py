import pytest

import ansys.tools.variableinterop as acvi


@pytest.mark.parametrize(
    "unescaped,expected_output",
    [
        pytest.param("", "", id="empty string"),
        pytest.param("no escaping necessary", "no escaping necessary", id="no escaping necessary"),
        pytest.param("whitespace>\t\r\n", r"whitespace>\t\r\n", id="escaped whitespace"),
        pytest.param('doublequote>"', r"doublequote>\"", id="quote"),
        pytest.param(r"backslash>\<", r"backslash>\\<", id="backslash"),
        pytest.param("null>\0<", r"null>\0<", id="null"),
    ],
)
def test_escape_string(unescaped: str, expected_output: str):
    output: str = acvi.escape_string(unescaped)

    assert isinstance(output, str)
    assert output == expected_output


@pytest.mark.parametrize(
    "escaped,expected_output",
    [
        pytest.param("", "", id="empty string"),
        pytest.param("no escaping necessary", "no escaping necessary", id="no escaping necessary"),
        pytest.param(r"whitespace>\t\r\n", "whitespace>\t\r\n", id="escaped whitespace"),
        pytest.param(r"doublequote>\"", 'doublequote>"', id="quote"),
        pytest.param(r"backslash>\\<", r"backslash>\<", id="backslash"),
        pytest.param(r"null>\0<", "null>\0<", id="null"),
        pytest.param(
            r"unr\ecogn\ized \esc\ap\es", "unrecognized escapes", id="drops unrecognized escapes"
        ),
    ],
)
def test_unescape_string(escaped: str, expected_output: str):
    output: str = acvi.unescape_string(escaped)

    assert isinstance(output, str)
    assert output == expected_output
