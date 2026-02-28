# Project: "Mini-Auto" Vacuum Platform (MAV)

## 📝 Project Overview

The goal of this project is to develop a modular, autonomous robotic vacuum cleaner, developed according to the software standards of modern autonomous vehicles (AV). Instead of a monolithic system, a **distributed architecture** is used, providing scalability for future expansions (Lidar, SLAM, Compute-Offloading).

### Core Philosophy

- **Hardware Abstraction:** Software runs isolated from the hardware through defined interfaces.
    
- **Native ROS 2 Integration:** Seamless communication from high-level algorithms down to motor registers using **micro-ROS**.
    
- **Modularity:** Each component (drive, sensors, logic) is an independent service.
    

---

## 🛠 Technology Stack & Standards

|**Area**|**Technology / Standard**|**Reasoning**|
|---|---|---|
|**Languages**|C++20 / C|Performance and modern language features (Smart Pointers, Ranges).|
|**Middleware**|**ROS 2 (Humble/Iron)**|Industry standard for robotics; uses DDS for reliable communication.|
|**Communication**|**micro-ROS (USB/Serial)**|Native ROS 2 nodes on MCUs; uses XRCE-DDS for resource-efficient Pub/Sub communication.|
|**Containerization**|**Docker & DevContainers**|Reproducible build environments; separation of host and target systems.|
|**Build System**|CMake / Colcon|Standard for C++ and ROS 2 projects.|
|**Quality Assurance**|GTest / GMock / Linter|Ensuring code quality through unit tests and static analysis.|

---

## 🏗 System Architecture

The architecture follows the pattern of a modern vehicle E/E system, but uses a direct serial connection:

1. **Low-Level Layer (Firmware):**
    
    - **Base:** ESP32.
        
    - **Task:** Motor control (PWM), encoder reading, emergency stop logic.
        
    - **Interface:** **micro-ROS Client** (publishes native ROS 2 topics like `/odom`).
        
2. **Middle Layer (Middleware):**
    
    - **Base:** Raspberry Pi or Jetson Nano (Dockerized ROS 2).
        
    - **Task:** Operating the **micro-ROS Agent**, which establishes the connection between the MCU and the rest of the ROS graph.
        
3. **High-Level Layer (Application):**
    
    - **Task:** Mapping, path planning (Nav2), obstacle detection.
        

> You can find the corresponding folder structure in the [Folder Structure](docs/setup/setup_windows.md#3-project-setup) of the setup guide.
---

## 🔄 Development Process

To maintain professionalism, we use a **Git-based workflow**:

### 1. Documentation (Markdown-First)

- **ADRs (Architecture Decision Records):** Every major decision (e.g., switching from CAN to USB/micro-ROS) is justified in a `.md` file in the `/docs/adr` folder.
    
- **API Docs:** Inline documentation via Doxygen.
    

### 2. Modular Build Process

Each module is its own ROS package or an independent C++ library.

- **Development in Container:** The entire toolchain (micro-ROS build system, compiler) resides in the Docker image.
    
- **CI/CD (Planned):** Automated builds and tests on every push via GitHub Actions.
    

### 3. micro-ROS Integration

Instead of manual byte protocols, we use the **XRCE-DDS** protocol:

- The microcontroller is treated as a full participant in the ROS network.
    
- Communication occurs via standard messages (`geometry_msgs/Twist`, `nav_msgs/Odometry`).
    
- No manual parsing of serial data streams necessary; micro-ROS handles serialization.
    

---

## 🚀 Roadmap: Phase 1 (The "Basics")
> See the [Project Status](STATUS.md) for the current state.

Focus on hardware-near C++ development and connectivity.

- [x] **Setup Dev-Environment:** Docker container with ROS 2 (and micro-ROS components).
    
- [ ] **Firmware "Drive-Unit":** micro-ROS node on the MCU for controlling the motors.
    
- [ ] **Topic Definition:** Implementation of subscribers for `/cmd_vel` and publishers for `/battery_state`.
    
- [ ] **ROS 2 Integration:** Validation of communication between Pi and MCU via the micro-ROS agent.