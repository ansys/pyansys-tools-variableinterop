Getting started
===============

Installation
------------

Two installation modes of the ``pyansys-tools-variableinterop`` package are provided: user and developer.

For users
^^^^^^^^^

Install the latest release for use with this command:

.. code:: bash

    python -m pip install pyansys-tools-variableinterop


For developers
^^^^^^^^^^^^^^

Installing the ``pyansys-tools-variableinterop`` package in developer mode allows
you to modify the source and enhance it.

For procedural information, see :ref:`ref_contribute`.

Style and testing
-----------------

If required, you can call style commands (such as `black`_, `isort`_,
and `flake8`_) or unit testing commands (such as `pytest`_) from the command line.
However, this does not guarantee that your project is being tested in an isolated
environment, which is why you might consider using `tox`_.


Documentation
-------------

For building documentation, you can run the usual rules provided in the
`Sphinx`_ Makefile:

.. code:: bash

    python -m pip install .[doc]
    make -C doc/ html

    # subsequently open the documentation with (under Linux):
    your_browser_name doc/html/index.html

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
