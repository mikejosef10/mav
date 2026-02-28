# Code Explanation: "Mini-Auto" Vacuum Platform (MAV) Project

This document explains the architecture and current code state of the MAV project.

## 1. Introduction & Project Goal

The project goal is to develop a modular, autonomous robotic vacuum cleaner. Instead of a monolithic system, a **distributed architecture** based on modern vehicle software is used. The core philosophy is based on three pillars:
- **Hardware Abstraction:** Clear separation of software and hardware.
- **Native ROS 2 Integration:** Seamless communication from the cloud to the motor register using **micro-ROS**.
- **Modularity:** Each function (e.g., drive) is an encapsulated service.

## 2. System Architecture

The system is divided into three layers:

1.  **Low-Level Layer (Firmware):**
    -   **Hardware:** An ESP32 microcontroller.
    -   **Task:** Direct control of hardware (motors, sensors).
    -   **Interface:** The ESP32 acts as a **micro-ROS client** and thus becomes a native node in the ROS 2 network.

2.  **Middle Layer (Middleware):**
    -   **Hardware:** A single-board computer (e.g., Raspberry Pi).
    -   **Task:** Operating the **micro-ROS agent**, which acts as a bridge between the microcontroller and the rest of the ROS 2 system.

3.  **High-Level Layer (Application):**
    -   **Task:** Execution of complex logic such as path planning (Nav2), mapping (SLAM), and obstacle detection.

Communication between the ESP32 and the Raspberry Pi occurs via a serial USB connection using the XRCE-DDS protocol from micro-ROS. This eliminates the need for manual, error-prone parsing routines.

## 3. Detailed Code Analysis (Status: micro-ROS Implementation)

The code in the `firmware/mav-esp-drive` directory has been fundamentally revised and now contains a working micro-ROS node.

### 3.1. Firmware (`firmware/mav-esp-drive`)

#### `platformio.ini`
The project configuration has been moved to **PlatformIO**:
- **Build System:** Configuration occurs via the `platformio.ini` file.
- **micro-ROS Integration:**
  - The `micro_ros_platformio` library is included via `lib_deps`.
- **Dependencies:**
  - `lib/StatusLed`: Custom library for hardware abstraction of the LED.

#### `lib/StatusLed/StatusLed.hpp`
The `StatusLed` class has been implemented as a C++ encapsulation for controlling the LED.

#### `src/main.cpp`
This is the heart of the firmware. The code initializes a full ROS 2 node on the ESP32 using Arduino and micro-ROS.

**Functionality Overview:**

1.  **ROS 2 Node:**
    -   Initializes a node named `mav_drive_unit`.

2.  **Publisher (Heartbeat):**
    -   **Topic:** `/mav/status/heartbeat`
    -   **Type:** `std_msgs/msg/Int32` (a simple 32-bit integer)
    -   **Logic:** A timer (`rcl_timer_t`) is set to 1000 ms (1 Hz). On every tick, the `timer_callback` function is called, which increments a counter and publishes its value to the topic.
    -   **Purpose:** This serves as a "life signal". Other nodes in the ROS network can subscribe to this topic to check if the microcontroller is still active.

3.  **Subscriber (LED Control):**
    -   **Topic:** `/mav/cmd/led`
    -   **Type:** `std_msgs/msg/Bool` (`true` or `false`)
    -   **Logic:** The node subscribes to this topic. When a message is received, the `subscription_callback` function is triggered. This toggles the `StatusLed` depending on the message content (`true` for on, `false` for off).
    -   **Purpose:** Enables remote control of the LED via the ROS 2 network. For example, a command can be sent from another computer to turn the LED on the robot on or off.

4.  **Executor (`rclc_executor_t`):**
    -   The executor is the central processing loop of micro-ROS on the client.
    -   It monitors all added event sources (here: the 1-Hz timer and the LED subscriber).
    -   In the `loop()` function, `rclc_executor_spin_some()` is called to "process" the executor, checking for new events and executing the corresponding callbacks.

5.  **Connection and Error Logic:**
    -   The `loop()` function contains a state machine managing the connection status.
    -   **Initialization:** It attempts to execute the `init_microros()` function. On success, the `micro_ros_init_successful` flag is set to `true`.
    -   **Error Case:** If initialization fails (e.g., because the micro-ROS agent is not running on the PC), all resources are cleanly released, and the status LED blinks slowly (every 500ms) to signal the error. Initialization is then retried.
    -   **Connection Loss:** If `rclc_executor_spin_some()` reports an error (e.g., because the serial connection to the agent was lost), the `micro_ros_init_successful` flag is set back to `false`. This triggers a re-initialization in the next iteration of the `loop()`.

## 4. Summary and Next Steps

**Current State:**
- The firmware is no longer just a simple prototype, but a **working, robust micro-ROS node**.
- Communication with the ROS 2 network is implemented via a publisher (heartbeat) and a subscriber (LED control).
- Solid error handling ensures the node automatically reconnects after connection losses.

**Next Steps (Implications from the Code):**
1.  **Implement Motor Control:** The next logical step would be adding another subscriber for the topic `/cmd_vel` (type `geometry_msgs/Twist`) to receive speed commands for the motors.
2.  **Publish Sensor Data:** Additional publishers could be added to publish sensor data such as wheel odometry (`nav_msgs/Odometry`) or battery status (`sensor_msgs/BatteryState`).
3.  **Develop ROS 2 Packages:** In the `ros2_ws` directory, counterparts can now be developed, e.g., a teleop node that sends commands to `/mav/cmd/led` or `/cmd_vel`.
