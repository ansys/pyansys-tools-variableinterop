User guide
==========

You can create values and metadata like any other Python object:

.. code:: python

   import ansys.tools.variableinterop as atvi

   width = atvi.RealValue(3.1)
   width


.. rst-class:: sphx-glr-script-out

 .. code-block:: none

      3.1


.. code:: python

   # Standard Python operations should work seamlessly
   4 + width


.. rst-class:: sphx-glr-script-out

 .. code-block:: none

      7.1

.. code:: python

   width_metadata = atvi.RealMetadata()
   width_metadata.lower_bound = 0.1
   vars(width_metadata)


.. rst-class:: sphx-glr-script-out

 .. code-block:: none

      {'_description': '', '_custom_metadata': {}, '_units': '', '_display_format': '', '_lower_bound': 0.1, '_upper_bound': None, '_enumerated_values': [], '_enumerated_aliases': []}
