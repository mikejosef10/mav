# Documentation - ROS 2 MAV Development Environment (Windows, Docker)
### 1. Architecture Overview

Your system is built in layers. The goal is to keep Windows "clean" and run the entire robotics toolchain in an isolated container.

- **Layer 1 (Hardware):** Your PC + USB connection.
    
- **Layer 2 (Host):** Windows 11/10 with WSL 2 (Ubuntu 22.04).
    
- **Layer 3 (Engine):** Docker Desktop (linked with WSL 2).
    
- **Layer 4 (Development):** VS Code with "Dev Containers".
    
- **Layer 5 (Runtime):** The Docker container with **ROS 2 Humble** and C++20.
    

---

### 2. Installation Checklist (Status Quo)

| **Step**           | **Status** | **Action**                                                                                                   |
| ------------------ | ---------- | ------------------------------------------------------------------------------------------------------------ |
| **WSL 2 & Ubuntu** | ✅ Done     | [WSL Installation Guide](wsl_installation_guide.md).                                                         |
| **Docker Desktop** | ✅ Done     | [Download here](https://www.docker.com/products/docker-desktop/). Select "Use WSL 2" during installation.    |
| **VS Code**        | ✅ Done     | Install and add the **"Dev Containers"** extension.                                                          |
| **USBIPD**         | ✅ Done     | [Download here](https://github.com/dorssel/usbipd-win/releases).                                             |
---

### 3. Project Setup

#### B. Hardware Integration

To ensure the USB port reaches the container, use this workflow on **Windows** (PowerShell):

1. Plug in the device (e.g., the ESP32).
    
2. `usbipd list` (Find the adapter's ID).
    
3. `usbipd bind --busid <ID>` (One-time as Admin).
    
4. `usbipd attach --wsl --busid <ID>` (Connects it to WSL).
    
    

#### C. Graphical User Interfaces (Rviz2 / Gazebo)

Thanks to WSLg, no configuration is needed. When you enter `rviz2` in the container terminal, the window opens directly on your Windows desktop. GPU acceleration is passed from Windows to the container.

---

### 5. Maintenance & Tips

- **Image Updates:** If you change the Dockerfile, press `F1` in VS Code -> `Dev Containers: Rebuild Container`.
    
- **Storage Space:** Docker images consume space. Use `docker system prune` (in PowerShell) to delete old, unused layers.
    
- **Performance:** Ensure your source code is located in the **WSL file system** (e.g., `\\wsl$\Ubuntu\home\user\projects`), not on `C:\`. Access from Docker to Windows drives (`/mnt/c/`) is very slow.



