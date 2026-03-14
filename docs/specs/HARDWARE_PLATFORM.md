# Technical Specifications - MAV Hardware Platform (REQ-HW-PLAT)

## 🏗 Modular Layer Architecture

To ensure "Component Autonomy" (.mav-rules.md), the physical robot is divided into independent functional layers.

| ID | Layer | Component Focus | Interface |
|---|---|---|---|
| **REQ-HW-L0** | **Base (Drive)** | Motors, Encoders, Battery | PWM / Hall-Pulse |
| **REQ-HW-L1** | **Compute** | ESP32, Raspberry Pi 4 | UART / USB-C |
| **REQ-HW-L2** | **Perception** | LiDAR, IMU | UART / I2C |
| **REQ-HW-L3** | **Payload** | Vacuum Fan, Dust Bin | GPIO / PWM |

---

## 🏎 REQ-HW-L0: Drive Unit Requirements
| ID | Requirement | Value / Detail | Verification |
|---|---|---|---|
| **REQ-DRV-01** | Motor Type | N20 Geared Motor (with Hall Encoder) | Rotation Count via PCNT |
| **REQ-DRV-02** | Motor Voltage | 6V - 9V DC | Power Test |
| **REQ-DRV-03** | Driver IC | TB6612FNG (Dual H-Bridge) | Thermal / PWM Test |
| **REQ-DRV-04** | Chassis Shape | Round / Circular (2WD + Caster) | Navigation clearance |

---

## 🔋 REQ-HW-PWR: Power Distribution
| ID | Requirement | Value / Detail | Verification |
|---|---|---|---|
| **REQ-PWR-01** | Battery Pack | Ansmann 2S1P Li-Ion (7.2V / 3500mAh) | Voltage Check (7.2V - 8.4V) |
| **REQ-PWR-02** | Charger | SkyRC B6neo (Li-Ion 2S Mode / 1.7A) | Full Charge Cycle |
| **REQ-PWR-03** | Connector | XT30U (Gold-plated, 30A rated) | Connectivity Test |
| **REQ-PWR-04** | Logic Power | ESP32 internal LDO via VIN (7.2V to 3.3V) | Serial stability |
| **REQ-PWR-05** | SBC Power | *Planned: 5V/3A Buck Converter for RPi 4* | `vcgencmd get_throttled` |

---

## 📏 Mechanical Dimensions (Modular Expansion)
| ID | Requirement | Value / Detail |
|---|---|---|
| **REQ-MECH-01** | Standoff Type | M3 Hex Brass Standoffs (Male-Female) |
| **REQ-MECH-02** | Deck Material | 3mm Acrylic or 3D Printed PLA |
| **REQ-MECH-03** | Diameter | 120mm - 150mm (Circular) |
