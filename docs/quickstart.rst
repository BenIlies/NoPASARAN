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

NoPASARAN can be run in either the WORKER or PROXY role:

- To run as a WORKER:

  .. code-block:: bash

     python main.py WORKER --scenario=<path-to-json-scenario-file>

  Or using the Python package:

  .. code-block:: bash

     nopasaran WORKER --scenario=<path-to-json-scenario-file>

- To run as a PROXY:

  .. code-block:: bash

     python main.py PROXY

  Or using the Python package:

  .. code-block:: bash

     nopasaran PROXY

Replace <path-to-json-scenario-file> with the path to your actual JSON scenario file.

Additional options:

- Enable debug logging with `--debug`
- Specify the path to the log file with `--log=<path-to-log-file>`. The default path is "conf.log".
- Specify the log level for output with `--log-level=<log-level>`. Valid choices are "info", "warning", and "error".

For any further assistance, use the `--help` argument with any command for additional information.

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
