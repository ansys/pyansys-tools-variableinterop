.. _ref_contribute:

Contribute
==========

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyAnsys Tools Variable Interop.

The following contribution information is specific to PyAnsys Tools Variable Interop.

Installation
------------
The ``pyansys-tools-variableinterop`` package currently supports Python
3.9 through 3.12 on Windows, MacOS, and Linux.

You can install the ``pyansys-tools-variableinterop`` package with this command:

.. code::

   pip install pyansys-tools-variableinterop

Alternatively, install the latest version from `pyansys-tools-variableinterop GitHub
<pyansys-tools-variableinterop_repo_>`_ with this command:

.. code::

   pip install git+https://github.com/ansys/pyansys-tools-variableinterop

For a local development version, you can create a new virtual environment with this command:

.. code:: bash

    python -m venv .venv

You can then activate the virtual environment with the command appropriate for your operating system:

.. tab-set::

      .. tab-item:: Linux
        :sync: linux

        ::

          source .venv/bin/activate

      .. tab-item:: macOS
        :sync: macos

        ::

          source .venv/bin/activate

      .. tab-item:: Windows
        :sync: windows

        ::

          .\.venv\Scripts\activate


Next, install the development version of the project with these commands:

.. code::

   git clone https://github.com/ansys/pyansys-tools-variableinterop
   cd pyansys-tools-variableinterop
   pip install -e .


Documentation
-------------

Install the required dependencies for the documentation with this command:

.. code::

    pip install .[doc]


For building documentation, you run the usual rules provided in the Sphinx Makefile for your operating system:

.. tab-set::

    .. tab-item:: Linux
      :sync: linux

      ::

        make -C doc/ html && your_browser_name doc/build/html/index.html

    .. tab-item:: macOS
      :sync: macos

      ::

        make -C doc/ html && your_browser_name doc/build/html/index.html

    .. tab-item:: Windows
      :sync: windows

      ::

        .\doc\make.bat html
        .\doc\build\html\index.html


Post issues
-----------

Use the `PyAnsys Tools Variable Interop Issues <pyansys-tools-variableinterop_issues_>`_ page to submit questions,
report bugs, and request new features. When possible, use these issue
templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the PyAnsys support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.


Build documentation
-------------------

To build the PyAnsys Tools Variable Interop documentation locally, in the root directory of the repository,
run these commands::

    pip install .[doc]
    .\doc\make.bat html

Testing
-------
You can install the dependencies required for testing with this command:

.. code:: bash

    pip install .[tests]

You can then run the tests via ``pytest`` with this command:

.. code:: bash

    pytest -v


Adhere to code style
--------------------

PyAnsys Tools Variable Interop follows the PEP8 standard as indicated in the `PyAnsys Developer's Guide
<dev_guide_pyansys_pep8_>`_ and implements style checking using
`pre-commit <pre-commit_>`_.

To ensure your code meets minimum code styling standards, run these commands:

.. code:: console

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command:

.. code:: console

  pre-commit install


This way, it's not possible for you to push code that fails the style checks:

.. code:: text

  $ git commit -am "added my cool feature"
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  check yaml...............................................................Passed
  trim trailing whitespace.................................................Passed
  Validate GitHub Workflows................................................Passed
