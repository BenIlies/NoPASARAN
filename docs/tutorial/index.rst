Tutorial
========

This section provides a step-by-step guide to using NoPASARAN, including various tests and the setup of an end-to-end control channel.

Tests
-------------------------

Here are some example tests that demonstrate the basic usage of NoPASARAN.

.. toctree::
   :maxdepth: 1

   Introduction to Tests <intro_tests.rst>
   Introduction to Primitives <intro_primitives.rst>
   Introduction to Variables <intro_variables.rst>
   Introduction to Guards <intro_guards.rst>
   Introduction to Nested State Machines <intro_nested_finite_state_machines.rst>
   Introduction to the Establishment of Control Channels <intro_establishment_control_channels.rst>
   Introduction to Sync Messages <intro_sync_messages.rst>

Control Channel
---------------

To establish an end-to-end control channel in NoPASARAN, you can follow the steps outlined in the "TLS Mutual Authenticated End-to-End Tunnel" tutorial:

.. toctree::
   :maxdepth: 1

   TLS Mutual Authenticated End-to-End Tunnel <setup_tls_tunnel>

Node Certificates
-----------------

SSH authentication are used to enhance security through mutual authentication. These certificates are issued by a certification authority for key management.

.. toctree::
   :maxdepth: 1

   SSH Certificates & Node Authentication <ssh_certificates>

Configuring a Worker with a Coordinator
---------------------------------------

Configuring a worker from scratch requires an existing coordinator with a pre-registered worker.

.. toctree::
   :maxdepth: 1

   Worker Deployment <configuring_worker>

Store Developed Tests in Public Library
---------------------------------------

GitHub is used as a mechanism to store public tests and tests-trees. Coordinators can locate and execute the tests stored in these libraries.

.. toctree::
   :maxdepth: 1

   Deploying tests and test trees in the public libraries <tests_deployment>

Temporary Section: Unaddressed Problems
---------------------------------------

This section deals with problems that have not been addressed yet.

Handling Kernel Packets After Receiving Raw Packets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using raw packets in NoPASARAN, the kernel might still send certain packets that are not intended to be part of the tests. To prevent these unwanted packets from affecting the testing environment, we can drop specific types of packets using `iptables`:

1. Drop output ICMP packets for UDP with "host unreachable" message:

.. code-block:: bash

   iptables -A OUTPUT -p icmp --icmp-type destination-unreachable -j DROP

2. Drop output TCP packets with the "RST" (reset) flag set:

.. code-block:: bash

   iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

These rules ensure that the kernel does not send unwanted packets, maintaining the integrity and predictability of the tests involving raw packets.
