# NoPASARAN Framework Projects

This directory outlines the core repositories of the NoPASARAN distributed testing framework and serves as an entry point to each project.

---

## Projects

### 🧠 Tests-Trees

**Repository:**  
https://github.com/nopasaran-org/nopasaran-tests-trees

A Python framework for defining and executing decision trees used to orchestrate complex test flows. Each node in a tree represents a test whose outcome determines the next execution path.

**Role in the Framework**
Used by masters to describe and control adaptive test execution logic.

---

### 🧪 Tests

**Repository:**  
https://github.com/nopasaran-org/nopasaran-tests

An open library of reviewed, reusable tests executed by worker nodes within the NoPASARAN framework.

**Role in the Framework**
Provides the executable building blocks used by decision trees and orchestrated by masters.

---

### ⚙️ Endpoint (Master / Worker)

**Repository:**  
https://github.com/nopasaran-org/nopasaran-endpoint

Implements the runtime endpoint for the distributed testing system, capable of operating as either a **master** or **worker**. Masters receive decision trees from the coordinator and dispatch test execution requests to workers, while workers execute assigned tests and report results. Communication with a coordinator is bidirectional over WebSockets, secured by a Netbird mesh VPN for firewall traversal, with mutual authentication enforced using X.509 certificates.

**Role in the Framework**
Execution and orchestration layer of NoPASARAN.

---

### 🌐 Coordinator

**Repository:**  
https://github.com/nopasaran-org/nopasaran-coordinator

Serves as the central control plane and user-facing interface of the NoPASARAN framework, providing user interaction via FastAPI, acting as the certificate authority for masters and workers, coordinating test execution, and handling system monitoring and configuration.

**Role in the Framework**
Acts as the brain and trust anchor of the entire system.
