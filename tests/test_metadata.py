from ansys.common import variableinterop


def test_pkg_version() -> None:
    assert variableinterop.__version__ == "0.1.dev0"
