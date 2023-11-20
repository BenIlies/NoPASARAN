Welcome to NoPASARAN's documentation!
=====================================

.. image:: https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml/badge.svg
   :target: https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml
.. image:: https://readthedocs.org/projects/nopasaran/badge/?version=latest
   :target: https://nopasaran.readthedocs.io/en/latest/?badge=latest
.. image:: https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/maintainability
   :target: https://codeclimate.com/github/BenIlies/NoPASARAN/maintainability
.. image:: https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/test_coverage
   :target: https://codeclimate.com/github/BenIlies/NoPASARAN/test_coverage
.. image:: https://badge.fury.io/py/nopasaran.svg
   :target: https://badge.fury.io/py/nopasaran
.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://app.gitter.im/#/room/#nopasaran:gitter.im
.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0.en.html

**NoPASARAN** is an advanced network tool, written in Python, that enables the detection, fingerprinting, and location of network middleboxes. Leveraging the power of finite state machines for test case description and Ansible for distributing and orchestrating these tests across a network of nodes, it is flexible and user-friendly.

NoPASARAN can be configured using JSON-based scenario files and can operate in different roles, including as a Network Worker or Proxy. 

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

.. note::
   
   .. raw:: html

      <div style="background-color: #ffebe9; padding: 10px;">
         <p>
            <strong>Temporary Documentation:</strong> 
            <a href="https://nopasaran-cheatsheet.readthedocs.io">https://nopasaran-cheatsheet.readthedocs.io</a>
            <br>
            Note: This temporary documentation will be integrated soon. NoPASARAN is currently under active development.
         </p>
      </div>

Join the discussion on `Gitter <https://app.gitter.im/#/room/#nopasaran:gitter.im>`_.

Contents
--------

.. toctree::
   :maxdepth: 2

   quickstart
   tutorial/index
   api/index
   contact