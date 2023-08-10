"""
This library contains definitions of the basic variables, types, \ metadata, and values
intended to provide interoperability between \ all products that optionally choose to
participate.

See the high level project documentation with examples and installation instructions at
`
http://variableinterop.docs.pyansys.com
<http://variableinterop.docs.pyansys.com>`_.
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("ansys.tools.variableinterop")
"""ansys.tools.variableinterop version."""
