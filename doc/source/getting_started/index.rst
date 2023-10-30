Getting started
===============

Installation
------------

Two installation modes of the ``pyansys-tools-variableinterop`` package are provided: user and developer.

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing the ``pyansys-tools-variableinterop`` package, make sure that you
have the latest version of `pip`_ with this command::

.. code:: bash

    python -m pip install -U pip

Then, install the latest ``pyansys-tools-variableinterop`` package with this command:

.. code:: bash

    python -m pip install pyansys-tools-variableinterop

Install in developer mode
^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the ``pyansys-tools-variableinterop`` package in developer mode allows
you to modify the source and enhance it.

Before contributing to the project, ensure that you are thoroughly familiar with the
`PyAnsys Developer's Guide`_.

To install the ``pyansys-tools-variableinterop`` package in developer mode, perform
these steps:

#. Clone the PyAnsys Tools Variable Interop repository with this command:

   .. code::

      git clone https://github.com/ansys/pyansys-tools-variableinterop

#. Create a clean Python environment and activate it with these commands:

   .. code::

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Make sure you have the latest required documentation and testing tools with
   these commands:

   .. code::

      pip install .[doc]
      pip install .[tests]

#. Install the project in editable mode with this command:

   .. code::

      python -m pip install --editable pyansys-tools-variableinterop


Style and testing
-----------------

If required, you can call style commands (such as `black`_, `isort`_,
and `flake8`_) or unit testing commands (such as `pytest`_) from the command line.
However, this does not guarantee that your project is being tested in an isolated
environment, which is why you might consider using `tox`_.


Distributing
------------

If you would like to create either source or wheel files, start by running this
command to install the building requirements:

.. code:: bash

    python -m pip install -e .[doc,tests]

Then, run these commands:

    .. code:: bash

        python -m build
        python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's Guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _tox: https://tox.wiki/
