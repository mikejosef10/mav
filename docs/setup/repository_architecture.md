# 🐳 MAV Docker & Repository Architecture

This document defines the standard for the development and deployment of the **Mini-Auto Vacuum Platform (MAV)**. We use a strict separation between the build environment on Windows and the runtime on the Raspberry Pi.

---

## 💻 1. The Development Workspace (Windows & WSL2)

In the development phase, we use VS Code **DevContainers** in conjunction with **Docker Compose**. Instead of packing everything into a single, massive image, we split the tasks:

* **The "Dev-Machine" Service:** Contains the entire toolchain for ROS 2 Humble/Iron and the ESP-IDF SDK. This is where you write your code.
* **Support Services (Sidecars):** In the `docker-compose.yml` of the DevContainer, we define additional services like the `micro-ros-agent` or simulation tools. This allows you to test communication with the ESP32 without having to manually install the agent software on Windows.
* **Benefit:** Your workspace remains modular. If you later need a database for telemetry tests, you simply add it as a service in the Compose file.

---

## 📦 2. Modularity & Git Submodule Strategy

To ensure a clean separation of responsibilities, the MAV project is structured as a **monorepo with submodules**.

* **Concept:** Each module under `software/` is an independent Git repository.
* **Benefit:** Each module (e.g., sensor logic or navigation) has its own history and version tags. You can reuse them in other projects without having to copy the entire MAV system.
* **Workflow:**
* Create a new repo (e.g., `mav_sensor_module`).
* Register it in the main repo: `git submodule add <URL> software/sensor_module`.
* The DevContainer mounts the entire root directory so you can work and commit across modules.



---

## 🚀 3. System Orchestration on the Raspberry Pi

The heart of the robot control is located in the folder `software/docker-compose/mav_rpi/`. This is where the `docker-compose.yml` that brings the robot to life resides.

* **The Role of Compose on the RPI:** While Compose on Windows is responsible for the toolchain, on the RPI it serves as a **lifecycle manager**. It ensures that all modules (drive, logic, sensors) automatically start in the correct order after a restart.
* **Hardware Mapping:** Here, it is centrally defined which container has access to physical interfaces (e.g., `/dev/ttyUSB0` for the ESP32 or I2C for sensors).
* **Deployment Path:**
1. Build ARM64 images via `docker buildx` on Windows.
2. Push them to a registry.
3. On the RPI in the `mav_rpi` folder, simply run `docker compose pull && docker compose up -d`.



---

## 📂 Final Folder Structure

```text
mav-platform/ (Main Repo)
├── .devcontainer/
│   ├── devcontainer.json        # VS Code configuration
│   ├── docker-compose.yml       # Dev infrastructure (Windows host)
│   └── Dockerfile.dev           # Image with ROS2 & ESP-IDF
├── firmware/
│   └── esp32_drive/             # micro-ROS client (C++/ESP-IDF)
├── software/
│   ├── sensor_module/           # [SUBMODULE] Own repo (sensor logic)
│   ├── nav_logic/               # [SUBMODULE] Own repo (nav algorithms)
│   └── docker-compose/          # Central deployment configurations
│       └── mav_rpi/             # Target setup for the Raspberry Pi
│           └── docker-compose.yml
└── shared/                      # Shared ROS2 interfaces (.msg / .srv)

```

---

## 🛠️ Hardware Connection (Standard)

Since Docker on Windows runs isolated, we use **usbipd-win** to pass through the ESP32:

1. **Windows:** `usbipd attach --wsl --busid <ID>`
2. **Container:** The device appears under `/dev/ttyUSB0` and can be addressed directly by the `dev-machine` or the `micro-ros-agent`.



