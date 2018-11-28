Python-uds
======================================

Python-uds is a communication protocol agnostic UDS tool.

It was designed to provide a high-level uds interface which can utilise any communication protocol( e.g. LIN, FlexRay, DoIP)
It has a parser tool which can parse an ODX file and produce an easy-to-use interface based on the ODX definition.

.. literalinclude:: ./examples/objectSetup.py
    :language: python
    :linenos:


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   configuration
   interface
