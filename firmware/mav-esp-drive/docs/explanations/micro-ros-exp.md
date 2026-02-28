# Detailed Explanation: micro-ROS

This document explains what micro-ROS is, how it works, and how it differs from a standard ROS 2 system.

## 1. What is micro-ROS? The Basic Idea

**Goal:** micro-ROS brings the ROS 2 framework to **microcontrollers (MCUs)** – small, resource-constrained processors like an ESP32, STM32, or Arduino.

**The Core Concept:** A microcontroller that, for example, directly controls a motor or reads a sensor, should be a **full participant ("First-Class Citizen")** in the ROS 2 network. Instead of using complicated, custom-developed serial protocols, the microcontroller can directly publish and subscribe to ROS 2 topics.

Imagine being able to simply type `ros2 topic echo /motor_odom` on your PC and seeing the odometry data sent directly from the motor microcontroller's firmware – without any detours. That's exactly what micro-ROS enables.

---

## 2. How Does It Work? The Client-Agent Architecture

micro-ROS cannot run the full ROS 2 software on an MCU because it lacks memory and processing power. Instead, it uses a clever **Client-Agent architecture**.

![Client-Agent Architecture](https://micro.ros.org/img/micro-ROS_architecture.png)
*Source: micro.ros.org*

#### The **micro-ROS Client**
- Runs on the **microcontroller** (e.g., your ESP32 in the `mav` project).
- It is an extremely lightweight C implementation of ROS 2 concepts (Node, Publisher, Subscriber, etc.).
- Its sole task is to talk to the agent. It does **not** communicate directly with other ROS 2 nodes.

#### The **micro-ROS Agent**
- Runs on a "real" computer with an operating system (e.g., a Raspberry Pi or your laptop).
- It acts as a **proxy (representative)** for the client.
- The agent receives data from the microcontroller and forwards it into the normal ROS 2 network (DDS).
- Conversely, the agent receives messages from the ROS 2 network intended for the microcontroller and forwards them to it.

#### The Communication Between Them
- The connection between client and agent is typically a **serial connection** (USB cable, UART), but can also be Wi-Fi (UDP) or Ethernet.
- The protocol used is **DDS-XRCE** (DDS for eXtremely Resource-Constrained Environments). It is a standardized, efficient, and reliable protocol specifically developed for this use case.

---

## 3. Differences and Similarities with ROS 2

| Feature | **Standard ROS 2** | **micro-ROS** | **Note** |
| :--- | :--- | :--- | :--- |
| **Target Hardware** | PCs, laptops, single-board computers (e.g., Raspberry Pi, Jetson Nano) | Microcontrollers (e.g., ESP32, STM32, Teensy, RP2040) | The most fundamental difference. |
| **Operating System** | Required (Linux, Windows, macOS) | Optional (runs on "bare-metal" or with an RTOS like FreeRTOS, Zephyr) | micro-ROS is designed for systems without a full OS. |
| **Resources** | High RAM and CPU requirements | Extremely low memory footprint (few kB RAM) | Optimized for MCUs with e.g., 512 kB RAM. |
| **Middleware** | **DDS (Data Distribution Service)** | **DDS-XRCE (Client side)** | The client speaks only XRCE to the agent. The agent then speaks full DDS. |
| **Network Topology**| Peer-to-Peer (any node can talk directly to any other) | Client-Server (the client talks **only** to the agent) | The MCU is isolated from the rest of the DDS network. |
| **Languages** | C++, Python | C/C++ | No Python on the microcontroller. |
| **Core Concepts** | Nodes, Topics, Services, Parameters | Identical | The fundamental ROS 2 concepts are the same on both sides. |
| **Message Types** | `std_msgs`, `sensor_msgs` etc. | Identical | They use exactly the same `.msg` definitions. |


---

## 4. Summary: Why is micro-ROS so Useful?

1.  **No More Protocol Development:** You no longer need to invent your own error-prone serial protocols to exchange data between PC and MCU (e.g., `"<motor_A:12.3;sensor_B:45>"`). You simply send a standardized ROS 2 message.
2.  **End-to-End Type Safety:** Since both sides use the same message definitions, there are no errors due to incorrect parsing or different data types.
3.  **Seamless Integration:** A sensor or actuator connected via micro-ROS is immediately compatible with all standard ROS 2 tools. You can use `ros2 topic echo`, `rqt_plot`, or `RViz` as if it were a normal ROS 2 node.
4.  **Decoupling:** The firmware on the microcontroller doesn't need to know anything about the rest of the system. Its only task is to publish or subscribe to its specific topics. This promotes modular and reusable code.

---

## 5. Manually Testing the micro-ROS Agent

To manually test the connection and ensure the ESP32 is communicating correctly, the micro-ROS agent can be started via Docker:

```bash
docker run -it --rm \
  --user root \
  --device=/dev/ttyUSB0 \
  microros/micro-ros-agent:humble serial --dev /dev/ttyUSB0
```

This starts the agent in serial mode and connects it to the device at `/dev/ttyUSB0`.
