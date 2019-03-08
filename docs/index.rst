Python-uds
======================================

Python-uds is a communication protocol agnostic UDS tool.

It was designed to provide a high-level uds interface which can utilise any communication protocol (e.g. LIN, FlexRay, DoIP).
It has a parser tool which can parse an ODX file and produce an easy-to-use interface based on the ODX definition.

.. literalinclude:: ./examples/objectSetup.py
    :language: python
    :linenos:

This is an example of how to interface with an ECU using both the raw object and the methods created
from the Bootloader.odx file.

Currently it supports diagnostics on CAN using a CAN Transport Protocol defined in ISO-15765
and uses the python-can package to utilise the can device interface.

The `final report <https://github.com/richClubb/python-uds/blob/master/docs/final%20report/Python%20UDS%20Manager%20-%20Final%20Report.pdf>`_ is available in the repository.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   configuration
   interface
   services
   examples
   developer

