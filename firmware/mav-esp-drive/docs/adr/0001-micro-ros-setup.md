# ADR 0001: Use of micro-ROS

**Status:** Accepted  
**Date:** 2026-02-12  
**Participants:** Developer

## Context
We need a robust interface between the microcontroller (real-time hardware level) and the single-board computer (high-level logic). Standard serial protocols require manual parsing and are error-prone when expanded.

## Decision
We use **micro-ROS** via a serial USB connection.

## Rationale
- **Native Integration:** The ESP32 appears as a full node in the ROS 2 graph.
- **Type Safety:** Use of standardized ROS 2 messages.
- **Scalability:** Easy integration of further sensors/actuators without protocol changes.

## Consequences
- Increased memory requirements on the ESP32.
- More complex build system (Colcon/micro-ROS Build Tool) compared to the Arduino IDE.