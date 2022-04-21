"""Configuration for tests."""
import pytest


@pytest.fixture
def anyio_backend():
    """
    Defines the backends async tests are run on.

    Returns
    -------
    The backends to run async tests on.
    """
    return 'asyncio'
