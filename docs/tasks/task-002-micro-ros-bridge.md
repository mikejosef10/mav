# TASK-002: micro-ROS Communication Bridge

## 📝 Description
Establish a stable communication layer between the ESP32 (Client) and the ROS 2 host (Agent). This is the foundation for all further control commands.

## 🎯 Acceptance Criteria (Definition of Done)
- [ ] The ESP32 is successfully recognized by the `micro-ros-agent`.
- [ ] Topic `/mav/status/heartbeat` publishes at ~1Hz.
- [ ] The physical LED on the ESP32 can be toggled via `ros2 topic pub /mav/cmd/led`.
- [ ] The code is stored in the Git repository under `firmware/mav-esp-drive/`.

## ⚙️ Technical Specifications
- **Hardware:** ESP32 DevKitC
- **Protocol:** XRCE-DDS over Serial (USB)
- **Baud Rate:** 115,200
- **ROS 2 Version:** Humble / Iron (Dockerized)

## 📌 Interfaces
| Topic | Message Type | Direction |
|:---|:---|:---|
| `/mav/cmd/led` | `std_msgs/msg/Bool` | Subscriber (In) |
| `/mav/status/heartbeat` | `std_msgs/msg/Int32` | Publisher (Out) |

---
This is a reasonable conclusion. We now have a working foundation that you can build upon later. Here is the summary and documentation for your **Task-002: micro-ROS Bridge**.

---

## 📝 Documentation: micro-ROS Bridge (Task-002)
[Official Documentation](https://micro.ros.org/)
[Video Tutorial](https://www.youtube.com/watch?v=Nf7HP9y6Ovo)

### 1. Objective

Set up a bidirectional communication bridge between an ESP32 (microcontroller) and a ROS 2 system (Docker/Host) via a serial USB connection.

### 2. Technical Components

* **Hardware:** ESP32 DevKit V1
* **Framework:** PlatformIO with the `micro_ros_platformio` library.
* **ROS 2 Version:** Humble (in the Docker container).
* **Transport:** Serial (UART) at **115200 Baud**.

### 3. Implemented Functions

* **Heartbeat Publisher:** Sends an incrementing integer every second on `/mav/status/heartbeat`.
* **LED Subscriber:** Receives `std_msgs/Bool` on `/mav/cmd/led` and toggles the internal LED (Pin 2).
* **Auto-Reconnection:** The ESP32 detects the loss of connection to the agent and independently attempts a re-initialization.

---

### 4. Execution (How-To)

#### Step A: Prepare Hardware

1. Connect ESP32 via USB.
2. Identify the port (usually `/dev/ttyUSB0` under Linux/WSL).

#### Step B: Flash ESP32

```bash
# In the project directory
pio run --target upload

```

#### Step C: Start micro-ROS Agent

Use the official Docker image to bridge the gap:

```bash
docker run -it --rm \
  -v /dev:/dev \
  --privileged \
  --net=host \
  microros/micro-ros-agent:humble serial --dev /dev/ttyUSB0 -b 115200

```

#### Step D: Test Communication (In a new terminal)

* **List topics:** `ros2 topic list`
* **Receive data:** `ros2 topic echo /mav/status/heartbeat`
* **Toggle LED:** `ros2 topic pub --once /mav/cmd/led std_msgs/msg/Bool "{data: true}"`

---

### 5. Known Difficulties & Solutions

* **Handshake Delay:** The ESP32 and the agent often take 2-3 attempts to synchronize the XRCE-DDS session. **Solution:** A robust `loop()` that calls `fini` functions and restarts on errors.
* **Memory Management:** micro-ROS on microcontrollers is sensitive to memory allocation. **Solution:** The `rclc_executor` was explicitly limited to 2 handles.
* **WSL2/Docker USB Pass-through:** On Windows, the device must be actively "attached" to the WSL instance via `usbipd` so the Docker container can access it.

---

### 6. Potential Improvements for Later

* **Increase Baud Rate:** Switch to `460800` or `921600` for lower latency.
* **Static IP/WiFi:** Switch to UDP (WLAN) if the USB cable is in the way.
* **Parameter Server:** Implementation of ROS parameters to change e.g., blink frequencies at runtime.