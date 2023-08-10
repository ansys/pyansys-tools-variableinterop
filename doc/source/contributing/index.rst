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
3.8 through 3.11 on Windows, MacOS and Linux.

You can install ``pyansys-tools-variableinterop`` with:

.. code::

   pip install pyansys-tools-variableinterop

Alternatively, install the latest version from `pyansys-tools-variableinterop GitHub
<https://github.com/pyansys/pyansys-tools-variableinterop>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pyansys-tools-variableinterop.git

For a local development version, you can create a new virtual environment: 

.. code:: bash

    python -m venv .venv

It can be activated with:

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


You can then install the developement version of the project:

.. code::

   git clone https://github.com/pyansys/pyansys-tools-variableinterop.git
   cd pyansys-tools-variableinterop
   pip install -e .


Documentation
-------------

Install the required dependencies for the documentation with:

.. code::

    pip install .[doc]


For building documentation, you can run the usual rules provided in the Sphinx Makefile, such as:

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

Use the `PyAnsys Tools Variable Interop Issues <pyansys-tools-variableinterop_issues>`_ page to submit questions,
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
Dependencies required for testing can be installed via:

.. code:: bash

    pip install .[tests]

The tests can then be run via pytest with:

.. code:: bash

    pytest -v


Adhere to code style
--------------------

PyAnsys Tools Variable Interop follows the PEP8 standard as outlined in the `PyAnsys Developer's Guide
<dev_guide_pyansys_>`_ and implements style checking using
`pre-commit <pre-commit_>`_.

To ensure your code meets minimum code styling standards, run this code:

.. code:: console

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this code:

.. code:: console

  pre-commit install


This way, it's not possible for you to push code that fails the style checks

.. code:: text

  $ git commit -am "added my cool feature"
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  Validate GitHub Workflows................................................Passed
