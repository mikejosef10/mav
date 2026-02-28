# MAV ESP Drive Unit

This project contains the firmware for the MAV (Modular Autonomous Vehicle) Drive Unit, based on an ESP32. It uses micro-ROS to communicate with a ROS 2 system.

## Project Status
- **Framework:** Arduino (via PlatformIO)
- **Previous Framework:** ESP-IDF (Deprecated)
- **Connectivity:** micro-ROS via Serial

## Hardware Requirements
- ESP32 DevKit V1 (or compatible)
- Status LED on GPIO 2 (Builtin)

## Setup and Build
This project has been migrated to **PlatformIO**.

1. Install [PlatformIO IDE](https://platformio.org/platformio-ide).
2. Open the `mav-esp-drive` folder.
3. The `platformio.ini` is configured for an `esp32dev` board.
4. Build and upload using the PlatformIO toolbar.

### micro-ROS Configuration
The project uses the `micro_ros_platformio` library. It is configured to use:
- **Transport:** Serial
- **Distro:** Humble

### Helper Scripts
- `helper_scripts/esp_attach.bat`: A Windows script to attach the ESP32 to WSL via `usbipd`.

## Usage
Upon startup, the LED will turn on for 1 second to signal readiness. 
- If micro-ROS connects successfully, the LED turns off.
- If an error occurs, the LED will blink (see specifications for blink codes).

## Troubleshooting and Testing
To manually test the micro-ROS connection, you can start the micro-ROS agent using Docker:

```bash
docker run -it --rm \
  --user root \
  --device=/dev/ttyUSB0 \
  microros/micro-ros-agent:humble serial --dev /dev/ttyUSB0
```
This is useful for verifying that the ESP32 is correctly sending data and that the agent can communicate with it.
