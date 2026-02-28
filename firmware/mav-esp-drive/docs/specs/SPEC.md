# Technical Specifications - MAV ESP Drive

## ROS 2 Interface

### Node Information
- **Node Name:** `mav_drive_unit`

### Topics
| Topic | Type | Direction | Description |
|---|---|---|---|
| `/mav/status/heartbeat` | `std_msgs/Int32` | Publisher | Increments every second (1 Hz). |
| `/mav/cmd/led` | `std_msgs/Bool` | Subscriber | Controls the Status LED (`true` = ON, `false` = OFF). |

## Hardware Mapping
- **MCU:** ESP32 (32-bit Dual Core)
- **Status LED Pin:** GPIO 2 (Active High)
- **Baud Rate:** 115200 (Serial Transport)

## System Behavior

### Startup Sequence
1. Wait 1000ms.
2. Initialize Serial (115200 baud).
3. Set Status LED to `OUTPUT`.
4. Turn LED **ON** for 1000ms, then **OFF**.

### Status LED Codes
| Behavior | Meaning |
|---|---|
| **Constant OFF** | Normal operation (Connected to micro-ROS). |
| **Blinking (100ms ON / 100ms OFF)** | Execution error / Spin failure. |
| **Blinking (500ms ON / 500ms OFF)** | micro-ROS Initialization failure. |

## Software Architecture
- **Framework:** Arduino
- **Libraries:**
    - `micro_ros_platformio` (v2.0+)
    - `rclc` (micro-ROS client library)
- **C++ Standard:** C++20 (GNU++2a)
- **Executor:** Static executor with 2 handles (1 Timer, 1 Subscription).
