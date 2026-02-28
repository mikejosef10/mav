## 🔌 Power Supply & Prototyping

These components form the physical backbone for your first Hardware-in-the-Loop (HIL) tests.

| Component | Specification / Capacity | Use in MAV Project |
| --- | --- | --- |
| **Power Supply Module** | Input: 6.5-12V (DC) / Output: 3.3V or 5V (switchable) | Supplying the breadboard rail for MCU and sensors. |
| **830-Point Breadboard** | 830 contacts, standard 2.54mm pitch | Fast assembly of test circuits without soldering. |
| **Jumper Wire Set** | Mix of M/M, F/M and rigid wires | Signal connection between ESP32/STM32 and sensors. |

---

## 🚦 Human-Machine Interface (HMI) & Indicators

For an autonomous robot, visual and acoustic feedback (e.g., ROS status diagnostics) is essential.

* **LEDs (Colored & RGB):** * **Spec:** Standard 5mm, approx. 2V forward voltage (note color), 20mA max.
* **Project Benefit:** Visualization of ROS 2 states (e.g., Green = `Active`, Blue = `Wait for Agent`, Red = `Emergency Stop`). The **RGB LED** is perfect for error codes via PWM.


* **Buzzer (Active/Passive):**
* **Active:** Generates sound at constant voltage (Logic-High).
* **Passive:** Requires PWM signal for sound generation (perfect for testing your PWM driver class).


* **Buttons (Pushbuttons):**
* **Spec:** 12x12mm tactile switches.
* **Project Benefit:** Manual reset or "Start Mission" trigger.



---

## 🧠 Signal Processing & Logic ICs

These components help you write the Hardware Abstraction Layer (HAL) for complex functions.

* **74HC595 (8-Bit Shift Register):**
* **Spec:** Serial-In, Parallel-Out. Allows control of 8 outputs via only 3 pins.
* **Project Benefit:** Expansion of GPIOs for status displays if pins on the ESP32 become scarce.


* **4N35 Optocoupler:**
* **Spec:** Galvanic isolation using light.
* **Project Benefit:** Critical for **emergency stop logic**. It separates the sensitive MCU circuit from the (later) load circuit of the vacuum motors.


* **PN2222 (NPN Transistors):**
* **Spec:** Ic max 600mA.
* **Project Benefit:** Switching small loads (like the active buzzer) that exceed the GPIO current of the MCU.



---

## 🌡 Sensors (Analog Inputs)

Ideal for testing your ADC drivers (Analog-to-Digital Converter) in micro-ROS.

* **Photoresistor (LDR):** Measures light intensity. Can be used for simple "under-furniture detection".
* **Thermistor (NTC):** Temperature-dependent resistor. Ideal for monitoring **battery health** or MCU temperature (published in `/battery_state`).
* **Precision Potentiometer:** For simulating sensor values (e.g., distance emulation) before you have a real Lidar/ultrasonic sensor.

---

## 🛠 Missing Components for the "Drive-Unit"

Since your goal is a "vacuum robot," I noticed something as a "peer": The kit is fantastic for logic, but for **Phase 1 (Drive-Unit)** of your roadmap, two crucial things are still missing:

1. **H-Bridge (Motor Driver):** e.g., an L298N or DRV8833, to drive the actual motors.
2. **Motors & Encoders:** To generate real feedback for `/odom` (odometry).

> **Pro-Tip for your C++20 project:** Use the resistors from the kit to build **pull-up/pull-down** circuits in hardware rather than relying solely on internal MCU pull-ups – this massively increases signal stability for your ROS 2 communication.