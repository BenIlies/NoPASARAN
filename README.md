# NoPASARAN

[![Docker](https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml/badge.svg)](https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml)
[![Documentation Status](https://readthedocs.org/projects/nopasaran/badge/?version=latest)](https://nopasaran.readthedocs.io/en/latest/?badge=latest)
[![Maintainability](https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/maintainability)](https://codeclimate.com/github/BenIlies/NoPASARAN/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/test_coverage)](https://codeclimate.com/github/BenIlies/NoPASARAN/test_coverage)
[![PyPI version](https://badge.fury.io/py/nopasaran.svg)](https://badge.fury.io/py/nopasaran)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://app.gitter.im/#/room/#nopasaran:gitter.im)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

NoPASARAN is an advanced network tool designed to detect, fingerprint, and locate network middleboxes in a unified framework. Written in Python, NoPASARAN uses finite state machines to describe test cases and leverages Ansible for distributing and orchestrating these tests across a network of nodes.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Installing from Source Code](#installing-from-source-code)
  - [Installing as a Python Package](#installing-as-a-python-package)
- [Usage](#usage)
  - [WORKER Role](#worker-role)
  - [PROXY Role](#proxy-role)
  - [Additional Options](#additional-options)
- [Docker](#docker)
- [Documentation](#documentation)
- [Gitter](#gitter)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Features

- Detection, fingerprinting, and location of network middleboxes.
- Utilization of finite state machines for test case description.
- Network orchestration with Ansible.
- Flexible roles for network nodes and proxies.
- Support for JSON-based scenario files for state machine configurations.

## Requirements

- Python 3.8 or later
- Scapy
- Twisted

## Installation

You can install and use NoPASARAN either by cloning the source code from GitHub or by installing it as a Python package.

### Installing from Source Code

1. Clone the NoPASARAN repository:

    ```bash
    git clone https://github.com/BenIlies/NoPASARAN.git
    ```

2. Navigate into the NoPASARAN directory:

    ```bash
    cd NoPASARAN
    ```

3. Install the necessary Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Installing as a Python Package

- Alternatively, you can install NoPASARAN as a Python package using pip:

    ```bash
    pip install nopasaran
    ```

## Usage

NoPASARAN can be executed in either a WORKER or PROXY role. 

### WORKER Role

In the WORKER role, NoPASARAN performs a test campaign to evaluate network middleboxes. This could be either a client machine that tests its connection path to another endpoint or a trusted machine registered in the network.

To run NoPASARAN in the WORKER role, you need to specify a JSON scenario file that indicates the test campaign the Worker has to run.

- From the source code:

    ```bash
    python main.py WORKER --scenario=<path-to-json-scenario-file>
    ```

- As a package:

    ```bash
    nopasaran WORKER --scenario=<path-to-json-scenario-file>
    ```

### PROXY Role

In the PROXY role, NoPASARAN does not perform any tests. It acts as a server accessible to remote Workers, enabling them to communicate when they are unreachable from the Internet, such as when blocked by a firewall.

To run NoPASARAN in the PROXY role:

- From the source code:

    ```bash
    python main.py PROXY
    ```

- As a package:

    ```bash
    nopasaran PROXY
    ```

### Additional Options

You can further customize the behavior of NoPASARAN with the following options:

- `--verbose` or `-v`: Enable verbose output.
- `--log=<path-to-log-file>` or `-l=<path-to-log-file>`: Specify the path to the log file (default is "conf.log").
- `--log-level=<log-level>` or `-ll=<log-level>`: Specify the log level for output. Valid choices are "debug", "info", "warning", and "error".

Replace `<path-to-json-scenario-file>` with the path to your actual JSON scenario file.

For any further assistance, use the `--help` argument with any command for additional information.

## Docker

You can also use Docker to download and run a NoPASARAN node.

1. Pull the latest node image:

    ```bash
    docker pull benilies/nopasaran:latest
    ```

2. Run the node container:

    ```bash
    docker run -it benilies/nopasaran:latest
    ```

The node container is now ready for use.

## Documentation

For more detailed guides and information about NoPASARAN, please visit our [documentation](https://nopasaran.readthedocs.io).

## Gitter

Join the discussion on [Gitter](https://app.gitter.im/#/room/#nopasaran:gitter.im).

## Acknowledgements

This software is based on the research paper titled "NoPASARAN: a Novel Platform to Analyse Semi Active elements in Routes Across the Network" by Ilies Benhabbour and Marc Dacier, published in 2022.

```bibtex
@article{benhabbour2022nopasaran,
title={NoPASARAN: a Novel Platform to Analyse Semi Active elements in Routes Across the Network},
author={Benhabbour, Ilies and Dacier, Marc},
year={2022},
publisher={Index Copernicus}
}
```

## License

NoPASARAN is released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
