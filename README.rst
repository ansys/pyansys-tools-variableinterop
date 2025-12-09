PyAnsys Tools Variable Interop
==============================
|pyansys| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |pypi| image:: https://img.shields.io/pypi/v/pyansys-tools-variableinterop.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/pyansys-tools-variableinterop/

.. |codecov| image:: https://codecov.io/gh/ansys/pyansys-tools-variableinterop/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/pyansys-tools-variableinterop

.. |GH-CI| image:: https://github.com/ansys/pyansys-tools-variableinterop/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pyansys-tools-variableinterop/actions/workflows/ci_cd.yml

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
  :target: https://github.com/psf/black
  :alt: black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pyansys-tools-variableinterop/main.svg
   :target: https://results.pre-commit.ci/latest/github/ansys/pyansys-tools-variableinterop/main
   :alt: pre-commit.ci status

Overview
--------

PyAnsys Tools Variable Interop contains definitions of the basic variables, types,
metadata, and values intended to provide interoperability between all products that
optionally choose to participate.

Characteristics
---------------

PyAnsys Tools Variable Interop has these key characteristics:

- Supports a minimal but complete set of formally defined data types for engineering work.
- Offers a standard base implementation in each supported language that matches the style and intent of
  the given language.
- Implements the same standard data types and conversion rules as all ModelCenter products.
- Provides the following capabilities:

  - To/from an "API" string (not intended for UI layer) to allow data transfer in human-readable format
    across products and regions
  - To/from human-readable display strings
  - To/from binary blocks that are platform agnostic
  - Implicit conversion to/from language primitives for lossless conversions
  - Explicit conversion for lossy conversions

- Uses the `visitor pattern <https://en.wikipedia.org/wiki/Visitor_pattern>`_ to make it easy and
  reliable to add and reuse new operations with compile-time semantics. A data type library can
  either make it easy to add new data types or make it easy to add new operations to the existing
  data types. It is extremely hard to make both possible at the same time. Because this library
  makes it easy to add new operations to the existing data types, adding new data types is not easy.
- Defines strongly the most commonly reused metadata.
- Provides a generic dictionary for custom metadata.

Top-level items
---------------

Descriptions follow of the top-level items in PyAnsys Tools Variable Interop:

- The base metadata type that all variable types extend is
  ``CommonVariableMetadata``. Metadata is defined as the information
  about a variable that is static and does not change when a
  component or workflow is run.
- The value interface is ``IVariableValue``. These values are defined so that
  PyAnsys Tools Variable Interop knows how to properly convert from one type to
  the other via language operators. Lossless conversions are implicit. Operations
  that are lossy, such as converting a real value to an integer, are explicit.
  Explicit conversions can throw an exception if there is an overflow or other
  "bad data" situation.


Project background
------------------

After 20 years of work on integration problems, a holistic review was performed around the
concept of a variable in some legacy codebases. No less than two dozen classes that represent a
variable were found. There were many more switch statements, where one data type needed to be
converted to another. This inconsistency brings about the following problems:

- The behavior of one capability within the product suite does not match that of other
  capabilities, leading to confusion, bugs, and lost time.
- Switch statements are notorious for introducing bugs. People tend to cut and paste them, leading
  to subtle maintenance issues as one is modified and the other diverges. There is no compile-time
  type checking.
- Slight differences in data types (int32 versus int64) can lead to unexpected bugs, including disastrous
  "bad data with no error" class issues.
- Seemingly simple tasks like reliably converting to a string or byte buffer and back are
  surprisingly hard to do correctly in all edge cases. Worse, even if you get a "correct"
  implementation, if it doesn't match what is used at an API boundary by a different capability
  or product, errors ensue.


The standards and the standard implementations in several languages came out of this review.

Documentation and issues
------------------------

Documentation for the latest stable release of this package is hosted at
`PyAnsys Tools Variable Interop documentation <https://variableinterop.docs.pyansys.com/index.html>`_.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the development
version or previously released versions.

On the `PyAnsys Tools Variable Interop Issues <https://github.com/ansys/pyansys-tools-variableinterop/issues>`_ page,
you can create issues to report bugs and request new features. On the
`PyAnsys Tools Variable Interop Discussions <https://github.com/ansys/pyansys-tools-variableinterop/discussions>`_
page or the `Discussions page <https://discuss.ansys.com/>`_ on the Ansys Developer portal, you
can post questions, share ideas, and get community feedback.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

Installation
------------

The ``pyansys-tools-variableinterop`` package currently supports Python
3.10 through 3.13 on Windows, MacOS, and Linux.

You can install this package with this command:

.. code::

   pip install pyansys-tools-variableinterop

Alternatively, install the latest version from the `pyansys-tools-variableinterop
<https://github.com/ansys/pyansys-tools-variableinterop/>`_ GitHub repository
with this command:

.. code::

   pip install git+https://github.com/ansys/pyansys-tools-variableinterop

To install a local development version of the project, run these commands:

.. code::

   git clone https://github.com/ansys/pyansys-tools-variableinterop
   cd pyansys-tools-variableinterop
   pip install -e .


Documentation building
----------------------

Install the required dependencies for building the documentation with this
command:

.. code:: bash

    pip install .[doc]

Build and view documentation with the one or more commands for your
operating system:

.. code:: bash

    # For Linux and MacOS
    make -C doc/ html && your_browser_name doc/build/html/index.html

    # For Windows
    .\doc\make.bat html
    .\doc\build\html\index.html

Testing
-------

Install the dependencies required for testing with this command:

.. code:: bash

    pip install .[tests]

Run the tests via `pytest <pytest_>`_ with this command:

.. code:: bash

    pytest -v

Usage
-----

You can create values and metadata like any other Python object:

.. code:: python

   import ansys.tools.variableinterop as atvi

   width = atvi.RealValue(3.1)
   width

.. code:: python

   width_metadata = atvi.RealMetadata()
   width_metadata.lower_bound = 0.1
   var(width_metadata)

License
-------

PyAnsys Tools Variable Interop is licensed under the MIT license.

.. LINKS AND REFERENCES
.. _pytest: https://docs.pytest.org/en/stable/
