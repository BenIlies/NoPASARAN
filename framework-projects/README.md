# NoPASARAN Framework Projects

This directory provides an overview and entry points to the core repositories that together form the NoPASARAN distributed testing framework. Each project fulfills a distinct role in orchestrating, executing, and managing complex, condition-driven test scenarios across distributed systems.

---

## Framework Architecture Overview

NoPASARAN is composed of four primary node roles:

- **Coordinator** – User-facing control plane and certificate authority
- **Master** – Test orchestration and workload delegation
- **Worker** – Test execution nodes
- **Proxy** – Connectivity enablers for workers behind NATs or firewalls

These components communicate using secure WebSocket-based RPCs, X.509 authentication, and a mesh VPN powered by Netbird.

---

## Projects

### 🧠 Tests-Trees

**Repository:**  
https://github.com/nopasaran-org/nopasaran-tests-trees

A Python framework for defining and executing decision trees used to orchestrate complex test flows. Each node in a tree represents a test whose outcome determines the next execution path.

**Key Features**

- Create decision trees representing conditional test sequences
- Save trees as PNG files with embedded metadata
- Load trees from PNG while preserving structure and data
- Evaluate trees dynamically based on test results

**Role in the Framework**
Used by coordinators and masters to describe and control adaptive test execution logic.

---

### 🧪 Tests

**Repository:**  
https://github.com/nopasaran-org/nopasaran-tests

An open library of reviewed, reusable tests executed by worker nodes within the NoPASARAN framework.

**Structure**

- Each test resides in its own folder
- `MAIN.json` defines the test entry point and flow
- Additional JSON files define test steps and logic

**Documentation**
Each test folder contains a `README.md` describing:

- Test purpose
- Required variables
- Variable structure and semantics

**Role in the Framework**
Provides the executable building blocks used by decision trees and orchestrated by masters.

---

### ⚙️ Endpoint (Master / Worker)

**Repository:**  
https://github.com/nopasaran-org/nopasaran-endpoint

Implements the runtime endpoint that can operate as either a **master** or **worker** in the distributed testing system.

**Key Responsibilities**

- Masters receive decision trees from the coordinator
- Masters dispatch test execution requests to workers
- Workers execute assigned tests and report results
- Mutual authentication via X.509 certificates

**Networking**

- WebSocket-based bidirectional communication
- Netbird mesh VPN for secure connectivity across firewalls

**Role in the Framework**
Execution and orchestration layer of NoPASARAN.

---

### 🌐 Coordinator

**Repository:**  
https://github.com/nopasaran-org/nopasaran-coordinator

The central control plane and user-facing interface of the NoPASARAN framework.

**Responsibilities**

- User interaction via FastAPI
- Certificate authority for masters and workers
- Coordination of test execution
- System monitoring and configuration

**Key Technologies**

- FastAPI (frontend & backend)
- WebSocket RPCs
- Docker Compose for deployment
- Cloudflare Tunnel for DNS and exposure
- Cisco Duo for 2FA
- SMTP for notifications
- Netbird API for VPN orchestration

**Role in the Framework**
Acts as the brain and trust anchor of the entire system.

---

## Node Roles Summary

| Role        | Responsibility                                                        |
| ----------- | --------------------------------------------------------------------- |
| Coordinator | User interface, orchestration, certificate authority                  |
| Master      | Test orchestration and worker management                              |
| Worker      | Execution of individual test cases                                    |
| Proxy       | Enables connectivity between workers behind NATs using ICE (RFC 5245) |

---

## How These Projects Fit Together

1. Users interact with the **Coordinator**
2. Coordinators distribute decision trees to **Masters**
3. Masters orchestrate execution across **Workers**
4. Workers execute tests from the **Tests** repository
5. **Tests-Trees** define conditional execution logic
6. **Proxies** ensure connectivity where direct networking is not possible
