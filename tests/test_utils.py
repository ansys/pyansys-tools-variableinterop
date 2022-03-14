from contextlib import contextmanager

import pytest

# TODO: search google, is there a standard way to do this?


@contextmanager
def _dummy_context():
    """
    A dummy context that does nothing so we can always use a with
    statement, even if one isn't needed.
    """
    yield None


def _create_exception_context(expect_exception: BaseException):
    """
    Creates an object to use in a with block that will test for expect_exception
    to be thrown, or does nothing if expect_exception is None

    Parameters
    ----------
    expect_exception The exception to expect, or None for not expecting an exception

    Returns
    -------
    A context to use in a with block that will validate the expected exception
    """
    if expect_exception is not None:
        return pytest.raises(expect_exception)
    else:
        return _dummy_context()
