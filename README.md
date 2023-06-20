# NoPASARAN

NoPASARAN is an advanced network tool designed to detect, fingerprint, and locate network middleboxes in a unified framework. Written in Python, NoPASARAN uses finite state machines to describe test cases and leverages Ansible for distributing and orchestrating these tests across a network of nodes.

## Features

* Detection, fingerprinting, and location of network middleboxes.
* Utilization of finite state machines for test case description.
* Network orchestration with Ansible.
* Flexible roles for network nodes and proxies.
* Support for JSON-based scenario files for state machine configurations.

## Requirements

* Python 3.8 or later
* Ansible
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