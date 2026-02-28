# Task 001: Blinking LED & Toolchain Validation

## 📝 Overview

This ticket marks the "Hello World" milestone for the **MAV Drive Unit**. The goal was not only to make an LED light up but also to validate the entire development environment (Windows -> WSL -> ESP32) as well as the modular C++ structure.

**Status:** ✅ Completed

**Component:** `firmware/mav-esp-drive`

**Hardware:** ESP32 DevKitC

---

## 🎯 Learning Objectives & Requirements

* **Toolchain Check:** Does the USB pass-through from Windows to WSL via `usbipd` work?
* **Build System:** Does ESP-IDF/PlatformIO compile correctly within the Docker/WSL environment?
* **Hardware Abstraction:** Application of the "Clean Code" principle by encapsulating the LED logic in a class (instead of naked `digitalWrite` calls).

---

## 🛠 Implementation Details

### 1. Hardware Connection (Windows Host)

Since development takes place in the WSL environment, the ESP32's serial interface must be "passed through" from the Windows host to WSL. A helper script was created for this:

**File:** `firmware/mav-esp-drive/helper_scripts/esp_attach.bat`

> This script automates identifying the `VID:PID` and binding the device to the WSL instance.

### 2. Software Architecture (Firmware)

In accordance with the project philosophy, the LED logic was outsourced to its own library.

#### The `StatusLed` Class

Instead of defining pins globally, `StatusLed` encapsulates the hardware details. This allows for future expansion of the LED logic (e.g., for blinking patterns or PWM dimming) without modifying the `main.cpp` code.

```cpp
// StatusLed.hpp
class StatusLed {
public:
    explicit StatusLed(int pin) : _pin(pin) {}
    void begin() { 
        pinMode(_pin, OUTPUT); 
    }
    void on() { digitalWrite(_pin, HIGH); }
    void off() { digitalWrite(_pin, LOW); }
private:
    int _pin;
};

```

#### Main Logic

`main.cpp` uses the class and provides telemetry data via the Serial Monitor (115200 baud) to monitor the status of the Drive Unit.

---

## 💡 Rationale & Decisions (ADR-Light)

* **Why a class for a simple LED?** In the spirit of the project ("Software runs isolated from hardware"), we prevent hardware-specific Arduino commands from being distributed throughout the code. `main.cpp` only knows that there is an object that can `on()` or `off()`.
* **Why `usbipd`?** It enables seamless integration into the Linux-based ROS 2 toolchain while the familiar Windows interface can be used for development.
* **Code Comment (LED OFF):** In the current state, the "off" part is commented out to force a permanent light for the first validation of the power supply and pin mapping.

---

## 🏁 Verification

1. **Build:** `pio run` via terminal successful.
2. **Upload:** `esp_attach.bat` executed -> `pio run -t upload` successful.
3. **Function:** The onboard LED (Pin 2) is permanently lit.
4. **Telemetry:** Serial Monitor correctly shows "MAV Drive Unit started...".

---

## ⏭ Next Steps

After the hardware foundation is in place, we will bridge the gap to ROS 2 in **Task 002**:

* Setup of the micro-ROS agent.
* Creation of a publisher that sends the LED status as `std_msgs/Bool` to the ROS graph.