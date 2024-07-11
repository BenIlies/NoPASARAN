Quickstart
==========

NoPASARAN is an advanced network tool designed to detect, fingerprint, and locate network middleboxes in a unified framework. The tool leverages the power of finite state machines for test case description and enables network orchestration with various roles for machines in the architecture.

Features
--------

- Detection, fingerprinting, and location of network middleboxes.
- Utilization of finite state machines for test case description.
- Flexible roles for machines in the architecture: Worker and Proxy.
- Worker machines perform test campaigns defined by JSON scenario files.
- Proxy machines are accessible to remote Workers, allowing communication when Workers are unreachable from the Internet.
- Support for JSON-based scenario files for state machine configurations.

Requirements
------------

- Python 3.8 or later
- Scapy
- Twisted

Installation
------------

There are two ways to install and use NoPASARAN: by using the source code from GitHub or by installing it as a Python package.

Installing from Source Code:

1. Clone the NoPASARAN repository:

   .. code-block:: bash

      git clone https://github.com/BenIlies/NoPASARAN.git

2. Navigate into the NoPASARAN directory:

   .. code-block:: bash

      cd NoPASARAN

3. Install the necessary Python packages:

   .. code-block:: bash

      pip install -r requirements.txt

Installing as a Python Package:

1. Install NoPASARAN using pip:

   .. code-block:: bash

      pip install nopasaran

Usage
-----

To run NoPASARAN:

.. code-block:: bash

   python main.py --scenario=<path-to-json-scenario-file>

Or using the Python package:

.. code-block:: bash

   nopasaran --scenario=<path-to-json-scenario-file>

Replace <path-to-json-scenario-file> with the path to your actual JSON scenario file.

Additional options:

- ``--verbose`` or ``-v``: Enable verbose output.
- ``--log=<path-to-log-file>`` or ``-l=<path-to-log-file>``: Specify the path to the log file (default is "conf.log").
- ``--log-level=<log-level>`` or ``-ll=<log-level>``: Specify the log level for output. Valid choices are "debug", "info", "warning", and "error".

For any further assistance, use the ``--help`` argument with any command for additional information.

Docker
------

You can also use Docker to download and run a NoPASARAN node:

1. Pull the latest node image:

   .. code-block:: bash

      docker pull benilies/nopasaran:latest

2. Run the node container:

   .. code-block:: bash

      docker run -it benilies/nopasaran:latest

The node container is now ready for use.
