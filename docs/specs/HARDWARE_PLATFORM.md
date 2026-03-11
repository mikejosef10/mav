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
| **REQ-PWR-01** | Battery Cell | 2x 18650 Li-Ion (3.7V nominal) | Multimeter |
| **REQ-PWR-02** | SBC Power | UPS HAT for Raspberry Pi (5V / 3A) | `vcgencmd get_throttled` |
| **REQ-PWR-03** | MCU Power | LM2596 Buck Converter (to 5V) | Logic stability |

---

## 📏 Mechanical Dimensions (Modular Expansion)
| ID | Requirement | Value / Detail |
|---|---|---|
| **REQ-MECH-01** | Standoff Type | M3 Hex Brass Standoffs (Male-Female) |
| **REQ-MECH-02** | Deck Material | 3mm Acrylic or 3D Printed PLA |
| **REQ-MECH-03** | Diameter | 120mm - 150mm (Circular) |
