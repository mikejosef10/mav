# 🐳 MAV Docker & Repository Architecture

This document defines the standard for the development and deployment of the **Mini-Auto Vacuum Platform (MAV)**. We use a strict separation between the build environment, simulation, and the runtime on the Raspberry Pi, governed by **Spec-Driven Development (SDD)**.

---

## 🎯 1. Spec-Driven Architecture (SDD)

As defined in the [MAV Engineering Protocol](/.mav-rules.md), the repository is structured to ensure that every component is self-contained with its own specifications and tests.

- **Single Source of Truth:** The `docs/specs/SPEC.md` within each component folder is the authoritative guide for implementation.
- **Traceability:** Requirements are linked from specs to tasks and finally to code/tests.

---

## 💻 2. The Development Workspace (Windows & WSL2)

In the development phase, we use VS Code **DevContainers** in conjunction with **Docker Compose**. 

* **The "Dev-Machine" Service:** Contains the entire toolchain (ROS 2, PlatformIO, ESP-IDF).
* **Simulation (QEMU):** Integrated into the workspace to allow "Spec-Validation" without physical hardware.
* **Support Services:** The `micro-ros-agent` runs as a sidecar to bridge the gap between simulation/hardware and the ROS 2 graph.

---

## 📦 3. Repository Structure & Modularity

The MAV project follows a modular structure where each functional unit (Component) manages its own life cycle.

### Final Folder Structure
```text
mav/ (Main Repo)
├── .mav-rules.md                # MAV Engineering Protocol (AI & Human Mandate)
├── CONTRIBUTING.md              # SDD Workflow instructions
├── STATUS.md                    # High-level project progress
├── docs/                        # Global documentation
│   ├── adr/                     # Global Architecture Decision Records
│   ├── setup/                   # Environment setup guides
│   └── tasks/                   # Project-wide task tracking (Backlog)
├── firmware/
│   └── mav-esp-drive/           # Component: ESP32 Drive Unit
│       ├── docs/
│       │   ├── specs/SPEC.md    # Local technical specification (SSOT)
│       │   └── adr/             # Local architectural decisions
│       ├── src/                 # Implementation
│       ├── test/                # QEMU & Hardware tests
│       └── platformio.ini       # Build configuration
├── ros2_ws/                     # Component: ROS 2 Workspace (High-level logic)
│   └── src/                     # ROS 2 Packages (each with its own docs/specs)
└── tools/                       # Shared tools (QEMU, scripts)
```

---

## 🚀 4. System Orchestration on the Raspberry Pi

The deployment on the Raspberry Pi (RPI) mirrors the modularity of the development environment using Docker Compose.

* **Lifecycle Management:** Compose ensures that all modules (drive, logic, sensors) start in the correct order.
* **Hardware Mapping:** Central definition of access to physical interfaces (e.g., `/dev/ttyUSB0`, I2C).
* **Deployment:** ARM64 images are built on Windows/CI and pulled directly to the RPI.

---

## 🛠️ 5. Hardware Connection (Standard)

Since Docker on Windows runs isolated, we use **usbipd-win** to pass through hardware:
1. **Windows:** `usbipd attach --wsl --busid <ID>`
2. **Container:** The device appears under `/dev/ttyUSB0` and is accessible by the `micro-ros-agent`.
