Quickstart
==========

NoPASARAN is an advanced network tool designed to detect, fingerprint, and locate network middleboxes in a unified framework. The tool leverages the power of finite state machines for test case description and Ansible for orchestrating tests across a network of nodes.

Features
--------

- Detection, fingerprinting, and location of network middleboxes.
- Utilization of finite state machines for test case description.
- Network orchestration with Ansible.
- Flexible roles for network nodes and proxies.
- Support for JSON-based scenario files for state machine configurations.

Requirements
------------

- Python 3.8 or later
- Scapy
- Twisted

Installation
------------

1. Clone the NoPASARAN repository:

   .. code-block:: bash

      git clone https://github.com/BenIlies/NoPASARAN.git

2. Navigate into the NoPASARAN directory:

   .. code-block:: bash

      cd NoPASARAN

3. Install the necessary Python packages:

   .. code-block:: bash

      pip install -r requirements.txt

Usage
-----

NoPASARAN can be run in either the Node or Proxy role using the main.py script:

- To run as a Node:

  .. code-block:: bash

     python main.py NODE --scenario=<path-to-json-scenario-file>

- To run as a Proxy:

  .. code-block:: bash

     python main.py PROXY

Replace <path-to-json-scenario-file> with the path to your actual JSON scenario file.

Docker
------

Alternatively, you can directly download a worker node using Docker:

1. Pull the latest worker node image:

   .. code-block:: bash

      docker pull benilies/nopasaran:latest

2. Run the worker node container:

   .. code-block:: bash

      docker run -it benilies/nopasaran:latest

The worker node container is now ready for use.