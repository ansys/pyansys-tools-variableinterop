from ansys.common import variableinterop


def test_pkg_version():
    assert variableinterop.__version__ == "0.1.dev0"
