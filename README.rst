PyAnsys Common Variable Interop
###############################


Project Overview
----------------
This library contains definitions of the basic variables, types,
metadata, and values intended to provide interoperability between
all Ansys products.
The top level items in this package are:

- The base metadata type that all variable types extend is
  CommonVariableMetadata. Metadata is defined as the information
  about a variable that is static and does not change when a
  component or workflow is run.
- The value interface is IVariableValue. These values are defined
  so they know how to properly convert from one type to the other
  via language operators, losslessly are implicitly. Operations
  that are lossy, such as converting a real to an integer value, are
  explicit. Explicit conversions may also throw an exception if
  there is an overflow or other "bad data" situation.


Installation
------------
The ``ansys-common-variableinterop`` package currently supports Python
3.8 through 3.10 on Windows and Linux.
This package is not currently available on PyPI, but will be when it is
ready for use.
At that time you can install ``ansys-common-variableinterop`` with:

.. code::

   pip install ansys-common-variableinterop

Alternatively, install the latest from `ansys-common-variableinterop GitHub
<https://github.com/pyansys/ansys-common-variableinterop>`_ via:

.. code::

   pip install git+https://github.com/pyansys/ansys-common-variableinterop.git

For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/ansys-common-variableinterop.git
   cd ansys-common-variableinterop
   pip install poetry
   poetry install -E dev

This creates a new virtual environment, which can be activated with

.. code::

   poetry shell

Documentation
-------------
TODO: link to the full sphinx documentation.
`ansys-common-variableinterop <https://common-variableinterop.docs.pyansys.com/>`_
For building documentation, you can run the usual rules provided in the Sphinx Makefile, such as:

.. code::

    make -C doc/ html && your_browser_name doc/html/index.html

on Unix, or:

.. code::

    .\doc\make.bat html

on Windows. Make sure the required dependencies are installed with:

.. code::

    pip install -E docs


Usage
-----
Values and metadata can be created like any other Python object:

.. code:: python

   >>> import ansys.common.variableinterop as acvi
   >>> width = acvi.RealValue(3.1)
   >>> width
   3.1

   # Standard python operations should work seamlessly
   >>> 4 + width
   7.1

   >>> width_metadata = acvi.RealMetadata()
   >>> width_metadata.lower_bound = 0.1
   >>> var(width_metadata)
   {'_description': '', '_custom_metadata': {}, '_units': '', '_display_format': '', '_lower_bound': 0.1, '_upper_bound': None, '_enumerated_values': [], '_enumerated_aliases': []}


Testing
-------
Dependencies required for testing can be installed via:

.. code::

    pip install -E test

The tests can then be run via pytest.


License
-------
ansys-common-variableinterop is licensed under the MIT license.
