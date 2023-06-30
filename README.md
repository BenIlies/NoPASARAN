# NoPASARAN

[![Docker](https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml/badge.svg)](https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml)
[![Documentation Status](https://readthedocs.org/projects/nopasaran/badge/?version=latest)](https://nopasaran.readthedocs.io/en/latest/?badge=latest)
[![Maintainability](https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/maintainability)](https://codeclimate.com/github/BenIlies/NoPASARAN/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/test_coverage)](https://codeclimate.com/github/BenIlies/NoPASARAN/test_coverage)
[![PyPI version](https://badge.fury.io/py/nopasaran.svg)](https://badge.fury.io/py/nopasaran)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://app.gitter.im/#/room/#nopasaran:gitter.im)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

NoPASARAN is an advanced network tool designed to detect, fingerprint, and locate network middleboxes in a unified framework. Written in Python, NoPASARAN uses finite state machines to describe test cases and leverages Ansible for distributing and orchestrating these tests across a network of nodes.

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

There are two ways to install and use NoPASARAN: by using the source code from GitHub or by installing it as a Python package.

### Installing from Source Code

1. Clone the NoPASARAN repository:

    ```
    git clone https://github.com/BenIlies/NoPASARAN.git
    ```

2. Navigate into the NoPASARAN directory:

    ```
    cd NoPASARAN
    ```

3. Install the necessary Python packages:

    ```
    pip install -r requirements.txt
    ```

### Usage

NoPASARAN can be run in either the Node or Proxy role using the `main.py` script:

- To run as a Node:

    ```
    python main.py NODE --scenario=<path-to-json-scenario-file>
    ```

- To run as a Proxy:

    ```
    python main.py PROXY
    ```

Replace `<path-to-json-scenario-file>` with the path to your actual JSON scenario file.

### Installing as a Python Package

Alternatively, you can install NoPASARAN as a Python package and use the `nopasaran` command.

1. Install NoPASARAN using pip:

    ```
    pip install nopasaran
    ```

2. To run as a Node:

    ```
    nopasaran NODE --scenario=<path-to-json-scenario-file>
    ```

3. To run as a Proxy:

    ```
    nopasaran PROXY
    ```

Replace `<path-to-json-scenario-file>` with the path to your actual JSON scenario file.

### Docker

You can also use Docker to download and run the NoPASARAN worker node.

1. Pull the latest worker node image:

    ```
    docker pull benilies/nopasaran:latest
    ```

2. Run the worker node container:

    ```
    docker run -it benilies/nopasaran:latest
    ```

The worker node container is now ready for use.

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
