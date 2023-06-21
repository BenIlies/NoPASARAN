Welcome to NoPASARAN's documentation!
======================================

**NoPASARAN** is an advanced network tool, written in Python, that enables the detection, fingerprinting, and location of network middleboxes. Leveraging the power of finite state machines for test case description and Ansible for distributing and orchestrating these tests across a network of nodes, it is flexible and user-friendly.

NoPASARAN can be configured using JSON-based scenario files and can operate in different roles, including as a Network Node or Proxy. 

For a detailed understanding of NoPASARAN, refer to the paper "NoPASARAN: a Novel Platform to Analyse Semi Active elements in Routes Across the Network". The paper can be accessed directly via the following link:

`NoPASARAN paper <https://acigjournal.com/api/files/download/2053571.pdf>`_

You may cite this work as follows:

.. code-block:: bibtex

   @article{benhabbour2022nopasaran,
     title={NoPASARAN: a Novel Platform to Analyse Semi Active elements in Routes Across the Network},
     author={Benhabbour, Ilies and Dacier, Marc},
     year={2022},
     publisher={Index Copernicus}
   }

For more information, check out the :doc:`usage` section, which includes how to :ref:`installation` the project.

.. note::

   This project is under active development.

Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   quickstart
   contact
   tutorial/*