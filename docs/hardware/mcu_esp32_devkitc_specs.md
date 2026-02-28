Link: [ESP32S Dev Kit](https://www.az-delivery.de/en/products/esp32-nodemcu-module-wlan-wifi-dev-kit-c-development-board-mit-cp2102-und-usb-c-anschluss-esp-32-esp32-wroom-32-kompatibel-mit-arduino?_pos=1&_psq=ESP32+NodeMCU+Module+WLAN+WiFi+Dev+Kit+C+Development+Board+mit+CP2102+und+USB-C+Anschluss&_ss=e&_v=1.0&variant=46038922297611)

Free Ebook: [Ebook](https://www.az-delivery.de/en/products/esp32s-dev-kit-c-v4-nodemcu-wlan-development-board-kompatibel-mit-arduino-nachfolger-modul-von-esp32s-dev-kit-c-v2-1?_pos=1&_psq=ESP32+DEV+Kit+C+V2+ebook&_ss=e&_v=1.0)
## 🧠 Computing Unit & Memory (The "Brain")

For a real-time system like the MAV, computing power is crucial for calculating odometry data while simultaneously serving the ROS stack.

| Feature | Specification | Relevance for MAV |
| --- | --- | --- |
| **Processor** | Xtensa® Dual-Core 32-bit LX6 | Enables multithreading (e.g., Core 0 for micro-ROS, Core 1 for motor control). |
| **Clock Frequency** | Up to 240 MHz | High performance for modern C++20 features (Ranges, Lambdas). |
| **SRAM** | 520 KB | Sufficient buffer for XRCE-DDS (micro-ROS) middleware. |
| **Flash** | 4 MB | Enough space for extensive firmware and log data. |

---

## 🌐 Connectivity & Communication

Since your project relies on a distributed architecture, the ESP32 offers maximum flexibility here.

* **USB Interface:** USB-C (CP2102 Bridge). This is your primary connection to the Raspberry Pi (micro-ROS agent).
* **WLAN (802.11 b/g/n):** Enables OTA (Over-the-Air) updates or telemetry streaming without cables.
* **Bluetooth (v4.2 BR/EDR & BLE):** Optional for a smartphone remote control or setup app.
* **Bus Systems:**
* **2x I2C:** For sensors (IMU, ToF sensors).
* **3x SPI:** For SD card logging or high-speed sensors.
* **3x UART:** One occupied by USB, two free for peripherals (e.g., Lidar).

---

## ⚙️ I/O & Sensor Interfaces (Hardware Abstraction)

In your hardware abstraction layer, you will address these pins directly:

* **PWM (MCPWM & LEDC):** The ESP32 has special motor PWM units (MCPWM), which are perfect for controlling H-bridges (motors).
* **ADC (12-bit):** 18 channels for monitoring battery voltage (via voltage divider from your kit).
* **Hardware Encoder:** The ESP32 has integrated pulse counters (PCNT) that count encoder signals from motors in hardware without burdening the CPU – essential for precise odometry.
* **GPIOs:** 3.3V logic level (Caution: Not 5V tolerant!).

---

## 🛠 Integration into the MAV Architecture

In your ADR (Architecture Decision Record), you can classify this ESP32 as follows:

1. **Role:** "Low-Level Controller" (Real-Time Actor/Sensor Hub).
2. **Middleware:** Runs the **micro-ROS Client**. Uses the XRCE-DDS protocol over the USB-C serial interface.
3. **Advantage over Arduino Uno:** The ESP32 can use real **FreeRTOS tasks**. This allows you to run motor control (PID) in a high-priority task while ROS data exchange takes place in another task without disturbing the timing.

---

**Tip from the "Peer":** Since you have the AZDelivery board, note that it is often very wide on the breadboard (only one row of holes remains free on one side). It's best to use two breadboards side-by-side or jumper cables from below to have room for your sensors.