# NoPASARAN

[![Documentation Status](https://readthedocs.org/projects/nopasaran/badge/?version=latest)](https://nopasaran.readthedocs.io/en/latest/?badge=latest)
[![Docker](https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml/badge.svg)](https://github.com/BenIlies/NoPASARAN/actions/workflows/docker-image.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/maintainability)](https://codeclimate.com/github/BenIlies/NoPASARAN/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/68f1d2f9ef6af3f65864/test_coverage)](https://codeclimate.com/github/BenIlies/NoPASARAN/test_coverage)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)


NoPASARAN is an advanced network tool designed to detect, fingerprint, and locate network middleboxes in a unified framework. Written in Python, NoPASARAN uses finite state machines to describe test cases and leverages Ansible for distributing and orchestrating these tests across a network of nodes.

## Features

* Detection, fingerprinting, and location of network middleboxes.
* Utilization of finite state machines for test case description.
* Network orchestration with Ansible.
* Flexible roles for network nodes and proxies.
* Support for JSON-based scenario files for state machine configurations.

## Requirements

* Python 3.8 or later
* Scapy
* Twisted

## Installation

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

## Usage

NoPASARAN can be run in either the Node or Proxy role using the main.py script:

1. To run as a Node:
   ```bash
   python main.py NODE --scenario=<path-to-json-scenario-file>
   ```

2. To run as a Proxy:
   ```bash
   python main.py PROXY
   ```

Replace `<path-to-json-scenario-file>` with the path to your actual JSON scenario file.

## Docker

Alternatively, you can directly download a worker node using Docker:

1. Pull the latest worker node image:
   ```bash
   docker pull benilies/nopasaran:latest

2. Run the worker node container:

   ```bash
   docker run -it benilies/nopasaran:latest

The worker node container is now ready for use.

## Documentation

Visit our [documentation](https://nopasaran.readthedocs.io) for more detailed guides and information about NoPASARAN.

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
