# Technical Specifications - MAV ESP Drive

## ROS 2 Interface

### Node Information
- **Node Name:** `mav_drive_unit`

### Topics
| ID | Topic | Type | Direction | Description | Verification |
|---|---|---|---|---|---|
| **REQ-COM-01** | `/mav/status/heartbeat` | `std_msgs/Int32` | Publisher | Increments every second (1 Hz). | `test_qemu.py` / `[uROS] Transport initialized` |
| **REQ-COM-02** | `/mav/cmd/led` | `std_msgs/Bool` | Subscriber | Controls the Status LED (`true` = ON, `false` = OFF). | `test_qemu.py` / `[uROS] Transport initialized` |

## Hardware Mapping
| ID | Component | Pin / Value | Description | Verification |
|---|---|---|---|---|
| **REQ-HW-01** | MCU | ESP32 | 32-bit Dual Core | PlatformIO Env |
| **REQ-HW-02** | Status LED | GPIO 2 | Active High | `[LED] Initialized` |
| **REQ-HW-03** | Baud Rate | 115200 | Serial Transport | `platformio.ini` |

## System Behavior

### Startup Sequence
| ID | Step | Detail | Verification |
|---|---|---|---|
| **REQ-SYS-01** | Boot Delay | Wait 1000ms. | `[SYS] MAV Drive Unit starting...` |
| **REQ-SYS-02** | Serial Init | Initialize Serial (115200 baud). | `[SYS] MAV Drive Unit starting...` |
| **REQ-SYS-03** | LED Init | Set Status LED to `OUTPUT`. | `[LED] Initialized` |
| **REQ-SYS-04** | LED Blink | Turn LED **ON** for 1000ms, then **OFF**. | `[LED] Test pattern completed` |

### Status LED Codes
| ID | Behavior | Meaning | Verification |
|---|---|---|---|
| **REQ-SYS-05** | **Constant OFF** | Normal operation (Connected to micro-ROS). | Manual |
| **REQ-SYS-06** | **Blinking (100ms)** | Execution error / Spin failure. | Manual |
| **REQ-SYS-07** | **Blinking (500ms)** | micro-ROS Initialization failure. | Manual |

## Software Architecture
- **Framework:** Arduino
- **Libraries:**
    - `micro_ros_platformio` (v2.0+)
    - `rclc` (micro-ROS client library)
- **C++ Standard:** C++20 (GNU++2a)
- **Executor:** Static executor with 2 handles (1 Timer, 1 Subscription).
