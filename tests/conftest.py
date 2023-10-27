"""Configuration for tests."""
import pytest


@pytest.fixture
def anyio_backend() -> str:
    """
    Define the backends async tests are run on.

    Returns
    -------
    str
        The backends to run async tests on.
    """
    return "asyncio"
