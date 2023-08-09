PyAnsys Common Variable Interop
###############################


Project Overview
----------------
This library contains definitions of the basic variables, types,
metadata, and values intended to provide interoperability between
all products that optionally choose to participate.

**Work in Progress**

This library is a work in progress and has not been released yet.
It still has unfinished documentation and APIs are not guaranteed
to be stable yet.

Characteristics
---------------
Characteristics of this library include:

- Minimal but complete set of formally defined data types for engineering work
- Standard base implementation in each supported language that matches the style and intent of
  the given language
- Follows and implements the standards in TODO: Add reference to standards doc
- Provides the following capabilities

  - to/from "API" string (not intended for UI layer, allows data transfer in human readable format
    across products and regions)
  - to/from human display strings
  - to/from binary blocks that are platform agnostic
  - implicit conversion to/from language primitives for lossless conversions. Explicit conversion
    for lossy conversions

- A data type library can either make it easy to add new data types or make it easy to add new
  operations to the existing data types. It is extremely hard to make both possible at the same
  time. This library uses the `visitor pattern <https://en.wikipedia.org/wiki/Visitor_pattern>`_ to
  make it easy and reliable to add and reuse
  new operations with compile-time semantics.
- In trade, adding new datatypes is not easy
- Most commonly re-used metadata strongly defined. Generic dictionary provided for custom metadata

Top Level Items
---------------
The top level items in this package are:

* The base metadata type that all variable types extend is
  CommonVariableMetadata. Metadata is defined as the information
  about a variable that is static and does not change when a
  component or workflow is run.
* The value interface is IVariableValue. These values are defined
  so they know how to properly convert from one type to the other
  via language operators. Lossless conversions are implicit. Operations
  that are lossy, such as converting a real to an integer value, are
  explicit. Explicit conversions may also throw an exception if
  there is an overflow or other "bad data" situation.

Project Background
------------------
After 20 years of working on integration problems a holistic review was performed around the
concept of a variable in some legacy codebases. No less than 2 dozen classes that represent a
variable were found. There were many more switch statements where one datatype needed to be
converted to another. This inconsistency brings about the following problems:

- The behavior of one capability within the product suite does not match that of other
  capabilities - leading to confusion, bugs, and lost time
- Switch statements are notorious for introducing bugs. People tend to cut-n-paste them, leading
  to subtle maintenance issues as one is modified and the other diverges. There is no compile-time
  type checking.
- Slight differences datatypes (int32 vs int64) can lead to unexpected bugs, including disastrous
  "bad data with no error" class issues.
- Seemingly simple tasks like reliably converting to string or byte buffer and back are
  surprisingly hard to do correct in all the edge cases. Worse, even if you get a "correct"
  implementation, if it doesn't match what is used at an API boundary by a different capability
  or product, errors ensue.

The standards and the standard implementations in several languages came out of this review.

Installation
------------
The ``pyansys-tools-variableinterop`` package currently supports Python
3.8 through 3.10 on Windows and Linux.
This package is not currently available on PyPI, but will be when it is
ready for use.
At that time you can install ``pyansys-tools-variableinterop`` with:

.. code::

   pip install pyansys-tools-variableinterop

Alternatively, install the latest from `pyansys-tools-variableinterop GitHub
<https://github.com/pyansys/pyansys-tools-variableinterop>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pyansys-tools-variableinterop.git

For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/pyansys-tools-variableinterop.git
   cd pyansys-tools-variableinterop
   pip install poetry
   poetry install -E dev

This creates a new virtual environment, which can be activated with

.. code::

   poetry shell

Documentation
-------------
TODO: link to the full sphinx documentation.
`pyansys-tools-variableinterop <https://common-variableinterop.docs.pyansys.com/>`_
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

   import ansys.tools.variableinterop as atvi

   width = atvi.RealValue(3.1)
   width
.. code:: out

    3.1

.. code:: python

   # Standard python operations should work seamlessly
   print(4 + width)

   width_metadata = atvi.RealMetadata()
   width_metadata.lower_bound = 0.1
   var(width_metadata)
.. code:: out

   7.1
   {'_description': '', '_custom_metadata': {}, '_units': '', '_display_format': '', '_lower_bound': 0.1, '_upper_bound': None, '_enumerated_values': [], '_enumerated_aliases': []}


Testing
-------
Dependencies required for testing can be installed via:

.. code:: bash

    poetry install -E test

The tests can then be run via pytest.


License
-------
pyansys-tools-variableinterop is licensed under the MIT license.
